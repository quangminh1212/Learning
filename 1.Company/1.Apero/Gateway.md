# Apero AI Gateway: chọn provider và tính giá

*Giá gói tại Mỹ, chưa thuế; giá API bằng USD. Cập nhật 29-10-2026.*

## Thứ tự ưu tiên

**Subscription của từng user → API key → model chạy trên máy/cụm GPU của mình.** Chỉ nối subscription qua Gateway theo điều khoản của provider; không dùng chung account hoặc gom quota.

| Cách dùng | Chi phí | Ưu điểm | Hạn chế |
|---|---|---|---|
| **Subscription CLI** | Phí tháng/user | Thường rẻ hơn API; phép thử Claude dưới đây quy đổi được khoảng 46–60 lần phí gói | Quota có giới hạn và khác nhau theo plan |
| **API key** | Tính theo token | Dễ mở rộng và đặt ngân sách | Tốn hơn khi lượng dùng tăng |
| **Local/self-host** | GPU + điện/hosting + vận hành | Chủ động dữ liệu; có thể rẻ khi tải cao, ổn định | GPU đắt; phải tự vận hành |

## Giá API tham chiếu

Giá cho **1 triệu token đầu vào / đầu ra**. Ví dụ dưới đây chưa tính cache hoặc công cụ.

| Model | Giá USD / 1M token |
|---|---:|
| Claude Fable 5.1 | $10 / $50 |
| Claude Opus 5.5 | $4 / $20 |
| Claude Sonnet 5.5 | $2 / $10 |
| Claude Haiku 5.5 (đầu vào ≤100k) | $0.10 / $0.50 |
| DeepSeek V4.1 Flash, giờ cao điểm | $0.30 / $1.20 |
| DeepSeek V4.1 Flash, giờ thấp điểm | $0.15 / $0.60 |
| GPT-6 Astra | $10 / $50 |
| GPT-6.1 Sol | $2 / $10 |
| GPT-6.1 Terra | $1 / $5 |
| GPT-6 Luna (đầu vào ≤272k) | $0.10 / $0.50 |

**Request mẫu: 100k đầu vào + 20k đầu ra** → Sonnet **$0.40**; Opus **$0.80**; Haiku **$0.02**; DeepSeek Flash **$0.054 giờ cao điểm / $0.027 giờ thấp điểm**; GPT Astra **$2.00**; Sol **$0.40**; Terra **$0.20**; Luna **$0.02**.

Haiku đắt hơn khi đầu vào vượt 100k: **$0.50/$2.50**. GPT-6 Luna đắt hơn khi vượt 272k: **$0.20/$0.75**. DeepSeek có giá đọc lại đầu vào đã cache **$0.006/1M giờ cao điểm**, **$0.003/1M giờ thấp điểm**.

## Subscription Claude: tính cả quota dùng và API credit

PDF quy đổi quota Claude khi dùng hết sang giá token API. Conversation là chat; Automated coding là agent tự làm nhiều bước code.

| Gói | Phí tháng | Giá API của quota dùng hết: Conversation / Automated coding |
|---|---:|---:|
| Pro | $20 (hoặc $200/năm) | ~$920 / ~$1,173 |
| Max 5x | $100 | ~$4,600 / ~$5,863 |
| Max 20x | $200 | ~$9,200 / ~$11,726 |

Max 20x là phép đo trực tiếp; Pro và Max 5x được ước tính theo tỷ lệ phí. Đây là giá trị nếu dùng hết quota, không phải mức trung bình hay cam kết. Max 5x còn có **$100 API credit**, Max 20x có **$200**. Nếu đã claim và tiêu hết credit cho API riêng, cộng thêm khoản đó: tổng lần lượt **$4,700–$5,963** và **$9,400–$11,926**. Credit chưa dùng không tính là usage; không tính credit hai lần cho cùng request.

**Team:** Standard/Premium giá **$25/$125 mỗi ghế/tháng**, hoặc **$20/$100** khi trả năm. Có **$20/$100 API credit mỗi ghế**, dùng chung tối đa **$500**.

**Enterprise mới:** **$20/người/tháng**, cam kết năm; không kèm quota token. Tổng = phí ghế + toàn bộ usage Claude/API tính theo token.

**OpenAI:** ChatGPT Plus **$20/tháng**, không có API credit. ChatGPT Pro **$100/$200/$500** có thể nhận cùng mức API credit nếu claim; khoản này dùng cho API, không tăng quota Codex. PDF không có số quy đổi token đủ tin cậy cho quota Codex.

**DeepSeek:** không có gói quota CLI tương ứng; dùng API key.

Khi có log token, tính giá trị subscription bằng: **token CLI đã dùng × giá API + API credit đã tiêu cho request riêng**. Nếu thiếu log input/output theo model thì ghi “chưa đo được”, không tự quy đổi quota thành token.

*Lưu ý:* số Sonnet trong PDF dùng giá đọc cache cũ **$0.20/1M**; giá hiện tại là **$0.10/1M**, nên không dùng số quy đổi Sonnet đó làm giá hiện hành.

