# Spec triển khai `wandura-gateway`: MCP và Codex Apply

- **Phạm vi:** Phase 1, tối đa 10 người dùng nội bộ Wandura
- **Ngày lập:** 29-10-2026
- **Trạng thái:** Bản spec để chốt triển khai và ngân sách
- **Bản HTML:** [7.Spec triển khai MCP và Codex Apply Phase 1.html](7.Spec%20triển%20khai%20MCP%20và%20Codex%20Apply%20Phase%201.html)

## 1. Tóm tắt quyết định

Hai hướng phục vụ hai nhu cầu khác nhau:

| Hướng | Dùng khi | Tác động lên repo |
|---|---|---|
| **MCP** | Nhân viên muốn gọi công cụ Gateway/Wandura ngay trong Codex, Claude Code hoặc client có MCP | Agent gọi các tool đã cấp quyền; MCP tự nó không đổi model chính của Codex |
| **Responses API `apply_patch`** | Muốn có workflow trong `wandura-gateway` nhận yêu cầu sửa code, tạo diff, áp dụng vào worktree và trả diff để review | Gateway tự quản lý context, patch harness, sandbox, phê duyệt và chi phí API |

**Khuyến nghị cho 10 người:** triển khai MCP trước nếu mục tiêu là đưa công cụ Wandura vào quy trình làm việc của nhân viên. Dùng `apply_patch` khi đã xác định cần sản phẩm sửa code trực tiếp trên repo. Không cần GPU riêng cho cả hai hướng.

**Định nghĩa trong tài liệu này:** “Codex Apply” là `apply_patch` tool của Responses API, không phải một endpoint tên `codex apply`. Tool trả về thao tác tạo/sửa/xóa file; ứng dụng của `wandura-gateway` chịu trách nhiệm áp dụng diff vào một môi trường giới hạn.

**MCP và HTML là hai giao diện sử dụng; Codex Apply là một backend xử lý code.** Vì vậy Apply có thể được gọi bằng tool MCP hoặc bằng nút/form trong HTML. Cả hai giao diện phải gọi cùng Gateway Core để dùng chung xác thực, policy, budget và audit; không tạo hai luồng ghi repo độc lập.

```text
Codex / Claude ── MCP adapter ──┐
                                ├── Gateway Core ── Wandura API / OpenAI Responses API
HTML app ─────── REST/BFF ──────┘
```

## 2. Giả định và phần cần đối chiếu với repo

Trong workspace hiện tại chưa có checkout hoặc source tree tên `wandura-gateway`; vì vậy các module bên dưới là ranh giới triển khai đề xuất, chưa gắn với file cụ thể của repo. Khi đưa vào repo thật, giữ nguyên cấu trúc package/framework đang dùng và map các module theo trách nhiệm.

Giả định phase 1:

- Tối đa 10 người, xác thực bằng danh tính Wandura; không chia sẻ tài khoản hoặc API key giữa người dùng.
- Một org/project để quản lý giới hạn chi tiêu, có thể gắn usage với từng user.
- Dùng provider cloud hiện có; không tự host model ở phase 1.
- Có thể tái sử dụng auth, database, logging, CI và môi trường deploy hiện có. Chỉ mua thêm các dịch vụ nếu repo chưa có những thành phần đó.
- Nếu mục tiêu cụ thể là tạo video/ảnh/audio bằng sản phẩm Wandura, ưu tiên MCP Wandura chính thức đang có. Không viết lại API/MCP client trong `wandura-gateway` nếu chỉ cần kết nối client.

## 3. Hướng A — MCP cho công cụ Gateway/Wandura

### 3.1 Mục tiêu

Đưa các thao tác có kiểm soát vào AI client của nhân viên. Với use case sáng tạo nội dung, MCP Wandura hiện có thể tìm template/model, xem giá trước khi chạy, tạo job và lấy kết quả. MCP chính thức dùng URL `https://www.wandura.ai/api/mcp`; CLI cài qua `@wandura/cli` và MCP local qua `@wandura/mcp`.

