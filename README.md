# StoreManagement Microservices

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green.svg)](https://fastapi.tiangolo.com/)
[![gRPC](https://img.shields.io/badge/gRPC-RPC-yellowgreen.svg)](https://grpc.io/)

## Overview

**StoreManagement** is a microservice-based system designed to manage retail operations. Each core business function is separated into its own FastAPI-based service, ensuring modularity, scalability, and ease of maintenance.

### Current Services

- **Inventory Service**: Manages stock levels and pricing, provides both REST API and gRPC interface.
- **Product Service**: Manages product information and communicates with the Inventory Service via gRPC.

---

## Project Structure 
```
storemanagement-microservice/
├── inventory-service/
│ ├── app/
│ │ ├── api/ # (Optional) REST API routes
│ │ ├── proto/ # gRPC definitions and generated code
│ │ ├── services/ # gRPC server logic
│ │ ├── db/ # SQLAlchemy models and DB setup
│ │ └── main.py # Application entrypoint
│ ├── Dockerfile
│ └── requirements.txt
│
├── product-service/
│ ├── app/
│ │ ├── api/ # REST API routes for product management
│ │ ├── proto/ # Compiled gRPC client for Inventory Service
│ │ ├── services/ # Business logic + gRPC client
│ │ ├── db/ # SQLAlchemy models and DB connection
│ │ └── main.py # Application entrypoint
│ ├── Dockerfile
│ └── requirements.txt
│
├── docker-compose.dev.yml # Docker Compose for development
├── docker-compose.prod.yml # Docker Compose for production
└── README.md

```



---

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- MySQL 8.0 (runs in a container via Compose)

---

## Run the Project (Development)

```bash
git clone -b productservice-dev https://github.com/truongthuanr/storemanagement-microservice.git
cd storemanagement-microservice
docker-compose -f docker-compose.dev.yml up --build
```

#### Service endpoints:

- Inventory Service: http://localhost:8001

- Product Service: http://localhost:8002

## gRPC Communication

- Product Service acts as a gRPC client to communicate with Inventory Service.

- Communication is done via defined .proto interfaces (compiled using grpcio-tools).

- All internal services can resolve each other by container name (Docker network).

Example usage:
```bash
python -m grpc_tools.protoc \
  -I=inventory-service/protos \
  --python_out=inventory-service/app/proto \
  --grpc_python_out=inventory-service/app/proto \
  inventory-service/protos/inventory.proto
```
Technologies Used
| Feature           | Technology                               |
| ----------------- | ---------------------------------------- |
| API Framework     | [FastAPI](https://fastapi.tiangolo.com/) |
| RPC Communication | [gRPC](https://grpc.io/)                 |
| Database          | MySQL + SQLAlchemy ORM                   |
| Containerization  | Docker + Docker Compose                  |
| Code Generation   | grpcio-tools                             |
| Dev Environment   | Linux / WSL / Docker Desktop             |


## Contact

For questions or collaboration, feel free to open an issue or submit a pull request on GitHub.



##
# **Draft**
# storemanagement-microservice

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