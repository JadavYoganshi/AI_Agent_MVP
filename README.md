# 🧠 AI Agent MVP

This is a complete **AI Assistant MVP System** built using FastAPI, MongoDB, and DuckDuckGo Search, organized into separate microservices and containerized using Docker Compose.

The architecture is based on **modular microservices**, ensuring maintainability, scalability, and independent development and testing. Each service has its own responsibility and communicates via FastAPI routes.

---

## 📖 Introduction

In modern AI systems, modular design helps break down complex functionalities into isolated, manageable components. This AI Agent MVP demonstrates a real-world microservices-based architecture for building an intelligent assistant using:

* **FastAPI** for creating microservices
* **MongoDB** for persistent storage
* **DuckDuckGo** for external web search
* **Docker Compose** for service orchestration

This project is ideal for learners, developers, and teams looking to implement an AI assistant using Python microservices.

---

## 📁 Project Structure

```
AI-MVP/
├── chat_service/
│   ├── main.py
│   └── requirements.txt
├── knowledge_service/
│   ├── main.py
│   └── requirements.txt
├── search_service/
│   ├── main.py
│   └── requirements.txt
├── history_service/
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🚀 Microservices Overview

### 1. **Chat Service** (`localhost:8000`)

* Acts as the main gateway for users to interact.
* Accepts user messages via `/chat` endpoint.
* Steps performed:

  1. Sends the query to **Knowledge Service** to check if the answer is already known.
  2. If no answer is found, sends the query to **Search Service** to fetch from the web.
  3. Saves the final question, answer, source, and timestamp to the **History Service**.
* Does not store any data itself.

### 2. **Knowledge Service** (`localhost:8001`)

* A curated store of predefined question-answer pairs.
* Provides two endpoints:

  * `POST /add` → to add QA pairs to MongoDB
  * `GET /get?q=...` → to retrieve an answer if it exists
* MongoDB schema:

  ```json
  {
    "question": "What is AI?",
    "answer": "AI stands for Artificial Intelligence."
  }
  ```
* Helpful for common queries.

### 3. **Search Service** (`localhost:8002`)

* Uses **DuckDuckGo** to fetch fresh information when knowledge base lacks an answer.
* Endpoint:

  * `GET /search?q=...`
* Sends back plain text response from the search result snippet.

### 4. **History Service** (`localhost:8003`)

* Records each interaction between user and assistant.
* MongoDB schema:

  ```json
  {
    "question": "What is Docker?",
    "answer": "Docker is a platform for containerizing applications.",
    "source": "search",
    "timestamp": "2025-07-26T10:00:00"
  }
  ```
* Endpoints:

  * `POST /add` → Save new interaction
  * `GET /all` → Retrieve all past history
* **No unique ID is included** as per your request.

### 5. **MongoDB**

* Shared across `knowledge_service` and `history_service`
* Exposes default port `27017`
* Used for data persistence

---

## ⚙️ Technology Installation Instructions

To build and run this project, install the following tools:

### 1. Python

* Install Python 3.10 or higher from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Ensure `pip` is installed (`pip --version`)

### 2. FastAPI

Install FastAPI and Uvicorn for all services:

```bash
pip install fastapi uvicorn
```

### 3. MongoDB

* Download MongoDB Community Edition from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
* Follow installation steps for your OS
* Start MongoDB using:

```bash
mongod
```

### 4. DuckDuckGo (No Installation Needed)

* This project uses `duckduckgo-search` package to fetch data:

```bash
pip install duckduckgo-search
```

### 5. Docker (Optional)

* Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* Required only if using Docker-based orchestration

---

## 🐋 Docker-Based Setup Instructions

### ✅ Prerequisites

* Docker
* Docker Compose

### 🛠 Build & Run All Microservices

```bash
docker-compose up --build
```

> This launches all services:
>
> * `chat_service` → [http://localhost:8000](http://localhost:8000)
> * `knowledge_service` → [http://localhost:8001](http://localhost:8001)
> * `search_service` → [http://localhost:8002](http://localhost:8002)
> * `history_service` → [http://localhost:8003](http://localhost:8003)
> * `MongoDB` → localhost:27017

### ❌ Stop Services

```bash
docker-compose down
```

---

## 🔧 API Examples

### 🔹 Chat Service

**GET** `/chat?message=What is AI`

**POST** `/chat`

```json
{
  "message": "What is Docker?"
}
```

### 🔹 Knowledge Base

**POST** `/add`

```json
{
  "question": "What is AI?",
  "answer": "AI stands for Artificial Intelligence."
}
```

**GET** `/get?q=What is AI`

### 🔹 Search Service

**GET** `/search?q=What is OpenAI`

### 🔹 History Service

**POST** `/add`

```json
{
  "question": "What is Docker?",
  "answer": "Docker is a platform for containerizing applications.",
  "source": "search"
}
```

**GET** `/all`

---

## 📚 API Documentation (Swagger UI)

| Service        | Docs URL                                                 |
| -------------- | -------------------------------------------------------- |
| Chat           | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Knowledge Base | [http://localhost:8001/docs](http://localhost:8001/docs) |
| Search         | [http://localhost:8002/docs](http://localhost:8002/docs) |
| History        | [http://localhost:8003/docs](http://localhost:8003/docs) |

---

## 🔮 Future Scope

* Add ChromaDB for vector search
* User authentication for personalized history
* Web dashboard (React/Vue frontend)
* OpenAI integration

---

## 🧑 Author

**Created by Yoganshi Jadav** – Guided by task architecture and Docker-based microservice design.

---

## 📝 License

MIT License. Use freely with attribution.
Update README.md with full project setup and documentation