Phân biệt hai sản phẩm khi triển khai: MCP public cho user sign-in dùng credits trên website; API v2 server-to-server dùng API key/product wallet và là sản phẩm API riêng. Không giả định credits của gói Basic/Growth thanh toán được API v2. Nếu cần backend Gateway gọi API v2, phải xin quyền/API key và báo giá phù hợp.

Với use case model routing trong Claude Code, cần một **Claude Code Mod** bắt sự kiện model request và một Gateway route service. MCP server thông thường chỉ cung cấp tools; nó không đổi model chính đang xử lý prompt. Codex dùng MCP để gọi tools, còn model Codex được chọn trong cấu hình/client.

### 3.2 Thành phần

1. **Gateway Core**
   - Danh mục model/provider được phép dùng.
   - Policy theo user/team: model allowlist, mức chi tiêu, giới hạn tốc độ và loại task.
   - Route decision theo rule ban đầu; có thể thêm classifier model sau khi đo được độ chính xác và chi phí.
   - Ghi usage metadata, không ghi prompt hoặc source code thô mặc định.

2. **MCP adapter**
   - Xác thực người dùng theo OAuth/session hiện có.
   - Chỉ expose các tool cần cho phase 1:

| Tool | Input | Chức năng | Quyền |
|---|---|---|---|
| `gateway_list_models` | `task_type?` | Trả model được phép dùng và thuộc tính cơ bản | Read |
| `gateway_route_preview` | `task_summary`, `repo_tags[]`, `max_cost_usd?` | Đề xuất route, model, lý do và cost band | Read |
| `gateway_usage_summary` | `period` | Usage của chính user; admin xem tổng team | Read |
| `code_task_preview` | `repo_id`, `base_ref`, `task`, `allowed_paths[]` | Trả `preview_id` và ước tính context/cost; chưa gọi model, chưa tạo branch | Read |
| `code_task_start` | `preview_id`, `max_cost_usd`, `idempotency_key` | Sau khi user duyệt preview trong client, gửi task cho isolated Apply worker | Write, tiêu API budget |
| `code_task_get` | `task_id` | Trạng thái, usage, diff và kết quả checks | Read |
| `code_task_approve` | `task_id`, `approval_id` | Tạo branch/PR draft sau khi user duyệt diff; backend xác minh approval token | Write |
| `code_task_cancel` | `task_id` | Hủy job còn chạy | Write |
| `wandura_preview_job` | `style/model`, `inputs`, `end_user_id` | Lấy giá trước khi tạo ảnh/video/audio | Read, không trừ credit |
| `wandura_create_job` | `preview_id`, `inputs`, `idempotency_key` | Gửi job sau khi user xác nhận giá | Write, tiêu credit |
| `wandura_get_job` | `job_id` | Trạng thái và URL kết quả | Read |

   - Không expose tool tổng quát như `run_shell`, không trả API key trong tool result, không cho agent tự tăng hạn mức.
   - Với thao tác tốn credit, yêu cầu `preview` trước `create/start`; cấu hình MCP host yêu cầu người dùng duyệt write tool, và backend kiểm tra `preview_id`, hạn mức cùng idempotency key.

   Các tool `gateway_*`/`wandura_*` ở bảng trên là contract đề xuất nếu `wandura-gateway` tự triển khai adapter; đây không phải tên tool đảm bảo của MCP public. Khi dùng MCP public thì dùng tool list do server gửi, hiện gồm các luồng như `search_templates` → `preview_generation` → `clone_template`, hoặc `preview_render` → `render_video`/`render_image`/`render_audio` → `get_generation`.

3. **Claude Code Mod (chỉ nếu cần tự chọn model trong Claude Code)**
   - `turn.step` gọi `POST /v1/route` với prompt summary ngắn, repo tags và allowlist model.
   - Mod chuyển model đã chọn vào event trước khi gọi tiếp model; giữ streaming và usage event.
   - Nếu route service lỗi, giữ model hiện tại hoặc báo user chọn lại; không âm thầm chuyển sang provider tính phí khác.
   - Không gửi toàn bộ repo để phân loại task. Bản đầu dùng rules và tối đa một câu tóm tắt task.
   - Cần pin và kiểm tra phiên bản Claude Code hiện hành. Tài liệu Mod hiện mô tả `turn.step` và khả năng gửi request sang model khác; alias model cần phiên bản xử lý alias tương ứng hoặc phải dùng model ID đầy đủ.

