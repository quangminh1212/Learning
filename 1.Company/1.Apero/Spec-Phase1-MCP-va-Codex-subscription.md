# Spec Phase 1: MCP chọn model và Codex subscription gateway

- Phạm vi: 10 người, một workspace, bốn tuần đo
- Ngày: 30-10-2026
- Nguồn quyết định: [Gateway.md](Gateway.md), [MCP.md](MCP.md)
- Giá dưới đây là giá niêm yết Mỹ, chưa thuế. Chốt lại ở trang thanh toán trước khi mua. Tỷ giá tham chiếu trong Gateway.md: $1 ≈ ₫26.040

Phase 1 chạy **một** hướng. Mỗi hướng có hóa đơn ghế riêng. Chạy cả hai cùng lúc thì mua cả hai bộ ghế.

Thứ tự tiền trong Gateway.md giữ nguyên: subscription của từng người, rồi API có trần, rồi máy GPU. Phase 1 không mua GPU và không mở đường API.

## Việc phase 1 không làm

- Không dùng chung một account, không gom quota, không xoay nhiều account để né hạn mức.
- Không lưu refresh token hay mật khẩu ChatGPT/Claude trên server.
- Không biến subscription thành API key cho app khác gọi. Gateway Codex chỉ nhận request từ Codex CLI, app desktop và IDE extension của đúng người đang đăng nhập.
- Không đưa Hermes, OpenCode, LiteLLM hay một trang web nội bộ vào đường subscription.
- Không tự quy quota thành đô la khi thiếu log input/output theo model. Khi thiếu log thì ghi «chưa đo được».

## Hướng A — MCP chọn model trong Claude Code

Đúng luồng trong MCP.md. Người dùng gõ yêu cầu trong Claude Code. Plugin Mod nhận yêu cầu đầu phiên, Haiku chọn model, các lượt sau trong cùng phiên dùng model đó. Không mở app chat khác.

MCP server đứng một mình không đổi được model. Bản phase 1 là một plugin gồm Mod và MCP local. Claude Code phải từ **2.1.287** trở lên.

### Thành phần

Tất cả chạy trên máy người dùng. Không có server công ty.

```text
Claude Code (>= 2.1.287)
  plugin apero-route
    mods/route.mjs     nhận prompt đầu phiên, gọi Haiku, ghim model
    mcp/server.mjs     stdio, kiểm rule và tên model
    rules.json         bảng việc → model
```

Haiku được gọi bằng `$.model.complete` bên trong Claude Code, tính vào quota ghế của người đó. MCP không giữ API key và không gọi ra Anthropic.

Cài plugin từ marketplace nội bộ của công ty, pin đúng commit. Không cài plugin lạ. Mod chạy trong process Claude Code, đọc được file và secret trên máy; chỉ cài bản đã review.

### Rule

| Việc | Model trong phiên |
|---|---|
| Việc nhỏ, tìm kiếm, lọc log, tóm tắt | Haiku |
| Viết code và việc hằng ngày | Sonnet |
| Debug khó, sửa nhiều phần, thiết kế hệ thống | Opus |

Tên đưa vào CLI là alias `haiku`, `sonnet`, `opus` của bản Claude Code đang cài. Đối chiếu alias với model trong Gateway.md: Haiku 5.5, Sonnet 5.5, Opus 5.5. Phase 1 không chọn Fable.

Haiku chỉ chạy một lần, ở prompt người dùng đầu tiên của phiên. Input là câu yêu cầu (cắt còn tối đa khoảng 1.500 token), tên repo và tên nhánh. Không gửi mã nguồn, không gửi lịch sử. Output là JSON ngắn: `model`, `reason`. MCP kiểm `model` thuộc `haiku | sonnet | opus`. JSON hỏng, timeout hoặc model lạ thì ghim `sonnet` và hiện một dòng lý do trong phiên. Không đổi sang model khác mà không báo.

Các prompt sau trong cùng phiên không gọi lại Haiku. Phiên mới thì chọn lại. Lệnh `/route` in model đang ghim và lý do. `/route haiku|sonnet|opus` đổi model cho đến hết phiên.

Tên event và field lấy từ type của đúng bản Claude Code đang cài, rồi mới viết Mod. Hợp đồng cần giữ: phân loại một lần ở prompt đầu; mọi lượt model sau trong phiên dùng model đã ghim; lỗi thì về Sonnet và báo người dùng.

