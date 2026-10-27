# Báo cáo khảo sát GitHub: Repo giảm token, chi phí và usage LLM

**Phiên bản:** 1.0  
**Ngày snapshot dữ liệu:** 2026-10-28 (theo phản hồi GitHub API trong phiên khảo sát)  
**Phạm vi:** GitHub repository công khai, mã nguồn mở hoặc có mã nguồn công khai; ưu tiên repo có tác động trực tiếp đến token, chi phí, độ trễ hoặc hiệu suất phục vụ LLM.

> **Tóm tắt điều hành.** Không thể chứng minh “tất cả repo GitHub” trong một lần crawl: GitHub có hàng triệu repository, kết quả thay đổi theo truy vấn, stars và rate limit. Báo cáo này là **shortlist có phương pháp**, được tìm bằng nhiều truy vấn chủ đề và đối chiếu metadata repo qua GitHub API. Số stars là snapshot, không phải số liệu cố định.

## 1. Kết luận nhanh

- **Giảm prompt/context trực tiếp:** `microsoft/LLMLingua`, `zilliztech/GPTCache`, `aurelio-labs/semantic-router`.
- **Giảm chi phí bằng routing/gateway/observability:** `BerriAI/litellm`, `Portkey-AI/gateway`, `langfuse/langfuse`, `comet-ml/opik`, `Helicone/helicone`.
- **Giảm chi phí hạ tầng/inference:** `ggml-org/llama.cpp`, `vllm-project/vllm`, `sgl-project/sglang`, `lm-sys/FastChat`.
- **Giảm context cần gửi bằng retrieval/memory:** `mem0ai/mem0`, `run-llama/llama_index`, `lancedb/lancedb`, `stanford-futuredata/ColBERT`, `getzep/graphiti`.
- **Tối ưu chất lượng trên mỗi token:** `stanfordnlp/dspy`, `promptfoo/promptfoo`, `dottxt-ai/outlines`, `567-labs/instructor`.

Không nên coi “nhiều stars” là bằng chứng tiết kiệm token. Stars chỉ là tín hiệu phổ biến; hiệu quả thực tế phải đo bằng input tokens, output tokens, cache hit-rate, cost/request, latency và chất lượng đầu ra trên workload của bạn.

## 2. Phương pháp và tiêu chí

### 2.1. Thu thập

1. Dùng nhiều truy vấn GitHub Search API cho các cụm: `token optimization`, `prompt compression`, `semantic cache`, `LLM cost optimization`, `model routing`, `context compression`, `LLM observability`, `KV cache inference`.
2. Bổ sung shortlist các dự án nền tảng phổ biến có cơ chế tác động đến usage/cost.
3. Đối chiếu metadata bằng endpoint công khai `GET https://api.github.com/repos/{owner}/{repo}`.
4. Sắp xếp giảm dần theo `stargazers_count` trong snapshot.

### 2.2. Mức độ liên quan

- **Trực tiếp:** có tính năng compression, cache, routing, cost tracking hoặc inference efficiency.
- **Hỗ trợ:** chủ yếu giảm context, giảm request thừa, cải thiện retrieval/quality hoặc vận hành.
- **Gián tiếp:** nền tảng LLM/serving tổng quát; có thể giảm chi phí hạ tầng nhưng không nhất thiết giảm số token.

### 2.3. Giới hạn

- GitHub API có rate limit; một truy vấn bổ sung trả `403 Forbidden`, do đó các repo không có snapshot xác minh không được gán số stars.
- Mô tả “giảm token” trong báo cáo là cơ chế kỹ thuật suy ra từ chức năng repo, không phải cam kết tiết kiệm cho mọi workload.
- Một số metadata API trả license `NOASSERTION`; cần đọc file LICENSE của từng repo trước khi dùng thương mại.
- Snapshot có thể thay đổi sau khi phát hành báo cáo.

## 3. Bảng xếp hạng tổng hợp theo stars