### 3.3 Contract gợi ý cho route service

`POST /v1/route`

```json
{
  "task_summary": "Fix the timeout handling in job polling",
  "repo_tags": ["typescript", "backend", "wandura-gateway"],
  "available_model_ids": ["claude-sonnet", "claude-opus"],
  "max_cost_usd": 0.50
}
```

Trả về:

```json
{
  "route_id": "rt_...",
  "model_id": "claude-sonnet",
  "reason_code": "routine_code_change",
  "estimated_cost_usd": 0.12,
  "fallback": "keep_current_model"
}
```

`user_id` lấy từ token đã xác thực, không nhận từ body. `route_id` dùng nối với usage event. Không nhận API key/model provider key do client gửi.

### 3.4 Luồng MCP

1. User đăng nhập bằng tài khoản cá nhân; MCP nhận token riêng của user.
2. Client gọi tool chỉ khi cần. Tool kiểm tra quyền, org/project, ngân sách và schema đầu vào.
3. Với media job, MCP gọi preview trước; hiển thị giá; chỉ submit sau khi user duyệt.
4. Ghi audit event gồm user, tool, job ID, credits, trạng thái và request ID; không lưu nội dung nhạy cảm không cần thiết.
5. Job chạy bất đồng bộ; client poll trạng thái hoặc nhận callback/webhook đã ký.

### 3.5 Các module đề xuất trong `wandura-gateway`

- `gateway-core`: catalog, policy, route decision.
- `mcp-adapter`: tool schemas, auth, MCP transport.
- `wandura-client`: API v2 client, idempotency, polling, chữ ký webhook.
- `usage-ledger`: usage theo user/project và audit.
- `claude-mod` (nếu cần): plugin/Mod ở repo hoặc marketplace nội bộ; không đặt provider secrets ở client.

### 3.6 Hạn chế và bảo mật

- MCP không thay model chính của Codex. Tool `gateway_route_preview` chỉ trả đề xuất; Codex có thể chọn model/tool dựa theo prompt. Muốn đổi model của Claude Code theo từng request phải dùng Mod.
- MCP local chạy trên máy từng nhân viên thì không cần public server cho phần transport; MCP remote/ChatGPT cần endpoint HTTPS và auth phù hợp.
- API key Wandura/OpenAI chỉ nằm ở backend hoặc secret manager; log đã redact token, email và URL có chữ ký.
- Dùng allowlist tool, rate limit, per-user spend cap và audit. Không cho phép agent tự phê duyệt chi phí hoặc đổi budget.

### 3.7 Giao diện HTML cho phase 1

HTML là app nội bộ để nhân viên không cần MCP client. Browser chỉ gọi REST/BFF của `wandura-gateway`; không giữ OpenAI/Wandura key và không gọi provider trực tiếp.

**Màn hình tối thiểu:**

1. Đăng nhập qua OIDC/SSO hiện có.
2. Tạo task: chọn media job hoặc code task, nhập yêu cầu, repo/style/model và mức chi tối đa.
3. Preview: hiển thị giá Wandura hoặc ước tính API trước khi submit.
4. Task list/detail: trạng thái queued/running/done/failed, usage, lỗi đã redact và link kết quả.
5. Review: preview asset hoặc diff code; approve trước khi tạo job tính credit hoặc branch/PR.
6. Admin usage: tổng theo user/project, budget và cảnh báo.

**REST/BFF gợi ý:** reuse `POST/GET /v1/code/tasks` cho Apply; thêm `POST /v1/media/preview`, `POST /v1/media/jobs`, `GET /v1/media/jobs/{id}` và `GET /v1/usage`. Browser gửi session cookie có CSRF protection; service validate schema/quyền/limit rồi gọi provider. Dùng signed upload/download URL cho file; không proxy file lớn qua browser logs.