## Hòa vốn thuê hoặc mua DeepSeek V4.1 Flash

Dùng weights mới nhất **DeepSeek-V4.1-Flash-1017**. Recipe vLLM nêu cấu hình tối thiểu là **máy chủ 8 GPU H100, mỗi GPU 80GB**.

### Giá máy chủ

| Nơi | Thuê 8×H100 | Mua 8×H100 |
|---|---:|---:|
| **Mỹ** | ~$555–$766/ngày | $310k–$315k cho máy hoàn chỉnh (~₫8,07–8,20 tỷ); khấu hao 3 năm là ~$283–$288/ngày |
| **Việt Nam** | ₫346–₫554 triệu/tháng (~₫11,5–₫18,5 triệu/ngày) cho máy 8 GPU | ₫8,73 tỷ cho riêng 8 GPU H100 SXM5; máy chủ hoàn chỉnh cần báo giá |

Giá thuê Mỹ tính từ đơn giá RunPod cho từng GPU × 8 × 24 giờ; đây là ước tính, không phải báo giá node 8 GPU. Giá thuê Việt Nam là hai cấu hình 8 GPU được niêm yết. Giá mua Mỹ là máy hoàn chỉnh, chưa gồm thuế/vận chuyển. Giá mua Việt Nam là giá GPU SXM5 trong nước **₫1,091 tỷ/GPU × 8**; chưa gồm máy chủ và linh kiện nên chỉ là mức sàn. Máy HGX 8 GPU bán tại Việt Nam hiện cần hỏi báo giá. Tỷ giá quy đổi: **$1 ≈ ₫26.040**.

### Tiền điện và công vận hành

| Nơi | Điện/ngày | Quản lý/ngày |
|---|---:|---:|
| **Mỹ** | ~$50 | ~$27 |
| **Việt Nam** | ~₫820.000 | ~₫150.000 |

Tiền điện lấy công suất tối đa **10,2 kW** của máy 8×H100, chạy 24 giờ/ngày, nhân PUE **1,52** để tính cả làm mát: khoảng **372 kWh/ngày**. Dùng giá điện kinh doanh Mỹ năm 2025 và giá điện bình quân EVN của Việt Nam (chưa VAT). Đây là dự toán cao theo mức tối đa; máy thực tế có thể dùng ít điện hơn.

Chi phí quản lý phân bổ **0,1 FTE** (khoảng 4 giờ/tuần) của một kỹ sư DevOps/sysadmin dùng chung để cài đặt, theo dõi và bảo trì mô hình. Đây là lương gộp tham chiếu, chưa tính phúc lợi và trực 24/7. Giá thuê GPU được giả định đã gồm điện; chỉ cộng công vận hành.

**Khấu hao** là cách chia giá mua máy thành chi phí theo thời gian sử dụng. Trong bài này tính thẳng đều trong **3 năm (1.095 ngày), giá trị còn lại bằng 0**: giá mua chia 1.095. Ví dụ, máy Mỹ $310k–$315k tương đương $283–$288/ngày; đây là chi phí quy đổi để so sánh, không phải tiền trả hàng ngày (tiền mua máy trả trước).

### Tốc độ input/output trên 8×H100

Benchmark vLLM FP4 + MTP (dự đoán nhiều token) trên tải coding-agent đa lượt của AgentX, đo ngày **26/10/2026**. Input/output là tổng tốc độ của cả cụm; concurrency là số phiên agent chạy đồng thời.

| Agent đồng thời | Input prompt tok/s* | Output tok/s | Output/ngày** | Tốc độ stream/user P90 |
|---:|---:|---:|---:|---:|
| 1 | ~22.600 | ~155 | ~13,4 triệu | ~323 tok/s |
| 4 | ~33.100 | ~228 | ~19,7 triệu | ~260 tok/s |
| 8 | ~58.000 | ~424 | ~36,6 triệu | ~183 tok/s |
| 16 | ~107.600 | ~686 | ~59,2 triệu | ~132 tok/s |
| 28 | ~156.900 | ~1.031 | ~89,1 triệu | ~66 tok/s |

*Input prompt tok/s tính cả token được lấy từ prefix cache. Ở 28 agent, cache hit khoảng **92,7%**; tốc độ input mới cần GPU tính lại đo được khoảng **12.600 tok/s**. Vì vậy 156.900 tok/s không phải tốc độ prefill input mới khi không có cache. **Output/ngày** giả sử chạy đủ 24 giờ với tải liên tục. Tốc độ stream/user là tốc độ khi model đang sinh; tăng số agent làm output tổng tăng nhưng mỗi user nhận token chậm hơn. Đây là throughput đo được, không phải rate limit cố định; traffic và cache thực tế có thể làm số thay đổi.

### Thời gian hòa vốn