### Ghi chú và agent phụ

Cuối phiên, nếu việc chưa xong, Mod ghi một file ngắn trong repo: mục tiêu, model đã chọn, file đã sửa, kết quả kiểm tra nếu có, bước tiếp. Phiên sau chỉ đọc file đó khi người dùng nói tiếp đúng việc. Context gần đầy thì dùng lệnh nén sẵn của Claude Code, rồi giữ file ghi chú. Chỉ clear khi việc xong hoặc đổi việc.

Phase 1 tắt agent phụ. Mỗi agent phụ tốn thêm token và làm nhiễu số đo. Bật lại sau bốn tuần, từng việc độc lập, có trần số agent.

### Log

Một file jsonl trên máy người dùng, không có nội dung prompt:

- thời điểm, id phiên
- model đã ghim, lý do, lần này có phải fallback không
- số lần gọi Haiku trong phiên (đạt khi bằng 1)
- độ trễ của lần chọn
- model người dùng sửa bằng `/route`, nếu có

Token input/output của cả phiên lấy từ số Claude Code đã hiện. Không có số thì ghi «chưa đo được». Không nhân với giá API để ra «tiết kiệm được bao nhiêu» trong báo cáo tuần.

### Cách rollout

1. Hai người cài Claude Code 2.1.287+, đăng nhập ghế Team của chính họ, cài plugin pin commit.
2. Chạy bốn phiên thử: việc nhỏ phải ra Haiku, việc code phải ra Sonnet, việc thiết kế phải ra Opus, và một lần cố làm hỏng JSON của bộ chọn để thấy fallback Sonnet có dòng báo.
3. Phiên thứ hai trong cùng cuộc hội thoại không được phát sinh thêm lần gọi Haiku.
4. Đủ bốn ca thì cài cho đủ 10 người.
5. Bốn tuần sau mới xét ghế Premium.

### Đạt phase 1

- 10 người, 10 account, plugin cùng một commit.
- Mỗi phiên đúng một lần chọn model, có lý do hiện trong phiên.
- Fallback và `/route` đúng như trên.
- Một file mã nguồn có chuỗi mồi không xuất hiện trong input gửi Haiku.
- Không có process nào giữ API key Anthropic cho plugin này.

### Mua thêm cho 10 người

Mua ngay:

| Hạng mục | Số lượng | Giá | Tiền phase 1 |
|---|---:|---:|---:|
| Claude Team, ghế Standard, trả năm | 10 | $20/ghế/tháng | **$200/tháng** ($2.400/năm, khoảng ₫5,2 triệu/tháng) |
| Claude Code | theo ghế | $0 | $0 |
| Máy chủ, domain, GPU | không dùng | $0 | $0 |

Team tối thiểu 2 ghế. Trả tháng thì Standard là $25/ghế, cả team **$250/tháng**. Phase 1 chọn trả năm.

Mỗi ghế Standard kèm $20 API credit/tháng. 10 ghế ra $200, gộp một pool, trần pool $500. Credit này dùng cho Claude API / Console, **không** dùng cho Claude Code. Phase 1 không claim số credit này để chạy bộ chọn model.

Đã có 10 ghế Pro trả năm ($20 hoặc $200/năm) thì chuyển sang Team Standard trả năm cùng mặt bằng giá ghế, thêm một hóa đơn và trang quản trị. Pro trả tháng $20 sang Team trả tháng $25 thì thêm $50/tháng cho 10 người.

Chưa mua:

| Hạng mục | Khi nào mới mua |
|---|---|
| Ghế Premium ($100/ghế/tháng trả năm, $125 trả tháng) | Một người chạm hạn mức tuần hơn một lần trong hai tuần. Nâng đúng người đó. 10 Premium trả năm là $1.000/tháng, không mua sẵn |
| Usage bundle | Bật usage credits với trần cả org $100/tháng, số dư ban đầu $0. Lần chạm trần đầu mua bundle $50 (trả $45). Không mua bundle $250 hoặc $1.000 trong phase 1 |
| Claude Max 5x/20x từng cá nhân | Không dùng cho pilot 10 người. Team đã có admin và một hóa đơn |
| Enterprise ($20/người/tháng, cam kết năm, không kèm quota) | Mọi token tính giá API. Đắt hơn đường subscription của phase 1 |
| API key Anthropic trả trước | Bộ chọn chạy trên quota ghế. Key riêng chỉ xét sau phase 1 |
| GPU | Gateway.md: cụm 8×H100 chưa hòa vốn |

