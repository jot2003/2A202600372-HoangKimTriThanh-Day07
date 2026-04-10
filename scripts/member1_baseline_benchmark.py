from __future__ import annotations

import os
import sys
from dataclasses import dataclass
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


@dataclass
class BenchmarkItem:
    query: str
    gold_answer: str


BENCHMARKS = [
    BenchmarkItem(
        query="Quy tắc cốt lõi của The Mom Test để tránh nhận lời nói dối là gì?",
        gold_answer=(
            "Nói về cuộc đời của họ thay vì ý tưởng của bạn; hỏi về các sự việc "
            "cụ thể trong quá khứ thay vì ý kiến tương lai; nói ít và lắng nghe nhiều."
        ),
    ),
    BenchmarkItem(
        query="Tại sao những lời khen (compliments) lại được coi là vàng giả trong học hỏi khách hàng?",
        gold_answer=(
            "Vì lời khen thường là lịch sự xã giao, khiến founder ảo tưởng nhưng không "
            "cho dữ liệu hành vi đáng tin để ra quyết định."
        ),
    ),
    BenchmarkItem(
        query="Làm thế nào để neo giữ những thông tin mơ hồ từ khách hàng?",
        gold_answer=(
            "Đặt câu hỏi neo vào ví dụ cụ thể trong quá khứ như lần gần nhất, hành động "
            "cụ thể, thay vì chấp nhận phát biểu chung chung."
        ),
    ),
    BenchmarkItem(
        query="Dấu hiệu nào cho thấy một cuộc gặp khách hàng đã thành công (Advancement)?",
        gold_answer=(
            "Khách hàng đưa ra commitment rõ ràng như hẹn bước tiếp theo, giới thiệu "
            "đến người quyết định, hoặc cam kết trả tiền/đặt cọc."
        ),
    ),
    BenchmarkItem(
        query="Bạn nên làm gì khi lỡ tay thuyết trình về ý tưởng của mình quá sớm?",
        gold_answer=(
            "Cần dừng lại, xin lỗi, thừa nhận vừa pitch quá sớm và kéo cuộc trò chuyện "
            "trở lại vấn đề thực tế của khách hàng."
        ),
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

    if chunk_tokens <= 0:
        raise ValueError("chunk_tokens must be > 0")
    if overlap_tokens >= chunk_tokens:
        raise ValueError("overlap_tokens must be < chunk_tokens")

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


def build_documents_from_book(book_path: Path) -> list[Document]:
    text = book_path.read_text(encoding="utf-8", errors="ignore")
    chunk_tokens = 300
    overlap_tokens = int(0.10 * chunk_tokens)  # 10% overlap
    chunks = token_chunks(text, chunk_tokens=chunk_tokens, overlap_tokens=overlap_tokens)

    docs: list[Document] = []
    for idx, chunk in enumerate(chunks):
        docs.append(
            Document(
                id=f"momtest_chunk_{idx:04d}",
                content=chunk,
                metadata={
                    "source": "The Mom Test.md",
                    "strategy": "member1_fixedsize_300tok_10overlap",
                    "chunk_index": idx,
                    "chunk_tokens": chunk_tokens,
                    "overlap_tokens": overlap_tokens,
                },
            )
        )
    return docs


def evaluate_relevance(results: list[dict], gold_answer: str) -> bool:
    # Lightweight heuristic for quick benchmark notes in the report.
    gold_terms = [w.lower() for w in gold_answer.split() if len(w) > 4][:8]
    for item in results:
        content = item["content"].lower()
        if any(term in content for term in gold_terms):
            return True
    return False


def main() -> None:
    root = Path(".")
    candidates = [root / "The Mom Test.md", root / "data" / "The Mom Test.md"]
    book_path = next((p for p in candidates if p.exists()), None)
    if book_path is None:
        raise FileNotFoundError("Could not find 'The Mom Test.md' in project root or data/")

    embedder = choose_embedder()
    store = EmbeddingStore(collection_name="member1_momtest", embedding_fn=embedder)
    docs = build_documents_from_book(book_path)
    store.add_documents(docs)

    top_k = 3
    score_threshold = 0.7

    lines: list[str] = []
    lines.append("# Member 1 Baseline Benchmark (The Mom Test)")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Source file: `{book_path}`")
    lines.append("- Strategy: Fixed-size 300 tokens, 10% overlap (30 tokens)")
    lines.append(f"- Embedding backend: `{getattr(embedder, '_backend_name', embedder.__class__.__name__)}`")
    lines.append(f"- top_k: `{top_k}`")
    lines.append(f"- score_threshold: `{score_threshold}`")
    lines.append(f"- Indexed chunks: `{store.get_collection_size()}`")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| # | Query | Top-1 score | Top-1 chunk id | Above 0.7? | Relevant in top-3? |")
    lines.append("|---|-------|-------------|----------------|------------|--------------------|")

    for i, item in enumerate(BENCHMARKS, start=1):
        results = store.search(item.query, top_k=top_k)
        top1 = results[0] if results else None
        top1_score = top1["score"] if top1 else 0.0
        top1_chunk_id = top1["id"] if top1 else "-"
        above_threshold = "yes" if top1 and top1_score >= score_threshold else "no"
        relevant = "yes" if evaluate_relevance(results, item.gold_answer) else "no"
        lines.append(
            f"| {i} | {item.query} | {top1_score:.4f} | {top1_chunk_id} | {above_threshold} | {relevant} |"
        )

        lines.append("")
        lines.append(f"### Query {i} details")
        lines.append(f"- Gold answer: {item.gold_answer}")
        for rank, result in enumerate(results, start=1):
            preview = result["content"][:240].replace("\n", " ")
            lines.append(
                f"- Top-{rank}: score={result['score']:.4f}, id={result['id']}, preview={preview}..."
            )
        lines.append("")

    out_path = root / "report" / "member1_baseline_results.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

