# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Hoàng Kim Trí Thành  
**MSSV:** 2A202600372  
**Nhóm:** Nhóm Data Foundations  
**Ngày:** 10/04/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**  
High cosine similarity nghĩa là hai câu có hướng vector gần nhau trong không gian embedding, tức là nội dung/ngữ nghĩa gần nhau. Điểm càng gần 1 thì mức tương đồng ngữ nghĩa càng cao.

**Ví dụ HIGH similarity:**
- Sentence A: "Python supports object-oriented programming."
- Sentence B: "Python includes object-oriented features."
- Tại sao tương đồng: Cùng nói về cùng một ý chính là đặc tính OOP của Python.

**Ví dụ LOW similarity:**
- Sentence A: "Customer support tickets should be prioritized by urgency."
- Sentence B: "Bananas are rich in potassium."
- Tại sao khác: Hai câu thuộc hai domain hoàn toàn khác nhau, không chia sẻ ngữ cảnh.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**  
Cosine similarity tập trung vào hướng vector nên phản ánh tốt hơn mức tương đồng ngữ nghĩa, ít bị ảnh hưởng bởi độ lớn vector. Với text embeddings, hướng thường quan trọng hơn khoảng cách tuyệt đối theo trục tọa độ.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**  
`num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))`  
`= ceil((10000 - 50) / (500 - 50))`  
`= ceil(9950 / 450)`  
`= ceil(22.11)`  
**Đáp án: 23 chunks**

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**  
Khi overlap tăng, bước nhảy (`chunk_size - overlap`) giảm nên số chunk tăng. Overlap cao giúp giữ ngữ cảnh liên tục giữa các chunk, giảm rủi ro mất ý ở ranh giới cắt.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Customer discovery / startup interview với sách *The Mom Test*

**Tại sao nhóm chọn domain này?**  
Nhóm chọn *The Mom Test* vì nội dung có nhiều rule rõ ràng (compliments, fluff, commitment, advancement), rất phù hợp để đo retrieval theo query thực tế. Dù là một nguồn chính, tài liệu đủ dài và có cấu trúc theo chương để so sánh chunking strategy.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự (xấp xỉ) | Metadata đã gán |
|---|--------------|-------|-------------------|-----------------|
| 1 | `The Mom Test.md` | Sách *The Mom Test* (Markdown đã chuyển đổi) | ~60,000+ | `source`, `chapter`, `topic`, `lang` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `source` | string | `The Mom Test.md` | Truy vết nguồn chunk |
| `chapter` | string | `chapter_03` | Lọc theo phần nội dung |
| `topic` | string | `compliments`, `advancement` | Tăng độ chính xác cho query hẹp |
| `lang` | string | `en` | Đồng bộ ngôn ngữ tài liệu |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Vai trò của em trong nhóm: **Thành viên 1 - Baseline (đối chứng)**.

| Cấu hình | Chunk Count | Avg Top-1 Score | Relevant Top-3 (/5) | Nhận xét |
|----------|-------------|-----------------|----------------------|---------|
| Fixed-size 220, overlap 10% | 160 | 0.3893 | 3/5 | Chunk nhỏ, dễ mất ngữ cảnh |
| **Fixed-size 300, overlap 10% (baseline chính thức)** | 117 | 0.3696 | **4/5** | Cân bằng tốt nhất |
| Fixed-size 420, overlap 10% | 84 | 0.3602 | 2/5 | Chunk lớn, nhiễu nội dung |

### Strategy Của Em

**Loại:** `FixedSizeChunker` (`chunk_tokens=300`, `overlap=10%`)

**Mô tả cách hoạt động:**  
Em chia theo fixed-size trên token để tạo đường cơ sở ổn định cho cả nhóm. Với sách dài như *The Mom Test*, fixed-size giúp kiểm soát số chunk và chi phí embedding, đồng thời làm mốc so sánh công bằng với strategy theo heading/sentence của các bạn khác.

**Tại sao em chọn strategy này cho domain nhóm?**  
Đây là baseline đúng phân công, giúp nhóm đánh giá khách quan: các chiến thuật thông minh hơn tốt hơn baseline ở điểm nào. Ngoài ra em có chạy sweep nhỏ để xác nhận `300 + 10%` là cấu hình fixed-size phù hợp nhất cho bộ benchmark.

### So Sánh: Strategy của em vs Baseline

| Query | Top-1 score | Relevant top-3? | Ghi chú |
|-------|-------------|-----------------|--------|
| Core rule của The Mom Test | 0.3900 | Có | Trúng đoạn định nghĩa The Mom Test |
| Compliments là vàng giả | 0.4012 | Có | Trúng đúng phần compliments |
| Neo giữ thông tin mơ hồ | 0.3363 | Không | Fail case chính |
| Advancement thành công | 0.4510 | Có | Trúng cụm commitment/advancement |
| Lỡ pitch quá sớm | 0.2692 | Có | Có ngữ cảnh đúng nhưng điểm thấp |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Hoàng Kim Trí Thành | FixedSizeChunker (300, 10%) | 8/10 (4/5 relevant) | Ổn định, làm đối chứng tốt | Có thể cắt giữa rule |
| Thành viên 2 | Structure-aware (Heading) | TBD | Giữ cấu trúc chương | Cần xử lý section dài |
| Thành viên 3 | Granular (Paragraph/small chunk) | TBD | Bám chi tiết | Dễ mất context |
| Thành viên 4 | Context-heavy (large chunk) | TBD | Giữ nhiều ngữ cảnh | Nhiễu |
| Thành viên 5 | Metadata-focused | TBD | Lọc query hẹp tốt | Filter quá chặt giảm recall |

