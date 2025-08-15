# Decorator
| Decorator           | Phiên bản | Dùng cho                                   | Mục đích chính                            |
| ------------------- | --------- | ------------------------------------------ | ----------------------------------------- |
| `@validator`        | ✅ v1      | Field (1 hoặc nhiều field)                 | Validate riêng lẻ                         |
| `@root_validator`   | ✅ v1      | Toàn bộ model                              | Validate giữa nhiều field                 |
| `@field_validator`  | ✅ v2      | Field                                      | Thay cho `@validator`, có hỗ trợ pre/post |
| `@model_validator`  | ✅ v2      | Toàn bộ model                              | Thay cho `@root_validator`, pre/post      |
| `@computed_field`   | ✅ v2      | Read-only field tính toán (getter)         | Cho output nhưng không input              |
| `@field_serializer` | ✅ v2      | Custom hóa field khi serialize             | Ví dụ đổi format datetime                 |
| `@model_serializer` | ✅ v2      | Custom hóa toàn bộ model khi serialize     | Thay `.dict()`/`.json()` mặc định         |
| `@property`         | ✅ v1+v2   | Getter không serialize                     | Dùng như Python gốc                       |
| `@classmethod`      | ✅ v1+v2   | Factory methods (custom create/init logic) | Ví dụ: `from_orm`, `from_payload`         |



# Feature

| Tính năng                                  | Dùng ở đâu  | Công dụng chính                                |
| ------------------------------------------ | ----------- | ---------------------------------------------- |
| `Field()`                                  | Trong model | Đặt ràng buộc, default, metadata               |
| `Form()` / `Query()` / `Path()` / `Body()` | Trong route | Nhập liệu từ request (form, query, path, body) |
| `field_validator()`                        | Model class | Custom validation                              |
| `computed_field()`                         | Model class | Field tính toán                                |
| `PrivateAttr()`                            | Model class | Field nội bộ, không hiển thị                   |
| `Config` / `model_config`                  | Model class | Cấu hình toàn cục                              |

