| Nhóm mã | Mã    | Tên gọi                   | Ý nghĩa chính                                                     |
| ------- | ----- | ------------------------- | ----------------------------------------------------------------- |
| 1xx     | `100` | Continue                  | Tiếp tục gửi phần còn lại của request                             |
|         | `101` | Switching Protocols       | Server đồng ý đổi protocol                                        |
| 2xx     | `200` | OK                        | Thành công (thường dùng GET/PUT)                                  |
|         | `201` | Created                   | Tạo mới thành công (thường dùng POST)                             |
|         | `202` | Accepted                  | Đã nhận request, xử lý sau                                        |
|         | `204` | No Content                | Thành công, không có nội dung trả về                              |
| 3xx     | `301` | Moved Permanently         | URL đã được chuyển vĩnh viễn                                      |
|         | `302` | Found (Moved Temporarily) | URL tạm thời chuyển                                               |
|         | `304` | Not Modified              | Không thay đổi, dùng cache được                                   |
| 4xx     | `400` | Bad Request               | Request sai định dạng, thiếu trường                               |
|         | `401` | Unauthorized              | Chưa đăng nhập, token sai                                         |
|         | `403` | Forbidden                 | Không có quyền truy cập                                           |
|         | `404` | Not Found                 | Không tìm thấy tài nguyên                                         |
|         | `409` | Conflict                  | Xung đột dữ liệu                                                  |
|         | `422` | Unprocessable Entity      | Dữ liệu đúng cú pháp nhưng sai logic (thường dùng với validation) |
| 5xx     | `500` | Internal Server Error     | Lỗi server chung                                                  |
|         | `502` | Bad Gateway               | Gateway nhận response lỗi từ upstream                             |
|         | `503` | Service Unavailable       | Server đang quá tải hoặc bảo trì                                  |
|         | `504` | Gateway Timeout           | Server không nhận được phản hồi kịp thời từ upstream              |