**Strategy nào tốt nhất cho domain này? Tại sao?**  
Ở góc nhìn baseline, fixed-size `300 + 10%` đang cân bằng tốt nhất trong nhóm fixed-size. Tuy nhiên với sách có cấu trúc rõ như *The Mom Test*, em kỳ vọng strategy theo heading và strategy metadata-focused sẽ vượt baseline ở các query theo chapter/topic.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:  
Sử dụng regex tách câu theo ranh giới dấu kết thúc câu, giữ dấu câu gắn với nội dung câu để không mất nghĩa. Sau đó gom N câu vào một chunk theo `max_sentences_per_chunk`. Có xử lý edge case text rỗng và loại bỏ phần tử trắng.

**`RecursiveChunker.chunk` / `_split`** — approach:  
Áp dụng đệ quy với danh sách separator theo ưu tiên. Base case là khi `len(text) <= chunk_size` hoặc không còn separator thì cắt cứng theo `chunk_size`. Khi split bằng separator hiện tại, thuật toán cố gắng ghép buffer để chunk vẫn tự nhiên, nếu quá dài thì đệ quy xuống separator tiếp theo.

### EmbeddingStore

**`add_documents` + `search`** — approach:  
Mỗi document được chuẩn hóa thành record gồm `id`, `content`, `metadata`, `embedding`, sau đó lưu vào in-memory list. `search` embed query rồi tính điểm bằng dot product với từng record, sort giảm dần và lấy `top_k`.

**`search_with_filter` + `delete_document`** — approach:  
`search_with_filter` lọc records theo metadata trước rồi mới search (đúng theo yêu cầu lab). `delete_document` xóa toàn bộ chunk có `metadata['doc_id'] == doc_id` và trả `True/False` tùy có xóa được hay không.

### KnowledgeBaseAgent

**`answer`** — approach:  
Agent retrieve top-k chunks từ store, ghép thành context có đánh số chunk, rồi chèn vào prompt template cùng question. Cuối cùng gọi `llm_fn(prompt)` để nhận câu trả lời grounded theo context.

### Test Results

```bash
pytest tests/ -v
...
============================= 42 passed in 0.16s ==============================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Python supports functions and classes. | Python has object-oriented programming features. | high | -0.0539 | Sai |
| 2 | Vector stores index embeddings for similarity search. | Cosine similarity measures vector direction alignment. | high | -0.2049 | Sai |
| 3 | I love cooking Italian pasta recipes. | Neural networks are used in deep learning. | low | -0.0771 | Đúng (thấp) |
| 4 | Customer tickets should be triaged by severity. | Support requests are prioritized by urgency. | high | -0.0589 | Sai |
| 5 | The capital of France is Paris. | Bananas are rich in potassium. | low | -0.2249 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**  
Cặp 1 và 4 bất ngờ vì về nghĩa là gần nhau nhưng điểm vẫn thấp khi dùng mock embedding. Điều này cho thấy backend embedding ảnh hưởng trực tiếp đến quality; mock embedder phù hợp để test chức năng nhưng không phản ánh chính xác ngữ nghĩa như model thật.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên `The Mom Test.md` với cấu hình baseline của em.

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Quy tắc cốt lõi của The Mom Test để tránh nhận lời nói dối là gì? | Nói về cuộc đời họ, hỏi sự kiện quá khứ cụ thể, nói ít và lắng nghe nhiều |
| 2 | Tại sao compliments là “vàng giả”? | Vì là lời khen xã giao, không phải dữ liệu hành vi đáng tin |
| 3 | Neo giữ thông tin mơ hồ bằng cách nào? | Hỏi ví dụ cụ thể trong quá khứ, không chấp nhận câu chung chung |
| 4 | Dấu hiệu cuộc gặp thành công (Advancement)? | Có commitment: bước tiếp theo, giới thiệu, thời gian, tiền |
| 5 | Nên làm gì khi lỡ pitch quá sớm? | Dừng lại, xin lỗi, quay về khai thác vấn đề của khách hàng |

### Kết Quả Của Em

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Core rule tránh lời nói dối | Trúng đoạn định nghĩa “The Mom Test rules” | 0.3900 | Có | Trả lời đúng ý chính |
| 2 | Compliments là vàng giả | Trúng chương nói về compliments/fibs | 0.4012 | Có | Trả lời đúng nguyên nhân |
| 3 | Neo giữ fluff | Top-3 chưa trúng rõ phần “last time/specific” | 0.3363 | Không | Trả lời còn chung chung |
| 4 | Dấu hiệu advancement | Trúng đoạn commitment/advancement | 0.4510 | Có | Trả lời đúng tiêu chí |
| 5 | Lỡ pitch quá sớm xử lý sao | Trúng đoạn khuyên dừng pitch | 0.2692 | Có | Trả lời đúng hướng |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất em học được từ thành viên khác trong nhóm:**  
Với tài liệu dạng sách có heading rõ, strategy theo cấu trúc chương thường giữ coherence tốt hơn fixed-size ở các query chapter-specific.

**Điều hay nhất em học được từ nhóm khác (qua demo):**  
Metadata filter thực sự hữu ích khi query nhắm đúng phạm vi; nhưng nếu filter quá chặt thì chunk đúng có thể bị loại mất.

**Nếu làm lại, em sẽ thay đổi gì trong data strategy?**  
Em sẽ chuẩn hóa topic map ngay từ đầu (`compliments`, `fluff`, `commitment`, `advancement`) và chuẩn hóa query song ngữ để giảm mismatch ngôn ngữ.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 8 / 10 |
| Chunking strategy | Nhóm | 13 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 4 / 5 |
| Results | Cá nhân | 8 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 4 / 5 |
| **Tổng** | | **86 / 100 (self-assessment)** |
