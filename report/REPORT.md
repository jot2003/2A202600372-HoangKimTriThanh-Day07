# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Hoàng Kim Trí Thành  
**MSSV:** 2A202600372  
**Nhóm:** E3-C401  
**Ngày:** 10/04/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**  
Theo cách em hiểu, high cosine similarity nghĩa là hai đoạn text có vector gần cùng hướng, nên nội dung ngữ nghĩa khá giống nhau. Điểm càng gần 1 thì mức tương đồng càng cao.

**Ví dụ HIGH similarity:**
- Sentence A: "Python supports object-oriented programming."
- Sentence B: "Python includes object-oriented features."
- Tại sao tương đồng: Cả hai cùng nói về đặc tính OOP của Python, chỉ khác cách diễn đạt.

**Ví dụ LOW similarity:**
- Sentence A: "Customer support tickets should be prioritized by urgency."
- Sentence B: "Bananas are rich in potassium."
- Tại sao khác: Hai câu thuộc hai ngữ cảnh hoàn toàn khác, gần như không có giao nhau về ý nghĩa.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**  
Với embedding, độ lớn vector có thể bị ảnh hưởng bởi nhiều yếu tố kỹ thuật, nên so sánh hướng vector sẽ ổn định và hợp lý hơn khi đánh giá nghĩa. Vì vậy cosine similarity thường phản ánh semantic relevance tốt hơn Euclidean distance.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**  
`num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))`  
`= ceil((10000 - 50) / (500 - 50))`  
`= ceil(9950 / 450)`  
`= ceil(22.11)`  
**Đáp án: 23 chunks**

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**  
Khi overlap tăng, bước nhảy giảm nên số chunk tăng. Đổi lại, overlap giúp giữ ngữ cảnh liên tục giữa các chunk, đặc biệt hữu ích khi ý chính nằm sát ranh giới chunk.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Customer discovery / startup interview với sách *The Mom Test*

**Tại sao nhóm chọn domain này?**  
Nhóm em chọn *The Mom Test* vì nội dung tập trung vào các nguyên tắc interview khách hàng rất rõ ràng (compliments, fluff, commitment, advancement). Tài liệu có tính thực tiễn cao, dễ tạo benchmark query và dễ đánh giá đúng/sai theo ngữ cảnh cụ thể.

Ngoài ra, dù chỉ dùng một nguồn chính, file sách đủ dài và có cấu trúc chương/phần rõ, nên vẫn phù hợp để thử nhiều strategy chunking khác nhau.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự (xấp xỉ) | Metadata đã gán |
|---|--------------|-------|-------------------|-----------------|
| 1 | `the_mom_test_part1_foundations.md` | Tách từ `The Mom Test.md` | ~28,500 | `chapter`, `source`, `language`, `domain`, `content_type` |
| 2 | `the_mom_test_part2_bad_data.md` | Tách từ `The Mom Test.md` | ~29,900 | `chapter`, `source`, `language`, `domain`, `content_type` |
| 3 | `the_mom_test_part3_advancement.md` | Tách từ `The Mom Test.md` | ~49,200 | `chapter`, `source`, `language`, `domain`, `content_type` |
| 4 | `the_mom_test_part4_process.md` | Tách từ `The Mom Test.md` | ~49,300 | `chapter`, `source`, `language`, `domain`, `content_type` |
| 5 | `the_mom_test_part5_recap.md` | Tách từ `The Mom Test.md` | ~23,000 | `chapter`, `source`, `language`, `domain`, `content_type` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `chapter` | string | `the_mom_test_part3_advancement` | Lọc theo phạm vi chương |
| `content_type` | string | `rule`, `compliment`, `fluff`, `pitching`, `advancement` | Lọc theo intent của câu hỏi |
| `source` | string | `data/the_mom_test_part2_bad_data.md` | Truy vết nguồn chunk |
| `language` | string | `en` | Đồng bộ ngôn ngữ dữ liệu |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Vai trò của em trong nhóm là **Hoàng Kim Trí Thành - Baseline (đối chứng)**.

Em dùng fixed-size strategy để làm mốc so sánh với các chiến thuật “thông minh” hơn trong nhóm (heading-aware, granular, context-heavy, metadata-focused). Em có chạy sweep nhỏ để xem trong họ fixed-size thì cấu hình nào ổn nhất.