Giả sử mỗi request có **100k input + 20k output**, không cache, và GPU chạy đủ tải 24/7. Ở tốc độ tối đa, cụm xử lý khoảng **4.455 request/ngày**; tương đương API trị giá **$241/ngày (~₫6,3 triệu) ở giá cao điểm** hoặc **$120/ngày (~₫3,1 triệu) ở giá thấp điểm**.

| Phương án | Nếu dùng giá API cao điểm | Nếu dùng giá API thấp điểm |
|---|---:|---:|
| Mỹ — thuê | Không hòa vốn | Không hòa vốn |
| Mỹ — mua máy hoàn chỉnh | ~5,2 năm | ~19,6 năm |
| Việt Nam — thuê | Không hòa vốn | Không hòa vốn |
| Việt Nam — mua 8 GPU | ~4,5 năm* | ~11 năm* |

Thuê không hòa vốn vì API tiết kiệm được ít hơn tiền thuê. Thời gian thu hồi vốn khi mua đều dài hơn **3 năm khấu hao**. *Giá Việt Nam chỉ tính 8 GPU, chưa có máy chủ. Cache hoặc máy chạy không hết tải sẽ kéo dài thời gian hòa vốn.

Claude và GPT-6 không có weights để tự chạy; có thể dùng model mở thay thế như gpt-oss-20b (~16GB) hoặc gpt-oss-120b (~80GB). Chúng không phải model Claude/GPT-6.

## Mở rộng gateway

| User | Cách triển khai |
|---:|---|
| **100** | Ưu tiên subscription theo từng user; API có ngân sách giới hạn. |
| **10.000** | Nhiều Gateway, quota theo user; API cho tải tăng giảm; local nếu tải ổn định và đã hòa vốn. |
| **100.000** | Nhiều vùng, dự phòng, hàng đợi; API và/hoặc cụm GPU theo tải đo thực tế. |

Có thể xem cách tổ chức nhiều provider của [9Router](https://github.com/decolua/9router) và [OmniRoute](https://github.com/cheaper-inference/OmniRoute). Cần tuân điều khoản riêng của mỗi provider.

## Nguồn

- [PDF Claude Pro/Max/Enterprise/API — 10/2026](<So sánh Claude Pro Max Enterprise và API - 10.2026.pdf>)
- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Claude plans](https://claude.com/pricing) · [Claude API credits](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)
- [DeepSeek API pricing](https://api-docs.deepseek.com/quick_start/pricing/)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) · [ChatGPT API credits](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)
- [vLLM recipe: DeepSeek V4.1 Flash](https://github.com/vllm-project/vllm/blob/main/recipes/models/deepseek-ai/DeepSeek-V4.1-Flash.yaml) · [RunPod GPU pricing](https://www.runpod.io/pricing) · [Lambda 8×H100 server price](https://shop.lambda.ai/deep-learning/servers/hyperplane/customize?step=3)
- [SemiAnalysis AgentX: benchmark DeepSeek V4.1 Flash trên H100](https://inferencex.semianalysis.com/run/deepseek-v41-flash-on-h100) · [Dữ liệu gốc: cụm 8×H100, vLLM, 26/10/2026](https://inferencex.semianalysis.com/api/v1/benchmarks?model=DeepSeek-V4.1-Flash&runId=40258062314&exactRun=true) · [Input/cache telemetry tại 28 agent](https://inferencex.semianalysis.com/api/v1/trace-server-metrics?id=446618) · [Cách đo AgentX](https://inferencex.semianalysis.com/agentx/methodology)
- [NVIDIA DGX H100 power: 10.2 kW max](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/nvidia-dgx-h100-datasheet.pdf) · [Uptime Institute: PUE 1.52 in 2026](https://intelligence.uptimeinstitute.com/resource/growing-pue-advantage-larger-data-centers)
- [Giá điện kinh doanh Mỹ (EIA, 2025)](https://www.eia.gov/electricity/Annual/table.php?t=epa_02_04.html) · [Giá bình quân EVN](https://www.evn.com.vn/userfile/User/tcdl/files/2025/5/QD1279-QD-BCT-20250509163514982.pdf)
- [Lương sysadmin Mỹ (BLS, 2025)](https://www.bls.gov/ooh/computer-and-information-technology/network-and-computer-systems-administrators.htm) · [Lương DevOps Việt Nam (ITviec)](https://itviec.com/report/vietnam-it-salary-and-recruitment-market-2024-2025)
- [HiTechCloud thuê máy 8×H100](https://hitechcloud.vn/nvidia-dgx-h100/) · [HiTechCloud bare-metal 8×H100](https://hitechcloud.vn/bare-metal-gpu/) · [Giá H100 SXM5 trong nước](https://thuemaychu.vn/bang-gia-gpu-server) · [Báo giá máy HGX H100 8 GPU](https://cnttshop.vn/nvidia-hgx-8-gpu-h100-sxm5)
- [Tỷ giá Vietcombank USD/VND](https://taichinh.com/ty-gia/usd)
- [OpenAI gpt-oss](https://openai.com/index/introducing-gpt-oss/)
