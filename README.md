# 🏬 StoreManagement Microservices

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Python%20Web%20Framework-green.svg)](https://fastapi.tiangolo.com/)  
[![gRPC](https://img.shields.io/badge/gRPC-Interservice%20Communication-yellowgreen.svg)](https://grpc.io/)  
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)  
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-orange.svg)](https://www.rabbitmq.com/)

---

## 🧾 Overview

**StoreManagement** is a microservice-based system built with Python 3.10, FastAPI, and gRPC. Each business domain (products, inventory, orders...) is split into individual services to ensure **modularity**, **scalability**, and **ease of maintenance**.

Current services include:

| Microservice       | Description                                                                 | Technologies                |
|--------------------|-----------------------------------------------------------------------------|-----------------------------|
| `Product Service`  | CRUD product management; communicates with Inventory via gRPC               | FastAPI + gRPC client       |
| `Inventory Service`| Stock management and pricing; exposes both REST and gRPC interfaces         | FastAPI + gRPC server       |
| `Order Service`    | Order creation and tracking; async communication with Inventory via RabbitMQ| FastAPI + RabbitMQ (pub/sub)|

---

## ⚙️ Tech Stack

| Layer                | Technology                                  |
|----------------------|---------------------------------------------|
| API Framework        | FastAPI                                     |
| Interservice Comm.   | gRPC (sync), RabbitMQ (async)               |
| Database ORM         | SQLAlchemy + MySQL                          |
| Messaging Queue      | RabbitMQ (aio-pika)                         |
| Containerization     | Docker, Docker Compose                      |
| Codegen Tools        | grpcio-tools                                |
| Service Structure    | Layered: api / service / broker / crud / log|
| Dev Environments     | Linux / Window / WSL                         |

---

## 🗂 Project Structure

```
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
| Order Service      | http://localhost:8003        |

---

## 🔌 Interservice Communication

- `product-service` acts as a **gRPC client** to `inventory-service`.
- Protocols defined in `inventory.proto`, compiled via `grpcio-tools`.

```bash
python -m grpc_tools.protoc \
  -I=inventory-service/protos \
  --python_out=inventory-service/app/proto \
  --grpc_python_out=inventory-service/app/proto \
  inventory-service/protos/inventory.proto
```

- `order-service` communicates with `inventory-service` via **RabbitMQ**:
  - Publishes `order.created` events
  - Listens to `inventory.response` for stock confirmation
- All services communicate through internal Docker network using service names.

---

## 🚀 Future Roadmap

Planned extensions:

- [x] **Order Service** – manage order creation & inventory reservation  
- [ ] **User Service** – handle authentication and user accounts  
- [ ] **Cart Service** – session-based cart before checkout  
- [ ] **Notification Service** – async email/SMS using message queue  
- [ ] **API Gateway** – optional routing layer (e.g., FastAPI or Traefik)

---

## 🧠 Key Concepts Applied

- ✅ Domain-based service decomposition  
- ✅ gRPC for synchronous internal calls  
- ✅ RabbitMQ for async workflows  
- ✅ Clean code separation per service  
- ✅ Fully dockerized dev environment  
- ✅ Production-readiness in structure

---

## 🤝 Contributing

Pull requests and suggestions are welcome. Feel free to fork and raise an issue for bugs or improvements.

---

## 📫 Contact

Maintained by **Nguyễn Trường Thuận**  
GitHub: https://github.com/truongthuanr  
Email: truongthuanr@gmail.com

---

## 📝 License

MIT License © 2025
