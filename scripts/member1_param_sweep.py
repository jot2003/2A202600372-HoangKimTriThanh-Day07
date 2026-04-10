from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src import (
    EMBEDDING_PROVIDER_ENV,
    LOCAL_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_MODEL,
    EmbeddingStore,
    LocalEmbedder,
    OpenAIEmbedder,
    _mock_embed,
)
from src.models import Document

BENCHMARKS = [
    (
        "Quy tắc cốt lõi của The Mom Test để tránh nhận lời nói dối là gì?",
        "Nói về cuộc đời của họ thay vì ý tưởng của bạn; hỏi về các sự việc cụ thể trong quá khứ thay vì ý kiến tương lai; nói ít và lắng nghe nhiều.",
    ),
    (
        "Tại sao những lời khen (compliments) lại được coi là vàng giả trong học hỏi khách hàng?",
        "Vì lời khen thường là lịch sự xã giao, khiến founder ảo tưởng nhưng không cho dữ liệu hành vi đáng tin để ra quyết định.",
    ),
    (
        "Làm thế nào để neo giữ những thông tin mơ hồ từ khách hàng?",
        "Đặt câu hỏi neo vào ví dụ cụ thể trong quá khứ như lần gần nhất, hành động cụ thể, thay vì chấp nhận phát biểu chung chung.",
    ),
    (
        "Dấu hiệu nào cho thấy một cuộc gặp khách hàng đã thành công (Advancement)?",
        "Khách hàng đưa ra commitment rõ ràng như hẹn bước tiếp theo, giới thiệu đến người quyết định, hoặc cam kết trả tiền/đặt cọc.",
    ),
    (
        "Bạn nên làm gì khi lỡ tay thuyết trình về ý tưởng của mình quá sớm?",
        "Cần dừng lại, xin lỗi, thừa nhận vừa pitch quá sớm và kéo cuộc trò chuyện trở lại vấn đề thực tế của khách hàng.",
    ),
]


def choose_embedder():
    load_dotenv(override=False)
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "mock").strip().lower()
    if provider == "openai":
        try:
            return OpenAIEmbedder(model_name=os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL))
        except Exception:
            return _mock_embed
    if provider == "local":
        try:
            return LocalEmbedder(model_name=os.getenv("LOCAL_EMBEDDING_MODEL", LOCAL_EMBEDDING_MODEL))
        except Exception:
            return _mock_embed
    return _mock_embed


def token_chunks(text: str, chunk_tokens: int, overlap_tokens: int) -> list[str]:
    tokens = text.split()
    if not tokens:
        return []
    step = chunk_tokens - overlap_tokens
    chunks: list[str] = []
    for start in range(0, len(tokens), step):
        part = tokens[start : start + chunk_tokens]
        if not part:
            break
        chunks.append(" ".join(part))
        if start + chunk_tokens >= len(tokens):
            break
    return chunks


def build_docs(book_path: Path, chunk_tokens: int, overlap_tokens: int) -> list[Document]:
    text = book_path.read_text(encoding="utf-8", errors="ignore")
    chunks = token_chunks(text, chunk_tokens=chunk_tokens, overlap_tokens=overlap_tokens)
    docs: list[Document] = []
    for i, chunk in enumerate(chunks):
        docs.append(
            Document(
                id=f"c{i:04d}",
                content=chunk,
                metadata={
                    "source": "The Mom Test.md",
                    "chunk_tokens": chunk_tokens,
                    "overlap_tokens": overlap_tokens,
                },
            )
        )
    return docs


def relevance_hit(results: list[dict], gold: str) -> bool:
    terms = [w.lower() for w in gold.split() if len(w) > 4][:8]
    for r in results:
        content = r["content"].lower()
        if any(t in content for t in terms):
            return True
    return False


def main() -> None:
    root = Path(".")
    book_path = root / "The Mom Test.md"
    if not book_path.exists():
        book_path = root / "data" / "The Mom Test.md"
    if not book_path.exists():
        raise FileNotFoundError("Could not find The Mom Test.md")

    embedder = choose_embedder()
    chunk_sizes = [220, 300, 420]
    overlap_rates = [0.10]
    top_k = 3

    lines: list[str] = []
    lines.append("# Member 1 Parameter Sweep")
    lines.append("")
    lines.append(f"- Embedding backend: `{getattr(embedder, '_backend_name', embedder.__class__.__name__)}`")
    lines.append("- top_k: `3`")
    lines.append("")
    lines.append("| chunk_tokens | overlap | chunks | avg_top1_score | relevant_top3 (/5) |")
    lines.append("|---|---:|---:|---:|---:|")

    for chunk_tokens in chunk_sizes:
        for rate in overlap_rates:
            overlap_tokens = int(chunk_tokens * rate)
            docs = build_docs(book_path, chunk_tokens, overlap_tokens)
            store = EmbeddingStore(
                collection_name=f"sweep_{chunk_tokens}_{overlap_tokens}",
                embedding_fn=embedder,
            )
            store.add_documents(docs)

            top1_scores: list[float] = []
            rel_count = 0
            for query, gold_answer in BENCHMARKS:
                results = store.search(query, top_k=top_k)
                top1_scores.append(results[0]["score"] if results else 0.0)
                if relevance_hit(results, gold_answer):
                    rel_count += 1

            avg_top1 = sum(top1_scores) / len(top1_scores)
            lines.append(
                f"| {chunk_tokens} | {int(rate*100)}% ({overlap_tokens}) | {len(docs)} | {avg_top1:.4f} | {rel_count} |"
            )

    out_path = root / "report" / "member1_param_sweep.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