**Vận hành:** reuse hosting, database, SSO, domain/TLS và secret manager hiện có. Nếu thiếu, phase 1 cần 1 web runtime khoảng 1–2 vCPU/2–4 GB RAM, 1 Postgres nhỏ khoảng 1 vCPU/2 GB với backup, queue nhẹ (có thể dùng Postgres), secret store và 1 worker pool giới hạn 1–2 job đồng thời. Mỗi Apply job chạy trong container/worktree cô lập khoảng 2 vCPU/4 GB RAM; tăng concurrency thì tăng worker capacity. Chốt SKU/cloud price sau khi repo và cloud account được xác định. Không cần GPU.

## 4. Hướng B — Responses API `apply_patch` cho sửa repo

### 4.1 Mục tiêu

Thêm vào `wandura-gateway` một workflow coding có thể tạo thay đổi ở branch/worktree riêng, áp diff, chạy kiểm tra sẵn có và trả kết quả để người dùng duyệt. Không tự merge hoặc deploy trong phase 1.

### 4.2 Thành phần

1. **Task API**

| Endpoint | Chức năng |
|---|---|
| `POST /v1/code/tasks` | Tạo task; nhận repo, base SHA/ref, yêu cầu, allowlist path và mức chi tối đa |
| `GET /v1/code/tasks/{id}` | Trạng thái, usage, model, bản tóm tắt và diff đã tạo |
| `POST /v1/code/tasks/{id}/approve` | Xác nhận lưu kết quả thành branch/PR draft |
| `POST /v1/code/tasks/{id}/cancel` | Hủy task còn chạy |

Ví dụ input:

```json
{
  "repo_id": "wandura-gateway",
  "base_ref": "main",
  "task": "Add retry-after support to the jobs client",
  "allowed_paths": ["src/**", "docs/**"],
  "max_cost_usd": 0.50,
  "idempotency_key": "user-123:ticket-456"
}
```

2. **Worker cô lập theo task**
   - Tạo worktree/container mới tại commit đã pin; không dùng chung working tree giữa user.
   - Context builder chỉ lấy file liên quan, hướng dẫn repo và cấu hình build; bỏ `.env`, credentials, artifacts, `node_modules`, build output và file không trong allowlist.
   - Phase 1 không cấp tool shell cho model. Chỉ cấp `apply_patch`; worker chạy các lệnh kiểm tra đã allowlist sau khi áp patch.
   - Sau khi patch và kiểm tra trong scratch worktree, UI hiển thị diff. Chỉ khi user duyệt mới tạo branch/PR draft.

3. **Responses API client**
   - Gửi `tools: [{"type":"apply_patch"}]`, cùng context chọn lọc.
   - Phase 1 pin `gpt-5.5`, model được liệt kê rõ trong bảng tương thích của tài liệu Apply Patch. Giữ model ID trong cấu hình để đổi sau khi kiểm tra lại tài liệu và smoke run.
   - Với mỗi `apply_patch_call`: validate path, áp operation vào scratch worktree, ghi status và trả đúng một `apply_patch_call_output` theo `call_id`.
   - Tiếp tục bằng `previous_response_id` và tool output; giới hạn vòng sửa lại ở tối đa 4 lượt trong phase 1.

4. **Patch harness**
   - Chỉ nhận `create_file`, `update_file`, `delete_file`.
   - Từ chối path tuyệt đối, `..`, symlink thoát workspace, path ngoài allowlist, file quá lớn, thay đổi binary, và thay đổi secret/config nhạy cảm.
   - Kiểm tra SHA/base ref trước khi commit để phát hiện repo thay đổi giữa lúc tạo task và lúc duyệt.
   - Áp dụng atomic trên scratch branch; nếu một operation hỏng thì trả lỗi operation đó và không ghi dở lên branch người dùng.
   - Không commit/merge/push tự động; phase 1 tạo diff/PR draft để reviewer xem.

### 4.3 Luồng xử lý

1. Xác thực user, kiểm tra quyền repo, giới hạn chi và idempotency.
2. Pin base commit; tạo isolated worktree và context manifest.
3. Gọi Responses API; nhận patch operations.
4. Validate và áp patch vào scratch worktree; trả tool output để model sửa tiếp nếu có lỗi.
5. Chạy formatter/linter/typecheck/test commands đã allowlist trong sandbox.
6. Ghi kết quả, diff stat, token usage, cost và log kiểm tra; redact secrets.
7. User review diff; duyệt mới tạo branch/PR draft. Không tự merge.

