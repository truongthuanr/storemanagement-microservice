"# storemanagement-microservice" 

## Microservice

### Inventory Service
```
online-shopping/
│
|-- gateway-service/       # Xử lý request từ client, định tuyến đến các service
|-- inventory-service/     # 📦 Service quản lý hàng tồn kho
│   |-- app/
│   │   |-- api/           # FastAPI route handlers
│   │   |-- models/        # SQLAlchemy models
│   │   |-- crud/          # Repository (DB logic)
│   │   |-- schemas/       # Pydantic schemas
│   │   |-- main.py        # App entry point
│   |-- Dockerfile
│   |-- requirements.txt
|-- docker-compose.yml
|-- mysql/                 # Volume data của MySQL cho inventory


```






draft
1. Phân tách các thành phần (Domain Decomposition)
Dựa vào chức năng, bạn có thể chia dự án thành các service như sau:

Microservice	Chức năng
User Service	Đăng ký, đăng nhập, phân quyền (Auth)
Product Service	Quản lý sản phẩm, danh mục
Cart Service	Giỏ hàng
Order Service	Đặt hàng, theo dõi đơn hàng
Payment Service	Xử lý thanh toán
Review Service	Đánh giá, nhận xét sản phẩm
Notification Service (tùy chọn)	Gửi email, thông báo

2. Kiến trúc giao tiếp
Sử dụng FastAPI cho từng service (có thể triển khai độc lập).

Giao tiếp giữa các service có thể dùng:

HTTP REST API (đơn giản)

Message Queue như RabbitMQ / Redis Streams (cho các task bất đồng bộ).

3. Shared resources
Cơ sở dữ liệu tách biệt cho mỗi service (nên là best practice).

Redis / Celery: Xử lý task nền như gửi email, đồng bộ hóa.

API Gateway: Một entrypoint duy nhất (ví dụ: dùng FastAPI hoặc Traefik / NGINX).

4. Công cụ triển khai
Docker: Container hóa từng service.

Docker Compose: Quản lý nhiều service cùng lúc khi phát triển local.

Kubernetes: Cho triển khai production ở quy mô lớn.

5. Bắt đầu từng bước
Tách service User ra trước (Auth + JWT)

Tách Product Service

Tạo API Gateway hoặc route thông qua frontend

Dùng Docker Compose để test service phối hợp với nhau

Triển khai Celery + Redis nếu cần task nền