## Hướng B — Codex bằng subscription, qua gateway

Codex không có giá riêng. Phase 1 mua ChatGPT Business. Mỗi người đăng nhập ChatGPT của chính họ trên Codex. Gateway công ty chỉ chuyển request đó sang Codex của OpenAI, kèm token của đúng người đó. Hạn mức trừ vào ghế của người đó.

Đây là đường «Sign in with ChatGPT through a gateway» trong tài liệu Codex: client gửi `Authorization` là token ChatGPT của user; gateway chuyển nguyên header đó và `ChatGPT-Account-ID` tới `https://chatgpt.com/backend-api/codex`.

Đường này khác với API key. API key tính theo token, không ăn quota Codex. Credit API của gói Pro cũng không tăng quota Codex. Phase 1 không mua Pro để lấy credit.

### Thành phần

```text
Máy nhân viên
  Codex CLI / desktop / IDE
  đăng nhập ChatGPT Business của chính họ
  config bắt buộc trỏ model_provider = apero-gateway
        |
        |  POST .../responses
        |  Authorization: Bearer <token của user>
        |  ChatGPT-Account-ID: <workspace phase 1>
        v
Gateway nội bộ (một process, TLS, trong VPN)
  kiểm workspace, allowlist model, không ghi prompt, không lưu token
        |
        v
https://chatgpt.com/backend-api/codex
```

Một process proxy là đủ. Chưa đưa LiteLLM, 9router hay OmniRoute vào phase 1.

Proxy làm đúng các việc sau:

1. Chỉ nghe trong VPN hoặc dải IP công ty. Có TLS. Không mở ra internet công cộng.
2. Từ chối request thiếu `Authorization` hoặc thiếu `ChatGPT-Account-ID`.
3. `ChatGPT-Account-ID` phải đúng workspace phase 1. Sai thì 403, không sửa header rồi gửi tiếp.
4. Đọc tên model trong body. Ngoài allowlist thì 400, nêu tên model bị từ chối. Không đổi model hộ người dùng.
5. Chuyển tiếp stream SSE ngay, không chờ hết câu trả lời. Giữ event kết thúc `response.completed`.
6. Log mỗi request: thời điểm, account id, model, status, usage nếu event có usage. Không log `Authorization`, không log prompt, không log tool argument.
7. Không có API key OpenAI trên process này.

File cấu hình phát cho mọi máy, đặt trước bảng TOML đầu tiên:

```toml
model = "gpt-6.1-terra"
model_provider = "apero-gateway"

[model_providers.apero-gateway]
name = "Apero Gateway"
base_url = "https://gw.apero.internal/backend-api/codex"
wire_api = "responses"
requires_openai_auth = true
```

`base_url` và path xác nhận bằng một request thật trên Codex đang cài (máy này đang ở CLI 0.165.0) trước khi phát cấu hình. Tài liệu Codex yêu cầu gateway chuyển `/models` và `/responses` sang `https://chatgpt.com/backend-api/codex`, và giữ `Authorization` cùng `ChatGPT-Account-ID`.

Phát cấu hình theo thứ tự:

1. Thử requirements trên workspace Business (Codex managed config). Business nằm trong danh sách nguồn cloud requirements.
2. Trang đó không có trên workspace thì phát file hệ thống: Windows `%ProgramData%\OpenAI\Codex\requirements.toml`. Cùng nội dung. Người dùng không ghi đè được requirements.
3. Không mua Enterprise chỉ để có nút trên console. Access token tự động cho CI là hạng mục Enterprise. Phase 1 mỗi người đăng nhập trình duyệt một lần trên máy của họ.

### Model

Phase 1 không có bộ chọn Haiku. Codex không chạy Mod của Claude Code. Gắn Haiku vào gateway sẽ phải mua thêm API Claude. Để sau.

| Model | Phase 1 |
|---|---|
| `gpt-6.1-terra` | Mặc định cả team |
| `gpt-6-luna` | Được phép khi người dùng tự chọn |
| `gpt-6.1-sol` | Được phép khi người dùng tự chọn |
| `gpt-6-astra` | Gateway trả 400 |

