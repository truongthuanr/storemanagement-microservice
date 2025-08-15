```
          [ Client / App / Web ]
                   |
                   v
            [ API Gateway ]
                   |
        +----------+-----------+
        |                      |
        v                      v
 [ auth-service ]        [ order-service ] --- gRPC ---> [ inventory-service ]
   |        |                 |                               (reserve/release)
   |        |                 |
   |        |                 +--(Outbox)--> [ Kafka: orders.events, payments.events, ... ]
   |        |
   |  (Outbox)--> [ Kafka: auth.events ]
   |
   |  JWKS -----> (public keys for JWT verification)
   |
   +-- JWT --> (used by all services)
   
[ noti-service ]
   ^        |
   |        +-- Celery worker(s) --> Email/SMS/Push Providers
   |
 (Kafka consumer: auth.events, payments.events, orders.events ...)
```

- auth-service: cấp JWT, quản lý user/roles, phát sự kiện auth.* lên Kafka (theo Outbox pattern).

- order-service: tạo đơn, phát sự kiện orders.*/payments.* lên Kafka (cũng theo Outbox).

- inventory-service: giao tiếp gRPC đồng bộ với order (giữ nguyên).

- noti-service: Kafka consumer (nhiều nhóm tiêu thụ khác nhau nếu cần), tạo Celery tasks để gửi email/SMS/push.

- Celery broker: RabbitMQ/Redis (tách biệt với Kafka).

- JWKS: các service khác verify JWT offline.

### Các thành phần & trách nhiệm
##### auth-service

- Endpoints: register/login/refresh/logout, password reset, JWKS.

- JWT Issuer (RS256/EdDSA) + key rotation; RBAC/ABAC qua claims.

- Audit & Security events → Kafka auth.events (mask/hash PII).

- Dùng Outbox để đảm bảo event được phát đúng đắn cùng transaction DB.

##### noti-service

- Kafka Consumer:

  + Nghe auth.events → welcome email, reset password email, login alert…

  + (Mở rộng) nghe payments.events → gửi hoá đơn/biên nhận.

  + (Mở rộng) nghe orders.events → gửi update trạng thái đơn.

- Celery: tách “gửi thực tế” khỏi consumer (retry/backoff, cách ly lỗi).

- Template/Provider adapters (SMTP/SendGrid/SES, SMS, push).

##### order-service (hiện có)

- Core API checkout, DB orders.

- Outbox → orders.events, payments.events (khi thanh toán xong).

- Giữ gRPC với inventory cho “command” nhanh.

##### inventory-service (hiện có)

- gRPC server: reserve/release stock.

- (Tuỳ chọn sau) có thể emit inventory.updated lên Kafka (không bắt buộc).

### Thiết kế sự kiện & hợp đồng (contract)
- Topic tối thiểu

  - auth.events (partition key: user_id)

  - orders.events (partition key: order_id)

  - payments.events (partition key: order_id)

### Luồng dữ liệu chính (Sequence tóm tắt)
1) Đăng ký tài khoản (Auth → Kafka → Noti → Email)
2) Đăng nhập & cảnh báo bảo mật
3) Quên mật khẩu / Reset mật khẩu
4) Thanh toán thành công (Payment → Kafka → Noti)
5) Đặt hàng (Order → Kafka → Noti) + giữ nguyên gRPC Inventory