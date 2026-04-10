# Member 1 Parameter Sweep

- Embedding backend: `text-embedding-3-small`
- top_k: `3`

| chunk_tokens | overlap | chunks | avg_top1_score | relevant_top3 (/5) |
|---|---:|---:|---:|---:|
| 220 | 10% (22) | 160 | 0.3893 | 3 |
| 300 | 10% (30) | 117 | 0.3696 | 4 |
| 420 | 10% (42) | 84 | 0.3602 | 2 |
