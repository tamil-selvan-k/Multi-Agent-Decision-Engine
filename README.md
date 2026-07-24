# 🧠 Multi-Agent Decision Engine for Enterprise Operations

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-TypeScript-green)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61dafb)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)

> **A neuro-symbolic multi-agent platform autonomously orchestrating decisions across siloed enterprise departments.**

## 📖 Overview
Enterprise organizations often operate in isolated silos (Sales, Finance, Inventory, Logistics), delaying cross-functional responses to market volatility. This project replaces stagnant, descriptive reporting with a **Multi-Agent Decision Engine**. 

By utilizing a centralized orchestrator and specialized domain agents, the platform actively breaks down data silos, dynamically resolves inter-departmental conflicts (e.g., sales growth vs. budget caps or inventory limits vs. shipping speeds), and provides real-time, prescriptive execution plans for human-on-the-loop approval.

## ✨ Key Features
* **Polyglot Microservices:** High-performance TypeScript API gateway handling real-time client sync and authentication, coupled with a Python-based AI microservice for heavy computation and agent reasoning.
* **Autonomous Cross-Domain Negotiation:** Specialized AI agents debate and resolve conflicting departmental goals in milliseconds.
* **Neuro-Symbolic Architecture:** Fuses LLM-based reasoning (Google ADK) with deterministic analytics and database-backed domain tools for accurate, data-driven forecasting.
* **Prescriptive Command Center:** An interactive React dashboard built with Vite that visualizes agent reasoning, key metrics, and enables 1-click human approval for operational changes.
* **Enterprise-Grade Security & Audit:** Built-in security framework with role-based access control (RBAC), Prisma ORM data modeling, and audit logging.

## 🏗️ Architecture

1. **API Gateway & Core Backend (`node_server` - Node.js/TypeScript):** 
   Manages user authentication, Prisma database CRUD operations, logger middleware, and routes orchestration requests to the AI microservice.
2. **AI & Orchestration Engine (`python_server` - Python/FastAPI):** 
   Built with Google Agent Development Kit (ADK) and FastAPI, housing specialized domain agents, LLM orchestration state, and SQLAlchemy database models.
3. **Frontend Dashboard (`client` - React/Vite):** 
   Modern dashboard interface built with React 19, Lucide icons, and React Router for visualization and user decision approvals.
4. **Domain Agents (The Specialists):**
   * 📈 `Sales Agent`: Analyzes historical sales, forecasts demand, calculates growth trends, and recommends production targets.
   * 📦 `Inventory Agent`: Monitors current stock levels, optimizes inventory, tracks warehouse capacity, and generates reorder recommendations.
   * 💰 `Finance Agent`: Tracks departmental budgets, detects financial anomalies, estimates production cost impacts, and enforces budget caps.
   * 🚚 `Logistics Agent`: Fetches active shipments, calculates route optimizations, estimates delivery ETAs and risk scores, and assigns warehouse fulfillment.

## 📁 Directory Structure

```
Multi-Agent-Decision-Engine/
├── client/              # React + Vite frontend user interface & dashboard
├── node_server/          # Node.js + TypeScript API Gateway (Express, Prisma)
├── python_server/        # Python FastAPI AI service (ADK Agents, SQLAlchemy)
│   └── app/
│       ├── agents/       # Sales, Inventory, Finance, Logistics agents
│       ├── tools/        # Domain-specific calculation & database tools
│       ├── models.py     # SQLAlchemy models for PostgreSQL
│       └── main.py       # FastAPI application entrypoint
├── docs/                 # Documentation (Setup Guide, Developer Guide, Task details)
└── CONTRIBUTING.md       # Contribution guidelines
```

## 💻 Tech Stack
* **AI & Orchestration:** Google Gemini (Vertex AI), Google ADK (Agent Development Kit).
* **AI Backend Microservice:** Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, Pydantic.
* **Core Backend Microservice:** Node.js, TypeScript, Express, Prisma ORM, Winston.
* **Database & Memory:** PostgreSQL, Redis, Prisma.
* **Frontend:** React 19, Vite, React Router, Lucide React.
* **Deployment:** Docker, Docker Compose, GCP.

## 🚀 Getting Started

### Prerequisites
* **Python**: 3.10+
* **Node.js**: v22+ / v24+ & pnpm / npm
* **PostgreSQL** & **Docker** (optional for local DB container)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tamil-selvan-k/Multi-Agent-Decision-Engine.git
   cd Multi-Agent-Decision-Engine
   ```

2. **Setup and Run Node.js API Gateway (`node_server`):**
   ```bash
   cd node_server
   pnpm install
   cp .env.example .env
   pnpm run db:push
   pnpm run dev
   ```

3. **Setup and Run Python AI Microservice (`python_server`):**
   ```bash
   cd python_server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   python -m app.main
   ```

4. **Setup and Run Frontend Dashboard (`client`):**
   ```bash
   cd client
   pnpm install
   pnpm run dev
   ```

For comprehensive details:
* 📘 See our [Setup Guide](docs/setup.md) for detailed configuration steps.
* 🛠️ See our [Developer Guide](docs/developer_guide.md) for architecture, guidelines, and extending agents.

## 🤝 Contributing
Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests to this project.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