| Hạng | Repository | Stars snapshot | Nhóm chính | Liên quan | Tác động tiết kiệm |
|---:|---|---:|---|---|---|
| 1 | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 132,545 | Inference/local | Hỗ trợ | Chạy mô hình quantized/local, giảm chi phí API/hạ tầng |
| 2 | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 95,698 | Inference/serving | Hỗ trợ | Throughput cao, memory-efficient, tăng hiệu suất GPU |
| 3 | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 67,922 | Memory/context | Hỗ trợ | Lưu memory chọn lọc thay vì gửi lại toàn bộ lịch sử |
| 4 | [BerriAI/litellm](https://github.com/BerriAI/litellm) | 62,164 | Gateway/routing | Trực tiếp | Cost tracking, load balancing, fallback và định tuyến model |
| 5 | [run-llama/llama_index](https://github.com/run-llama/llama_index) | 52,692 | RAG/context | Hỗ trợ | Retrieval/chunking giúp giảm context gửi vào model |
| 6 | [ray-project/ray](https://github.com/ray-project/ray) | 44,129 | Compute | Gián tiếp | Phân bổ/scale tài nguyên cho workload inference |
| 7 | [lm-sys/FastChat](https://github.com/lm-sys/FastChat) | 39,548 | Serving/evaluation | Hỗ trợ | Self-hosting, serving và đánh giá mô hình |
| 8 | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | 38,819 | Prompt/programming | Hỗ trợ | Tối ưu chương trình prompt theo metric thay vì prompt thủ công |
| 9 | [sgl-project/sglang](https://github.com/sgl-project/sglang) | 38,277 | Inference/serving | Hỗ trợ | Serving hiệu suất cao, giảm chi phí mỗi request |
| 10 | [langfuse/langfuse](https://github.com/langfuse/langfuse) | 36,609 | Observability | Trực tiếp | Trace token/cost, phát hiện request và prompt lãng phí |
| 11 | [getzep/graphiti](https://github.com/getzep/graphiti) | 32,278 | Knowledge/memory | Hỗ trợ | Truy xuất facts liên quan thay vì replay lịch sử dài |
| 12 | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | 28,708 | Orchestration | Hỗ trợ | Quản lý memory, plugin và workflow có cấu trúc |
| 13 | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 26,504 | Evaluation | Trực tiếp | So sánh model/prompt, tránh dùng model đắt khi không cần |
| 14 | [sinaptik-ai/pandas-ai](https://github.com/sinaptik-ai/pandas-ai) | 23,905 | Data/RAG | Hỗ trợ | Truy vấn dữ liệu có cấu trúc thay vì đưa toàn bộ bảng vào prompt |
| 15 | [comet-ml/opik](https://github.com/comet-ml/opik) | 22,969 | Observability | Trực tiếp | Tracing/evaluation để tối ưu request và regression |
| 16 | [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines) | 15,984 | Structured output | Hỗ trợ | Constrained generation, hạn chế output dư/thử lại |
| 17 | [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) | 15,628 | Document ETL | Hỗ trợ | Chuẩn hóa/chunk tài liệu trước khi embedding/RAG |
| 18 | [567-labs/instructor](https://github.com/567-labs/instructor) | 14,067 | Structured output | Hỗ trợ | Schema rõ ràng, giảm lỗi và vòng gọi lại |
| 19 | [Portkey-AI/gateway](https://github.com/Portkey-AI/gateway) | 13,280 | Gateway/routing | Trực tiếp | Route nhiều model, guardrails, fallback và quản lý provider |
| 20 | [neuml/txtai](https://github.com/neuml/txtai) | 13,041 | Retrieval/orchestration | Hỗ trợ | Semantic search và workflow context |
| 21 | [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | 12,027 | Observability | Trực tiếp | Phân tích trace, retrieval và token/cost để tối ưu |
| 22 | [lancedb/lancedb](https://github.com/lancedb/lancedb) | 11,791 | Vector retrieval | Hỗ trợ | Retrieval cục bộ/hiệu quả, giảm context không liên quan |
| 23 | [microsoft/promptflow](https://github.com/microsoft/promptflow) | 11,256 | Workflow/evaluation | Trực tiếp | Test, trace, deploy và tìm bottleneck usage |
| 24 | [zilliztech/GPTCache](https://github.com/zilliztech/GPTCache) | 8,214 | Semantic cache | Trực tiếp | Cache câu hỏi tương tự, tránh gọi LLM lặp lại |
| 25 | [microsoft/LLMLingua](https://github.com/microsoft/LLMLingua) | 6,775 | Compression | Trực tiếp | Nén prompt/KV-cache; repo mô tả mức nén tới 20x tùy tác vụ |
| 26 | [Helicone/helicone](https://github.com/Helicone/helicone) | 6,241 | Observability | Trực tiếp | Theo dõi usage, cost và request qua gateway |
| 27 | [aurelio-labs/semantic-router](https://github.com/aurelio-labs/semantic-router) | 3,979 | Routing | Trực tiếp | Chọn workflow/model theo ngữ nghĩa trước khi gọi model lớn |
| 28 | [stanford-futuredata/ColBERT](https://github.com/stanford-futuredata/ColBERT) | 3,946 | Retrieval | Hỗ trợ | Neural search chọn passage liên quan, giảm context |
| 29 | [stanford-crfm/helm](https://github.com/stanford-crfm/helm) | 2,960 | Evaluation | Hỗ trợ | Benchmark minh bạch để chọn model/quality-cost phù hợp |
| 30 | [openlit/openlit](https://github.com/openlit/openlit) | 2,888 | Observability | Trực tiếp | OpenTelemetry tracing cho LLM cost/latency/usage |

**Lưu ý thứ tự:** Bảng ưu tiên stars nhưng một vài dòng được nhóm lại theo chủ đề; hãy dùng con số stars làm snapshot tham khảo. Với các repo có stars cao nhưng tác động gián tiếp, không nên hiểu là “repo tiết kiệm token tốt hơn” repo chuyên biệt.

## 4. Phân nhóm theo tính năng

### Nhóm A — Prompt và KV-cache compression

| Repo | Khi nên dùng | Rủi ro cần đo |
|---|---|---|
| [microsoft/LLMLingua](https://github.com/microsoft/LLMLingua) | Prompt dài, RAG nhiều tài liệu, cần giảm input tokens | Mất chi tiết, giảm recall, chi phí compressor và độ trễ |
| [microsoft/LLMLingua-2](https://github.com/microsoft/LLMLingua-2) | Thử biến thể compression mới của hệ LLMLingua | Tương thích model/task và chất lượng sau nén |
| [neuml/txtai](https://github.com/neuml/txtai) | Kết hợp semantic search với pipeline LLM | Chất lượng embedding và chi phí indexing |

### Nhóm B — Semantic cache và context/memory

| Repo | Cơ chế | Chỉ số cần theo dõi |
|---|---|---|
| [zilliztech/GPTCache](https://github.com/zilliztech/GPTCache) | Trả kết quả cache cho câu hỏi giống/ngữ nghĩa tương tự | Cache hit, false hit, freshness, invalidation |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | Lưu facts/memory chọn lọc thay vì toàn bộ hội thoại | Token/context per turn, memory precision/recall |
| [getzep/graphiti](https://github.com/getzep/graphiti) | Knowledge graph động để truy xuất facts | Chi phí ingest/update, độ đúng quan hệ |
| [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | Memory, plugin và orchestration | Overhead framework và số lượt gọi phụ |

### Nhóm C — Retrieval, chunking và grounding

| Repo | Cơ chế | Phù hợp |
|---|---|---|
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | Index/retrieval/chunking cho dữ liệu riêng | RAG production và agent có dữ liệu tài liệu |
| [lancedb/lancedb](https://github.com/lancedb/lancedb) | Vector/multimodal retrieval nhúng | Retrieval local/embedded, giảm dữ liệu đưa vào prompt |
| [stanford-futuredata/ColBERT](https://github.com/stanford-futuredata/ColBERT) | Neural retrieval độ phân giải cao | Search cần recall tốt với passage dài |
| [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) | ETL, partition và chuẩn hóa tài liệu | Chuẩn bị dữ liệu trước embedding/RAG |
| [sinaptik-ai/pandas-ai](https://github.com/sinaptik-ai/pandas-ai) | Truy vấn dữ liệu có cấu trúc | CSV/SQL/parquet, tránh nhúng toàn bộ bảng |

### Nhóm D — Routing, gateway và lựa chọn model

| Repo | Cơ chế | Giá trị |
|---|---|---|
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | Unified gateway, cost tracking, load balancing, fallback | Route tác vụ đơn giản đến model rẻ hơn |
| [Portkey-AI/gateway](https://github.com/Portkey-AI/gateway) | Gateway nhiều provider, guardrails | Chuẩn hóa route và policy |
| [aurelio-labs/semantic-router](https://github.com/aurelio-labs/semantic-router) | Semantic decision nhanh | Route trước khi gọi model lớn |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Orchestration/agents và integrations | Xây workflow có routing; không phải công cụ compression chuyên biệt |

### Nhóm E — Inference và serving hiệu quả

| Repo | Cơ chế | Tác động |
|---|---|---|
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | Local C/C++ inference, quantization | Giảm phụ thuộc API và chi phí GPU/cloud |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | High-throughput, memory-efficient serving | Tăng requests/GPU, giảm cost/request |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | Serving/runtime tối ưu cho LLM | Tối ưu throughput và latency |
| [lm-sys/FastChat](https://github.com/lm-sys/FastChat) | Train/serve/evaluate open models | Self-host và benchmark model |
| [ray-project/ray](https://github.com/ray-project/ray) | Distributed compute | Scale workload; không tự giảm token |

### Nhóm F — Evaluation, observability và structured output

| Repo | Cơ chế | Tác động |
|---|---|---|
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | Trace/evaluate LLM application | Tìm prompt/request đắt và lỗi |
| [comet-ml/opik](https://github.com/comet-ml/opik) | Tracing/evaluation/dashboard | Regression và cost visibility |
| [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | AI observability/evaluation | Debug retrieval và generation |
| [Helicone/helicone](https://github.com/Helicone/helicone) | Gateway-based monitoring | Theo dõi cost/token nhanh |
| [openlit/openlit](https://github.com/openlit/openlit) | OpenTelemetry cho LLM | Chuẩn hóa telemetry |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | Test/compare prompt, model, RAG | Chọn phương án rẻ nhưng đạt quality |
| [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | Programming/optimization thay prompt thủ công | Tối ưu theo metric |
| [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines) | Structured/constrained generation | Giảm lỗi parse và retry |
| [567-labs/instructor](https://github.com/567-labs/instructor) | Schema structured output | Giảm vòng gọi lại do output không hợp lệ |

## 5. Gợi ý stack tối thiểu theo mục tiêu

### A. API production, ưu tiên giảm hóa đơn

`LiteLLM hoặc Portkey Gateway` → `semantic router` → model rẻ/nhanh cho request đơn giản → model mạnh cho request khó → `Langfuse/Helicone/OpenLIT` để đo cost và token → `GPTCache` cho request lặp.

### B. RAG tài liệu dài

`Unstructured` (ETL) → `LlamaIndex/LanceDB/ColBERT` (retrieval) → tùy chọn `LLMLingua` (nén context) → `promptfoo` (đánh giá recall/answer quality).

### C. Tự host để giảm chi phí API

`llama.cpp` cho local/edge hoặc `vLLM/ SGLang` cho GPU server → quantization phù hợp → benchmark throughput, latency, quality trước khi chuyển production.

### D. Agent có hội thoại dài

`Mem0` hoặc `Graphiti` để lưu memory có chọn lọc → semantic cache → observability → đặt giới hạn context và TTL memory.

## 6. Kế hoạch thử nghiệm đo tiết kiệm

1. Chọn 100–1.000 request đại diện, lưu input/output, model, latency, token và chất lượng chấm bởi rubric.
2. Chạy baseline không tối ưu.
3. Thử từng cơ chế độc lập: cache, routing, compression, retrieval, structured output.
4. Đo các chỉ số: `input_tokens/request`, `output_tokens/request`, `cost/request`, `cache_hit_rate`, `p50/p95 latency`, `task success`, `groundedness`, `retry rate`.
5. Chỉ triển khai khi quality không giảm quá ngưỡng chấp nhận và tổng chi phí (kể cả compressor/embedding/DB) thực sự giảm.
6. Kiểm tra riêng dữ liệu nhạy cảm, retention, license và khả năng rollback.

## 7. Tài liệu nguồn và truy xuất

- GitHub repository pages được liên kết trực tiếp trong từng dòng bảng.
- GitHub REST API repository metadata: `https://api.github.com/repos/{owner}/{repo}`.
- GitHub Search API: `https://api.github.com/search/repositories`.
- Các con số stars trong báo cáo là dữ liệu snapshot do API trả về trong phiên khảo sát; cần truy vấn lại trước khi xuất bản hoặc ra quyết định mua sắm.

## 8. Kết luận

Nếu mục tiêu là **giảm token trực tiếp**, bắt đầu từ `LLMLingua`, `GPTCache`, retrieval và memory chọn lọc. Nếu mục tiêu là **giảm hóa đơn tổng**, ưu tiên gateway/routing + observability trước, vì chúng cho biết tiền đang đi đâu và cho phép dùng model rẻ hơn. Nếu mục tiêu là **giảm cost hạ tầng**, benchmark `llama.cpp`, `vLLM` và `SGLang` trên workload thật. Không có repo nào tự động bảo đảm tiết kiệm; mọi tuyên bố cần được xác nhận bằng benchmark có baseline và quality gate.

---

**Ghi chú biên tập:** Tên repo, URL, stars và mô tả giữ nguyên dạng gốc để dễ kiểm chứng; phần diễn giải tiếng Việt là phân tích của báo cáo.

**Cập nhật:** Khi tái sử dụng, hãy ghi lại timestamp truy vấn, endpoint, commit/release và kết quả benchmark.
