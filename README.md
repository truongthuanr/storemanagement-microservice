# 🏬 StoreManagement Microservices

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Python%20Web%20Framework-green.svg)](https://fastapi.tiangolo.com/)  
[![gRPC](https://img.shields.io/badge/gRPC-Interservice%20Communication-yellowgreen.svg)](https://grpc.io/)  
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)  
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-orange.svg)](https://www.rabbitmq.com/)

---

## 🧾 Overview

**StoreManagement** là một hệ thống **microservice-based** được xây dựng bằng Python 3.10, FastAPI và gRPC, giúp quản lý toàn bộ hoạt động bán lẻ. Mỗi business domain (sản phẩm, tồn kho, đơn hàng...) được tách thành service riêng biệt để đảm bảo tính **modular**, **scalable** và **maintainable**.

Hiện tại, hệ thống bao gồm:

| Microservice         | Chức năng chính                                               | Tech sử dụng                 |
|----------------------|---------------------------------------------------------------|------------------------------|
| `Product Service`    | CRUD sản phẩm, giao tiếp với Inventory thông qua gRPC         | FastAPI + gRPC client        |
| `Inventory Service`  | Quản lý tồn kho, định giá sản phẩm, expose gRPC và REST API   | FastAPI + gRPC server        |

---

## ⚙️ Tech Stack

| Layer               | Technology                                  |
|---------------------|---------------------------------------------|
| API Framework       | FastAPI                                     |
| Interservice Comm.  | gRPC                                        |
| Database ORM        | SQLAlchemy + MySQL                          |
| Messaging (optional)| RabbitMQ                                    |
| Containerization    | Docker, Docker Compose                      |
| Codegen Tools       | grpcio-tools                                |
| Dev Environments    | Linux / macOS / WSL                         |

---

## 🗂 Project Structure

```bash
storemanagement-microservice/
├── docker-compose.yml
├── inventory-service/
│   ├── Dockerfile
│   ├── app/
│   │   ├──...
│   └── requirements.txt
├── order-service/
│   ├── Dockerfile
│   ├── app/
│   │   ├──...
│   └── requirements.txt
├── product-service/
│   ├── Dockerfile
│   ├── app/
│   │   ├──...
│   └── requirements.txt
└── README.md
```

---

## ▶️ Run Locally with Docker

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- (Optional) Make or bash

### Start all services

```bash
git clone https://github.com/truongthuanr/storemanagement-microservice.git
cd storemanagement-microservice
docker-compose -f docker-compose.dev.yml up --build
```

### Service Endpoints

| Service            | Endpoint                     |
|--------------------|------------------------------|
| Inventory Service  | http://localhost:8001        |
| Product Service    | http://localhost:8002        |

---

## 🔌 gRPC Interservice Communication

- \`product-service\` acts as a gRPC **client** to \`inventory-service\`.
- Protocol defined via \`inventory.proto\` và được biên dịch bằng \`grpcio-tools\`.

### Example:

\`\`\`bash
python -m grpc_tools.protoc \
  -I=inventory-service/protos \
  --python_out=inventory-service/app/proto \
  --grpc_python_out=inventory-service/app/proto \
  inventory-service/protos/inventory.proto
\`\`\`

- Các service giao tiếp với nhau qua tên container nội bộ (Docker network DNS).

---

## 🚀 Future Roadmap

Planned extensions include:

- [ ] **Order Service** – handle order placement and tracking  
- [ ] **User Service** – manage authentication and authorization  
- [ ] **Cart Service** – temporary cart storage per session  
- [ ] **Notification Service** – for async email/SMS via RabbitMQ  
- [ ] **API Gateway** – optional routing via FastAPI or Traefik

---

## 🧠 Key Concepts Applied

- ✅ Clean architecture & domain-driven decomposition  
- ✅ Async communication via gRPC  
- ✅ Dockerized, isolated development per service  
- ✅ Decoupled database per service  
- ✅ RabbitMQ-ready for future event-driven flows  

---

## 🤝 Contributing

PRs and suggestions are welcome. Feel free to fork and raise an issue if you encounter bugs or want to discuss improvements.

---

## 📫 Contact

Maintained by **Nguyễn Trường Thuận**  
GitHub: https://github.com/truongthuanr  
Email: truongthuanr@gmail.com

---

## 📝 License

MIT License © 2025