### 4.4 Dữ liệu và vận hành

Lưu tối thiểu: `task_id`, `user_id`, `repo_id`, `base_sha`, `status`, `response_id`, `model_id`, token usage, estimated/final cost, diff hash, timestamps và kết quả kiểm tra. Mặc định không lưu prompt đầy đủ hoặc snapshot source quá thời hạn vận hành đã được công ty duyệt.

Mỗi task có per-user hard budget nội bộ và giới hạn số file/bytes/turns. OpenAI project hard spend limit là lớp bảo vệ bổ sung; giới hạn ở dashboard có thể vượt nhẹ do độ trễ ghi nhận.

## 5. Mua sắm cho phase 1 — 10 người

Giá dưới đây là USD trước thuế; Wandura hiển thị credit theo USD. Chỉ tính khoản mua mới nếu nhóm chưa có license hoặc credit phù hợp.

### 5.1 Hướng MCP

| Hạng mục | Số lượng/giá tham chiếu | Ghi chú |
|---|---:|---|
| Codex host có MCP, nếu chọn Codex làm client | 10 ChatGPT Business Standard: **$250/tháng** trả tháng; hoặc **$200/tháng tương đương** khi trả năm (**$2,400 trả trước/năm**) | Business Standard hiện gồm Codex. Nếu 10 người đã có Codex/client license phù hợp thì không mua thêm; Claude Code/Cursor có license riêng. |
| Wandura Basic cho user cá nhân | 10 × **$15/tháng = $150/tháng**, tổng 15,000 credits/tháng | Chỉ áp dụng nếu dùng MCP public sign-in theo account/credits website. Mỗi Basic gồm 1,500 credits; reset theo kỳ, không rollover; không coi là credit pool dùng chung. |
| Wandura API/team workspace | **Báo giá Enterprise** | Dùng cho API v2 server-to-server hoặc khi cần team workspace, SSO/SAML, full API access, credit volume tùy chỉnh. Hỏi sales; không cộng đồng thời 10 Basic nếu Enterprise thay thế các account đó. |
| Hosting MCP nội bộ | **$0 thêm** nếu dùng MCP Wandura chính thức/local và hạ tầng sẵn có | Nếu tự host remote MCP để ChatGPT truy cập, dùng app service/HTTPS/auth hiện có; nếu chưa có thì lấy báo giá theo cloud hiện hành. |
| GPU | **Không mua** | Dùng service cloud; 10 người không cần cụm GPU riêng cho MCP. |

**Ngân sách tham chiếu cho MCP public + Codex:** $400/tháng nếu trả tháng cho 10 Business seats và 10 Basic; hoặc $350/tháng tương đương khi trả năm cho Business ($2,400/năm thanh toán trước) cộng $150/tháng Wandura. Nếu đã có ChatGPT seats, phần mua mới còn $150/tháng. Nếu chỉ dùng Codex MCP tool cho code, không cần mua Wandura Basic; nếu chỉ dùng public Wandura MCP trong client đã có, không cần mua thêm hosting MCP. Thuế/đơn giá theo quốc gia có thể khác.

**Nếu MCP dùng cho Claude Code model routing:** Claude Code cần seat có quyền dùng Claude Code. Team Standard không gồm Claude Code; Team/Enterprise Premium mới có. Dùng Pro/Max theo từng user hoặc xin giá Premium hiện trong admin console. Tài liệu giá nội bộ ngày 29-10 ghi Premium $125/user/tháng hoặc $100/user/tháng khi trả năm; xác nhận lại ngay trước khi mua vì giá/entitlement theo vùng và loại workspace có thể đổi.

### 5.2 Hướng HTML app

