# MCP chọn model cho Claude Code

## Luồng chính

1. Người dùng nhập yêu cầu như bình thường trong Claude Code CLI.
2. Plugin dạng Mod nhận yêu cầu trước khi Claude xử lý.
3. Mod gọi MCP; Haiku chọn model theo rule đã cấu hình.
4. Mod chuyển các lượt gọi model trong phiên sang model đã chọn.
5. Claude trả lời ngay trong cùng phiên CLI. Các yêu cầu tiếp theo tiếp tục dùng model đó.

Haiku chỉ dùng để chọn model ở đầu phiên; không phân tích lại mọi tin nhắn tiếp theo. Nhờ vậy, công việc chính chạy bằng model phù hợp ngay từ đầu.

**Trải nghiệm:** Không mở app chat riêng hay chat mới. Haiku chọn model trước; câu hỏi được xử lý và trả lời trong cùng hội thoại Claude Code.

## Rule chọn model

| Loại việc | Model gợi ý |
|---|---|
| Việc nhỏ, tìm kiếm, lọc log, tóm tắt | Haiku |
| Viết code và công việc thường ngày | Sonnet |
| Debug khó, sửa nhiều phần hoặc thiết kế hệ thống | Opus |

Haiku nhận mô tả task và thông tin repo tối thiểu, rồi chọn model theo rule. Không gửi mã nguồn hay lịch sử dài nếu không cần. Nếu không chọn được model hoặc bộ chọn gặp lỗi, dùng model mặc định đã cài hoặc hỏi người dùng.

## Khả thi và giới hạn

Có thể tích hợp trực tiếp vào Claude Code CLI bằng plugin có **Mod** và MCP server. Mod nhận prompt trước khi xử lý, gọi MCP chọn model, rồi định tuyến các lượt gọi model trong phiên sang model đó.

MCP server hoặc hook thông thường đứng riêng thì chưa đủ; cần phần Mod để điều khiển prompt và lượt gọi model. Mods cần Claude Code phiên bản 2.1.287 trở lên.

Nếu không tự đổi model được, hãy báo model đã chọn và hỏi người dùng trước khi tiếp tục. Không tự chạy bằng model khác mà chưa báo.

## Ghi nhớ và context

- Lưu ghi chú ngắn: mục tiêu, việc đã làm, file đã sửa, kết quả kiểm tra và bước tiếp theo.
- Phiên mới chỉ đọc ghi chú khi người dùng tiếp tục đúng công việc.
- Khi context gần đầy, lưu ghi chú rồi dùng tính năng nén sẵn có của Claude Code.
- Chỉ clear khi công việc đã xong hoặc chuyển sang việc khác; không tự xóa phiên đang làm dở.

## Nhiều model và agent phụ

Model Haiku chọn sẽ chạy phiên chính. Nếu công việc lớn, có thể giao phần tìm kiếm hoặc tóm tắt cho agent phụ dùng model khác; phiên chính vẫn giữ model đã chọn. Chỉ chạy song song khi các phần việc độc lập và đặt giới hạn chi phí. Mỗi agent phụ dùng thêm token.

## Ưu và nhược điểm

**Ưu điểm**

- Chọn model trước khi bắt đầu xử lý công việc chính.
- Dùng model phù hợp thay vì luôn chạy model đắt, hỗ trợ tiết kiệm phần lớn các chi phí
- Giữ ghi chú để tiếp tục công việc và tránh nạp lại toàn bộ lịch sử.

**Nhược điểm**

- Lượt gọi Haiku thêm một khoản chi phí nhỏ và một chút thời gian chờ.
- Haiku có thể phân loại sai; cần rule dự phòng và cho phép người dùng đổi model.
- Cần phát triển và cài plugin có Mod; chỉ cài MCP server thì chưa đủ.
- Nén hội thoại có thể bỏ sót chi tiết

## Bản đầu nên có

1. Mod nhận yêu cầu đầu tiên trong phiên.
2. Mod gọi MCP để Haiku chọn model và trả lý do.
3. Mod định tuyến các lượt gọi model trong phiên sang model đã chọn.
4. Ghi chú task, nén context và giới hạn chi phí agent phụ.


## Tài liệu tham khảo

- [Mods trong Claude Code](https://code.claude.com/docs/en/plugins/mods/overview): plugin Mod chạy trực tiếp trong CLI.
- [Mod xử lý prompt và model](https://code.claude.com/docs/en/plugins/mods/events): nhận prompt và đổi model cho từng lượt gọi.
- [Mods API](https://code.claude.com/docs/en/plugins/mods/api): gọi model phụ hoặc gọi tool từ MCP server đã kết nối.
- [Plugins](https://code.claude.com/docs/en/plugins): đóng gói Mod và MCP server trong cùng plugin.
- [Claude CLI](https://code.claude.com/docs/en/cli-reference): nhận prompt ban đầu và chọn model bằng `--model`.
