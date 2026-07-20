# 🧠 Multi-Agent Decision Engine for Enterprise Operations

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-TypeScript-green)

> **A neuro-symbolic multi-agent platform autonomously orchestrating decisions across siloed enterprise departments.**

## 📖 Overview
Enterprise organizations often operate in isolated silos (Sales, Finance, Logistics), delaying cross-functional responses to market volatility. This project replaces stagnant, descriptive reporting with a **Multi-Agent Decision Engine**. 

By utilizing a centralized orchestrator and specialized domain agents, the platform actively breaks down data silos, dynamically resolves inter-departmental conflicts (e.g., sales growth vs. budget caps), and provides real-time, prescriptive execution plans for human-on-the-loop approval.

## ✨ Key Features
* **Polyglot Microservices:** High-performance TypeScript API gateway handling real-time client sync, coupled with Python-based AI microservices for heavy computation.
* **Autonomous Cross-Domain Negotiation:** Specialized AI agents debate and resolve conflicting departmental goals in milliseconds.
* **Neuro-Symbolic Architecture:** Fuses LLM-based reasoning (Google ADK) with deterministic Machine Learning models (Prophet/XGBoost) for zero-hallucination forecasting.
* **Prescriptive Command Center:** An interactive, role-based Next.js dashboard that visualizes agent reasoning and requires 1-click human approval for massive operational changes.
* **Enterprise-Grade Security:** Built-in Zero-Trust framework with role-based access control (RBAC) and immutable audit logging.

## 🏗️ Architecture

1. **API Gateway & Core Backend (Node.js/TypeScript):** Manages user authentication, database CRUD operations, and real-time streams for the frontend dashboard.
2. **AI & Orchestration Engine (Python/FastAPI):** Built with Google Agent Development Kit (ADK), this microservice houses the AI agents, manages LLM state, and executes deterministic ML pipelines.
3. **Domain Agents (The Specialists):**
   * `Sales Agent`: Analyzes CRM data and forecasts demand.
   * `Inventory Agent`: Monitors stock levels and proposes reorder quantities.
   * `Finance Agent`: Tracks cash flow and enforces budget constraints.

## 💻 Tech Stack
* **AI & Orchestration:** Google Gemini (Vertex AI), Google ADK (Agent Development Kit).
* **AI Backend Microservice:** Python, FastAPI.
* **Core Backend Microservice:** Node.js, TypeScript, Express, WebSockets.
* **Deterministic ML:** Prophet, Scikit-Learn.
* **Data & Memory:** PostgreSQL (Audit/RBAC), Redis.
* **Frontend:** React.
* **Deployment:** Docker, GCP.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js v22 & pnpm
* Docker & Docker Compose
* Google Cloud Platform account (for Vertex AI API keys)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tamil-selvan-k/Multi-Agent-Decision-Engine.git
   cd Multi-Agent-Decision-Engine
   ```

For detailed setup instructions for both Node and Python servers, see our [Setup Guide](docs/setup.md).
For architectural details and how to extend the platform, see our [Developer Guide](docs/developer_guide.md).

## 🤝 Contributing
Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests to this project.