| Hạng mục | Mua/cấp cho 10 người | Ghi chú |
|---|---|---|
| SSO/Identity | Dùng Wandura Google Workspace/Microsoft Entra/OIDC hiện có | Không mua seat auth mới nếu đã có IdP. Nếu chưa có, chọn IdP trước khi chốt giá; HTML không dùng chung tài khoản. |
| Web app + BFF | Reuse app platform hiện có; nếu chưa có thì cấp 1 web runtime nhỏ | HTML không thay thế backend. BFF giữ secrets, gọi Wandura/OpenAI và áp quyền. Chi phí tùy cloud hiện có; chưa thể chốt SKU khi source/deploy repo chưa có trong workspace. |
| DB + task queue | Reuse Postgres/queue hiện tại; nếu chưa có, thêm managed DB nhỏ và queue/job runner | Lưu task/status/usage; giữ hạn mức và xử lý job media/code bất đồng bộ. |
| Secret manager, domain/TLS, logs | Reuse dịch vụ nội bộ; nếu chưa có thì tạo các resource tối thiểu trên cùng cloud account | Không lưu key trong HTML, local storage hoặc source repo. |
| Codex/ChatGPT seats | **Không bắt buộc** nếu 10 người dùng HTML app | Mua 10 Business seats chỉ khi họ cũng cần dùng Codex/ChatGPT client; giá ở mục MCP. |
| Wandura access | MCP public credits không cấp API access cho BFF | HTML gọi media API v2 server-to-server cần API access/live wallet theo Enterprise quote; nếu chưa mua API access, HTML chỉ có thể mở/link sang website Wandura, không gọi MCP public trực tiếp như một browser REST API. |

**Nếu company có sẵn app platform + IdP + Postgres + secret manager:** chi phí hạ tầng tăng thêm có thể bằng $0; chỉ trả provider usage/credits. **Nếu chưa có:** mua/cấp một web runtime, database nhỏ, queue/worker, secret store và DNS/TLS; chưa gán giá USD vì chưa biết cloud account, stack và service tier của repo. Không mua GPU.

### 5.3 Engine API Codex Apply (dùng từ MCP hoặc HTML)

| Hạng mục | Số lượng/giá tham chiếu | Ghi chú |
|---|---:|---|
| OpenAI API organization/project + service account/key | 1 project dùng riêng cho `wandura-gateway` | Một project cho phase 1; key đặt server-side trong secret manager. API tính riêng với ChatGPT subscription. |
| API budget ban đầu | **Đặt hard limit $100/tháng**, cảnh báo ở 50%, 80%, 100% | Bên trong app vẫn cần per-user/task hard cap; limit của provider có thể vượt nhẹ do độ trễ thống kê. |
| Model `gpt-5.5` | **$5/1M input tokens, $30/1M output tokens** | `apply_patch` có thể phát sinh nhiều lượt API do áp patch và gửi kết quả để model sửa tiếp. |
| Runtime/worker | Dùng hạ tầng hiện tại nếu có; nếu thiếu thì mua một worker CPU có sandbox/worktree | Không cần GPU; giá phụ thuộc cloud và stack của repo nên chốt sau khi thấy source/deploy hiện tại. |
| ChatGPT Business/Codex seats | **Không bắt buộc** nếu nhân viên thao tác qua UI HTML của `wandura-gateway` | Nếu gọi Apply bằng MCP từ Codex: cần quyền dùng Codex ở client; ví dụ 10 Standard seats là $250/tháng hoặc tương đương $200/tháng khi trả năm. ChatGPT Business không bao gồm API usage. |
| Wandura credits | **Không phát sinh từ `apply_patch`** | Chỉ mua nếu cùng workflow còn gọi Wandura để tạo ảnh/video/audio. |

**Ước tính workload để đặt mức $100:** giả sử mỗi người làm 20 task/tháng, mỗi task trung bình 40k input + 8k output, tổng 200 task/tháng. Với giá `gpt-5.5`, chi phí mẫu là khoảng **$88/tháng** trước retries/long-context. Đây là dự toán ban đầu, không phải cam kết; đo token thực tế trong tuần đầu rồi điều chỉnh. Nếu task vượt ngưỡng context dài hoặc cần nhiều lượt sửa, chi phí tăng.

**Hai cách dùng cùng engine:**