Một model mặc định để bốn tuần đo cùng một mặt bằng. Astra có giá API $10 / $50 mỗi triệu token trong Gateway.md. Chặn ở gateway cho đến khi có người cần và được duyệt từng account.

### Việc gateway chưa làm

- Không cấp một API key công ty để app khác gọi hộ quota.
- Không nhận request của người A rồi gửi bằng token của người B.
- Không nhánh sang API key khi hết quota. Hết quota thì Codex hiện lỗi hạn mức của ghế đó. Người dùng dừng hoặc chờ reset.
- Không bot CI. Việc nền trên subscription cần người đó bật và là việc của chính họ.

### Cách rollout

1. Tạo workspace Business, mời đúng 10 email công ty, bật MFA. SSO công ty nếu đã có; chưa có thì chưa mua IdP mới.
2. Cài Codex bản đã chốt (hiện 0.165.0 trên Windows) bằng installer chính thức. Mỗi người đăng nhập ChatGPT, chọn đúng workspace.
3. Dựng proxy trên một máy công ty đã có. Chưa có máy thì một VPS nhỏ trong VPN là đủ. Chưa cần GPU.
4. Một người chạy năm kiểm tra, xong mới phát cấu hình.
5. Mỗi người chạy một prompt thử. Log phải có 10 account id khác nhau.
6. Bốn tuần giữ allowlist. Hết tuần 4 mới xét ghế Premium và có bật API fallback hay không.

Năm kiểm tra, lấy từ checklist gateway của Codex:

| Kiểm tra | Đạt khi |
|---|---|
| Kết nối | `/status` hiện provider `apero-gateway` và model `gpt-6.1-terra`. Prompt ngắn có chữ trả về |
| Stream | Chữ hiện dần. Stream kết thúc bằng `response.completed` |
| Tool local | Trong thư mục thử, Codex liệt kê file và tóm tắt, không sửa file |
| Lượt sau | Câu hỏi tiếp trong cùng thread dùng được nội dung lượt trước |
| Lỗi | Model `gpt-6-astra` bị 400, message nêu rõ model. Request hợp lệ của người khác vẫn chạy |
| Log | Dòng log có account id và model, không có chuỗi `Bearer` |

### Đạt phase 1

- 10 người đăng nhập 10 ghế, mọi request Codex đi qua proxy, upstream là Codex ChatGPT.
- Astra không đi qua.
- Rút một người khỏi workspace thì request kế tiếp của người đó bị từ chối, chín người còn lại vẫn dùng được.
- Bốn tuần không có API key OpenAI nào gắn với proxy.

### Mua thêm cho 10 người

Mua ngay:

| Hạng mục | Số lượng | Giá | Tiền phase 1 |
|---|---:|---:|---:|
| ChatGPT Business, ghế Standard, trả năm | 10 | $20/ghế/tháng | **$200/tháng** ($2.400/năm, khoảng ₫5,2 triệu/tháng) |
| Codex CLI / app / IDE | theo ghế | $0 | $0 |
| Máy gateway | 1 máy nội bộ sẵn có | $0 | $0 |
| TLS | chứng chỉ nội bộ hoặc Let's Encrypt | $0 | $0 |

Business tối thiểu 2 người. Trả tháng thì Standard là $25/ghế, cả team **$250/tháng**. Phase 1 chọn trả năm.

Ghế Standard dùng Codex trên desktop, CLI và IDE, có SSO/MFA, mặc định không dùng dữ liệu business để train. Hạn mức theo kiểu Plus, có cửa sổ năm giờ. Free và Go ($0 và $8) không đủ: Codex của hai gói đó nằm ở desktop và không phải đường CLI của phase 1. Plus lẻ $20/người có CLI nhưng không có workspace, SSO và một hóa đơn. Phase 1 không mua 10 Plus.

Chưa có máy nội bộ để đặt proxy thì thêm một VPS nhỏ, khoảng $5–20/tháng. Đó là khoản duy nhất ngoài ghế.

Chưa mua:

| Hạng mục | Khi nào mới mua |
|---|---|
| Ghế Business Premium ($100/ghế/tháng trả năm, $125 trả tháng) | Một người bị cửa sổ năm giờ chặn việc lặp lại trong hai tuần. Nâng đúng người đó. Premium được khoảng 5 lần usage ghế Standard và không có cửa sổ năm giờ. Ngày 29-10-2026 OpenAI tăng usage Work/Codex trên Premium. Không lấy con số «gấp bao nhiêu token» làm cam kết |
| Credit dùng thêm của workspace | Bật trần, số dư $0. Lần hết quota đầu tiên nạp tối đa $50 cho cả workspace, có trần từng ghế |
| ChatGPT Pro $100 / $200 / $500 | Credit API của Pro không tăng quota Codex. Không mua Pro cho 10 người |
| Codex-only trả theo token trên Business | Ghế mới kiểu này ngừng từ 24-06-2026 |
| Enterprise | Chỉ để lấy access token cho CI hoặc nút console. Phase 1 không cần |
| OpenAI API, nạp sẵn | Công tắc fallback để tắt trong bốn tuần. Khi bật sau phase 1: một project, trần cứng $100/tháng, cảnh báo 50/80/100%, và người dùng thấy rõ request đó đang tính tiền API |
| GPU | Chưa hòa vốn ở quy mô này |

## Chọn hướng nào

| | Hướng A — MCP | Hướng B — Codex subscription |
|---|---|---|
| Người dùng ở đâu | Claude Code | Codex CLI, app, IDE |
| Ai chọn model | Haiku, một lần mỗi phiên, theo rule | Cả team mặc định Terra. Người dùng tự đổi Luna hoặc Sol. Astra bị chặn |
| Tiền ghế | $200/tháng trả năm | $200/tháng trả năm |
| Máy chủ | Không | Một proxy trong VPN |
| App khác gọi vào | Không có cổng | Không có cổng |
| Đo tiết kiệm | Được nếu có log token theo model | Quota Codex chưa có bảng quy đổi. Thiếu log thì ghi «chưa đo được» |

Team đang làm việc chính trong Claude Code thì làm hướng A: hết tiền ở ghế, không thêm máy. Team đang làm việc chính trong Codex thì làm hướng B: thêm một proxy, ghế cùng mức tiền.

Không mua 10 ghế Claude và 10 ghế ChatGPT cho cùng phase 1. Đó là $400/tháng trước khi biết hướng nào được dùng.

## Bốn tuần đo

Mỗi tuần một dòng cho cả team:

- số người dùng thực sự
- số phiên
- phân bố model
- số lần fallback (hướng A) hoặc số lần 400 vì model bị cấm (hướng B)
- số người chạm hạn mức
- token input/output theo model, hoặc «chưa đo được»

Hết tuần 4 mới quyết: giữ nguyên 10 ghế Standard, nâng từng người sang Premium, hoặc bật API có trần $100/tháng. Chưa hòa vốn thì chưa bàn GPU. Mốc 100 người trong Gateway.md vẫn là subscription từng người và API có trần, không đổi vì phase 1.

## Nguồn

- [Gateway.md](Gateway.md) — thứ tự subscription, giá API, giá ghế Claude Team và ChatGPT, ghi chú quota Codex chưa quy đổi được. 29-10-2026
- [MCP.md](MCP.md) — Mod + MCP, rule Haiku/Sonnet/Opus, fallback, ghi chú, agent phụ
- [Claude Code Mods](https://code.claude.com/docs/en/plugins/mods/overview) · [Events](https://code.claude.com/docs/en/plugins/mods/events) · [Mods API](https://code.claude.com/docs/en/plugins/mods/api)
- [Claude Team](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) — Standard $25 hoặc $20/năm, Premium $125 hoặc $100/năm, Claude Code gồm trong ghế
- [API credit Team/Max](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans) — credit không dùng cho Claude Code
- [Codex authentication](https://developers.openai.com/codex/auth) — ChatGPT cho subscription, API key cho tính token
- [Connect to a gateway](https://developers.openai.com/codex/enterprise/connect-to-a-gateway) — forward token ChatGPT của từng user
- [Roll out a gateway](https://developers.openai.com/codex/enterprise/roll-out-a-gateway) · [Gateway compatibility](https://developers.openai.com/codex/enterprise/gateway-compatibility)
- [Sign in with ChatGPT Terms](https://openai.com/policies/sign-in-with-chatgpt-terms/) — 29-09-2026. Request của từng user, không biến plan thành API dùng chung, không để người này gọi bằng ghế của người khác
- [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration) — requirements cloud trên Business và Enterprise, file hệ thống khi không có trang cloud