| Cấu hình | Chunk Count | Avg Top-1 Score | Relevant Top-3 (/5) | Nhận xét |
|----------|-------------|-----------------|----------------------|---------|
| Fixed-size 220, overlap 10% | 160 | 0.3893 | 3/5 | Chunk nhỏ, nhiều đoạn bị thiếu ngữ cảnh |
| **Fixed-size 300, overlap 10% (baseline chính thức)** | 117 | 0.3696 | **4/5** | Cân bằng tốt nhất giữa độ phủ và coherence |
| Fixed-size 420, overlap 10% | 84 | 0.3602 | 2/5 | Chunk lớn, dễ nhiễu thông tin không liên quan |

### Strategy Của Em

**Loại:** `FixedSizeChunker` (`chunk_tokens=300`, `overlap=10%`)

**Mô tả cách hoạt động:**  
Em tách tài liệu thành các chunk theo số token cố định, sau đó cho chồng lấp 10% để giữ liên kết giữa các đoạn sát biên. Cách này dễ tái lập, dễ debug, và đặc biệt phù hợp làm baseline vì tham số rõ ràng.

**Tại sao em chọn strategy này cho domain nhóm?**  
Vì nhóm cần một mốc đối chứng ổn định trước khi kết luận strategy khác tốt hơn ở điểm nào. Nếu baseline đã được setup rõ (300/10%), mọi khác biệt ở các strategy còn lại sẽ dễ giải thích hơn.

### So Sánh: Strategy của em vs bộ query nhóm

| Query | Top-1 score | Relevant top-3? | Ghi chú |
|-------|-------------|-----------------|--------|
| Core rule của The Mom Test | 0.3900 | Có | Trúng đoạn định nghĩa The Mom Test |
| Compliments là vàng giả | 0.4012 | Có | Trúng đúng phần compliments/fibs |
| Neo giữ thông tin mơ hồ | 0.3363 | Không | Failure case chính |
| Advancement thành công | 0.4510 | Có | Trúng cụm commitment/advancement |
| Lỡ pitch quá sớm | 0.2692 | Có | Trúng ý chính nhưng score chưa cao |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Hoàng Kim Trí Thành | FixedSizeChunker (300, 10%) | 8/10 (4/5 relevant) | Ổn định, làm đối chứng tốt | Có thể cắt giữa rule |
| Phạm Quốc Dũng | SentenceChunker (granular, 1 câu/chunk) | 8/10 | Match tốt các câu ngắn chứa tín hiệu rõ | Context mỏng khi cần tổng hợp nhiều câu |
| Quách Gia Được | RecursiveChunker (structural, chunk ~1200) | 4/5 relevant (chưa quy đổi điểm nhóm cuối) | Chunk mạch lạc, giữ ý theo đoạn/chương | Score tuyệt đối chưa cao nếu ép threshold 0.7 |
| Đặng Đinh Tú Anh | FixedSizeChunker (1000, overlap=0) | 7/10 (3/5 relevant) | Mỗi chunk chứa nhiều context, thuận lợi cho câu hỏi tổng quát | Chunk quá lớn làm nhiễu chủ đề, query mơ hồ dễ trượt |
| Thành Nam | RecursiveChunker + Metadata Filter (member5 run) | 1/5 relevant (chưa quy đổi điểm nhóm cuối) | Có cơ chế lọc theo `content_type` trước khi search | Metadata chưa đủ chính xác nên filter chưa cải thiện kết quả |

**Strategy nào tốt nhất cho domain này? Tại sao?**  
Theo dữ liệu hiện có, hai strategy cho kết quả ổn định nhất là baseline `FixedSize 300+10%` của em và `RecursiveChunker` của bạn Được (đều đạt 4/5 relevant ở bộ query nhóm). Strategy sentence-level của bạn Dũng cũng cho kết quả tốt với câu hỏi cần bằng chứng ngắn. Với member5 metadata-filter, kết quả hiện tại mới 1/5 relevant nên chưa thể kết luận filter mạnh hơn; nhóm cần tinh chỉnh lại metadata schema trước khi đánh giá tiếp.

---

## 4. My Approach — Cá nhân (10 điểm)