- **MCP → `code_task_start/get/approve`:** mua Codex client seats nếu dùng Codex; cộng OpenAI API usage $100 budget; cần Gateway worker. MCP host yêu cầu duyệt write tools; worker giữ quyền repo, model không nhận credential GitHub.
- **HTML → `/v1/code/tasks`:** không cần Codex seats; vẫn mua OpenAI API budget và cần cùng worker. HTML hiển thị trạng thái/diff/approve qua REST/BFF.

Nếu media generation cũng nằm trong HTML hoặc MCP adapter, Wandura API access/credits là khoản riêng; không gộp vào ngân sách OpenAI API.

### 5.4 Tổng hợp ngân sách mua thêm

| Kịch bản phase 1 | Chi phí dịch vụ AI tham chiếu | Hạ tầng/seat cần có |
|---|---:|---|
| **MCP public Wandura + Codex client** | $150/tháng Wandura Basic + $200/mo tương đương ChatGPT Business annual (hoặc $250 nếu trả tháng); tổng $350/$400 | Không cần tự host MCP; dùng SSO/client/hosting hiện có. |
| **MCP cho code, Apply worker phía Gateway** | OpenAI API đặt $100/tháng; thêm Codex seats chỉ nếu nhân viên dùng Codex làm host | Gateway worker/container + repo integration; 10 Business seats nếu chưa có Codex access. Không cần Wandura credits. |
| **HTML media app gọi Wandura API v2** | Wandura Enterprise/API access và live credit: báo giá | Web runtime + BFF + DB/queue + secrets + SSO; reuse hạ tầng nếu đã có. Không cần Codex seats. |
| **HTML code app gọi Apply** | OpenAI API đặt $100/tháng; mức mẫu $88/tháng theo workload ở trên | Web runtime + isolated worker + DB/queue + secrets + SSO; không cần Codex seats. Không cần Wandura credits. |

Nếu bật **cả MCP và HTML**, dùng chung Gateway Core, OpenAI project, Wandura API/wallet, DB và worker. Chỉ cộng chi phí của giao diện MCP seats (nếu cần Codex/Claude) và HTML hosting/resources còn thiếu; không nhân đôi provider budget.

### 5.5 Khoản không mua trong cả hai hướng

- Không mua máy 8×H100 hoặc GPU local cho phase 1.
- Không mua API key cá nhân cho từng nhân viên nếu service đã dùng project key phía server; thay vào đó gắn `user_id` và áp hạn mức trong Gateway.
- Không mua thêm model API chỉ để dùng MCP Wandura chính thức nếu use case chỉ gọi Wandura MCP bằng tài khoản/credits Wandura.

## 6. Bảng chọn nhanh

| Tiêu chí | MCP | API `apply_patch` |
|---|---|---|
| Dùng ngay trong agent client | Có | Cần UI/API workflow của Gateway hoặc Codex client gọi service |
| Dùng công cụ Wandura media | Phù hợp; MCP chính thức đã có | Không thuộc phạm vi của patch tool |
| Sửa trực tiếp file repo | Chỉ khi client đã có file tools và quyền local | Có; Gateway tự áp patch trong worktree giới hạn |
| Tự đổi model | Không với MCP thuần; Claude Code cần Mod; Codex giữ model client chọn | Chọn model ở Responses API request |
| Tài khoản/chi phí | License client + Wandura credits/API access theo use case | OpenAI API token usage; không cần ChatGPT seat nếu có UI riêng |
| Công sức vận hành | Thấp đến vừa; auth/tool policy | Vừa đến cao; worker, worktree, patch harness và review |

## 7. Kế hoạch triển khai

### Phase 1A — Gateway Core và xác thực

1. Map Gateway Core vào auth/database/deploy hiện hữu và tạo usage ledger, user-level limit, audit event.
2. Tạo một project OpenAI riêng và secret store nếu có Apply; giới hạn repo/org Wandura theo phạm vi pilot.
3. Chốt client và quyền Wandura: personal MCP credits hoặc Enterprise API wallet.

### Phase 1B — MCP pilot (10 người)

1. Cấu hình MCP trong Codex/Claude client theo user scope; bắt đầu bằng read-only tools.
2. Bật media preview hoặc `code_task_preview`; xác nhận trước mọi tool call tính phí.
3. Chỉ thêm write tools sau khi metering, idempotency và revoke access hoạt động.
4. Nếu cần model routing trong Claude Code, triển khai Mod riêng; Codex MCP không đổi model chính.

### Phase 1C — HTML pilot (10 người)

1. Dùng IdP Wandura hiện có; thêm web app/BFF, task list, preview và usage view.
2. Reuse chung REST/service layer với MCP; không cất provider key hoặc xử lý quyền ở browser.
3. Thêm trạng thái job, asset preview/diff review, explicit approve, audit và per-user limit.
4. Chỉ mua thêm web runtime/DB/queue/secret resources nếu hạ tầng hiện có chưa đáp ứng.

### Phase 1D — Codex Apply pilot

1. Cấu hình API project/model allowlist, server key và $100 hard spend limit.
2. Tạo isolated worker/worktree; gắn repo bằng GitHub App quyền tối thiểu cho `wandura-gateway`.
3. Tích hợp Responses API + `apply_patch`; giới hạn path và không cấp shell cho model.
4. Hiển thị diff/checks ở MCP tool result hoặc HTML; chỉ tạo PR draft sau khi user duyệt.
5. Pilot với 2–3 kỹ sư trước, sau khi đạt tiêu chí mới mở cho đủ 10 người.

### Tiêu chí chấp nhận

- MCP: 10 user đăng nhập riêng; tool catalog/usage hoạt động; mọi thao tác tiêu credit đều có price preview, confirmation và idempotency; revoke user không ảnh hưởng account khác.
- HTML: login SSO hoạt động; browser không thấy provider keys; user chỉ xem task của mình, admin xem team; mọi lần submit/review có audit.
- Routing: tool/mod lỗi không làm request tự chuyển provider; mỗi route có model/reason/route ID; Codex không bị tuyên bố là tự đổi model qua MCP.
- Apply Patch: không thể ghi ra ngoài worktree/allowlist; patch lỗi trả status `failed`; task có cost ceiling và cancel; mọi thay đổi đều hiện diff trước khi tạo PR; không auto merge.
- Tài chính: usage gắn được với user/project; có cảnh báo 50/80/100%; so khớp được chi phí API và Wandura credits với dashboard nguồn.

## 8. Nguồn giá và tài liệu kỹ thuật

- [Wandura MCP & CLI](https://www.wandura.ai/mcp) — URL, sign-in, tool flow và kiểm tra giá trước khi tạo.
- [Wandura pricing](https://www.wandura.ai/pricing) — Basic/Growth/credit pack, Enterprise workspace và giá credit.
- [Wandura API v2](https://docs.wandura.ai/developers/api-v2) — Jobs API, key, idempotency, webhook và test/live keys.
- [OpenAI Apply Patch](https://developers.openai.com/api/docs/guides/tools-apply-patch) — Responses API, patch operations, harness và an toàn path.
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — Giá token hiện hành; cần kiểm tra lại trước khi vận hành.
- [Kết nối MCP với Codex](https://developers.openai.com/resources/docs-mcp) — Codex CLI và IDE dùng chung cấu hình MCP.
- [ChatGPT Business pricing and access](https://help.openai.com/en/articles/8792828-chatgpt-business-overview) — Seat price, Codex access và lưu ý API billing riêng.
- [OpenAI project spend limits](https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform) — Hard spend limit và alerts.
- [Claude Code Mods overview](https://code.claude.com/docs/en/plugins/mods/overview) · [Mod events](https://code.claude.com/docs/en/plugins/mods/events) — Mod, `turn.step`, đổi model cho request.
- [Claude Code seats for Team/Enterprise](https://www.anthropic.com/news/claude-code-on-team-and-enterprise) · [Anthropic billing](https://support.anthropic.com/en/articles/9267289-how-is-my-bill-calculated).
- [Bảng tham chiếu nội bộ Gateway](Gateway.md) — các mức giá/provider đã khảo sát ngày 29-10-2026; xác nhận lại tại checkout trước khi mua.