Phần này em mô tả ngắn gọn cách em triển khai các TODO trong `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:  
Em dùng regex tách theo ranh giới câu (`.`, `!`, `?`) và giữ nguyên dấu câu trong từng sentence để không mất ngữ nghĩa. Sau đó em gom theo `max_sentences_per_chunk`. Em xử lý text rỗng và lọc phần tử trắng trước khi trả kết quả.

**`RecursiveChunker.chunk` / `_split`** — approach:  
Em triển khai theo thứ tự separator ưu tiên (đoạn > dòng > câu > từ > ký tự). Base case là khi chunk đã nhỏ hơn `chunk_size` hoặc hết separator thì cắt cứng. Ý chính là tận dụng cấu trúc tự nhiên tối đa trước khi fallback sang hard split.

### EmbeddingStore

**`add_documents` + `search`** — approach:  
Em chuẩn hóa mỗi document thành record gồm `id`, `content`, `metadata`, `embedding`. Khi search, em embed query, tính score bằng dot product, sort giảm dần và lấy top-k.

**`search_with_filter` + `delete_document`** — approach:  
Với `search_with_filter`, em filter theo metadata trước rồi mới search để đúng yêu cầu bài. Với `delete_document`, em xóa toàn bộ chunk theo `doc_id` và trả `True/False` để phản ánh có xóa thành công hay không.

### KnowledgeBaseAgent

**`answer`** — approach:  
Em retrieve top-k chunks, ghép thành context có đánh số chunk, rồi build prompt yêu cầu trả lời dựa trên context. Sau đó gọi `llm_fn` để sinh câu trả lời.

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

**Kết quả nào bất ngờ nhất? Điều này nói gì về embeddings?**  
Em bất ngờ nhất ở cặp 1 và 4 vì về nghĩa thì khá gần nhưng điểm vẫn thấp. Điều này cho thấy kết quả phụ thuộc mạnh vào backend embedding. Mock embedding phù hợp để test chức năng code, nhưng không đại diện tốt cho semantic quality thật.

---

## 6. Results — Cá nhân (10 điểm)

Em chạy 5 benchmark queries nhóm trên `The Mom Test.md` với cấu hình baseline của em (`FixedSize 300 + overlap 10%`, `top_k=3`, embedding `text-embedding-3-small`).

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

**Chấm nhanh theo rubric 2/1/0 (ước lượng):**
- Q1: 2 điểm
- Q2: 2 điểm
- Q3: 0 điểm
- Q4: 2 điểm
- Q5: 1 điểm (relevant nhưng score thấp, câu trả lời còn ngắn)

**Tổng ước lượng:** 7 / 10

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất em học được từ thành viên khác trong nhóm:**  
Từ bạn Dũng, em học được là sentence-level chunking rất hợp khi cần truy xuất một câu bằng chứng cụ thể. Từ bạn Tú Anh, em thấy rõ trade-off của chunk lớn: có lợi cho câu hỏi tổng quát nhưng dễ nhiễu ở câu hỏi hẹp. Từ bạn Được, em thấy recursive giữ ngữ cảnh đoạn tốt hơn nên trả lời khái niệm mạch lạc hơn baseline.

**Điều hay nhất em học được từ nhóm khác (qua demo):**  
Nhóm khác nhấn mạnh việc không nên dùng cứng một ngưỡng score duy nhất cho mọi query, mà cần đọc thêm mức độ liên quan thực tế trong top-3. Insight này rất đúng với kết quả nhóm em, vì có những query score không cao nhưng chunk vẫn relevant.

**Nếu làm lại, em sẽ thay đổi gì trong data strategy?**  
Em sẽ chuẩn hóa metadata ở cấp chunk ngay từ đầu theo schema nhóm (`chapter`, `content_type`, `source`, `language`) và ép mọi thành viên ingest cùng format để so sánh công bằng hơn. Ngoài ra, em sẽ chuẩn bị sẵn cặp query VI/EN tương đương để giảm mismatch ngôn ngữ khi dữ liệu gốc là tiếng Anh.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 9 / 10 |
| Chunking strategy | Nhóm | 14 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 4 / 5 |
| Results | Cá nhân | 9 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 4 / 5 |
| **Tổng** | | **91 / 100** |
