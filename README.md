# 🧾 Clone SplitWise 💸

A Splitwise-like expense sharing backend application built with Flask. This project allows users to manage shared expenses, split costs in various ways, and settle up balances. It is designed to be easy to deploy using Docker.

-----

### 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

-----

### 🚀 Features

*   **👤 User Management**: Register and authenticate users securely (Flask-Login).
*   **💸 Expense Tracking**: Record expenses paid by specific users.
*   **➗ Flexible Splitting**: Support for Equal, Exact, and Percentage based splits.
*   **📊 Balance Calculation**: Real-time calculation of debts and receivables.
*   **🔄 Settlement**: Logic to settle debts between users efficiently.
*   **🐳 Containerized**: Fully containerized with Docker and Docker Compose for easy deployment.
*   **🧪 Tested**: Comprehensive unit tests using Pytest.

-----

### ⚙️ Setup & Installation

You can run this project either using **Docker (Recommended)** or locally with a virtual environment.

#### Option 1: Docker (Recommended)

Ensure you have [Docker](https://www.docker.com/products/docker-desktop) and Docker Compose installed.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/svedant1207/Clone_SplitWise
    cd Clone_SplitWise
    ```

2.  **Create Environment File**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    *   *Optional*: Edit `.env` to change `SECRET_KEY` or `GUNICORN_WORKERS`.

3.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    *   The app will be available at `http://localhost:80`.
    *   **Nginx** acts as a reverse proxy sitting in front of the **Gunicorn** application server.
    *   Database initialization and seeding happen automatically on the first run via `entrypoint.sh`.

4.  **Stop the Application**:
    ```bash
    docker-compose down
    ```

#### Option 2: Local Development

1.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database**:
    ```bash
    python scripts/init_db.py
    python scripts/seed_db.py  # Optional: Adds dummy users A, B, C
    ```

4.  **Run the Application**:
    ```bash
    flask run
    ```
    The server will start at `http://127.0.0.1:5000`.

5.  **Run Tests**:
    ```bash
    pytest
    ```

-----

### 💡 API Usage

**Base URL**: `http://localhost:80` (Docker) or `http://localhost:5000` (Local)

#### Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Health check / Welcome message |
| **POST** | `/auth/register` | Register a new user |
| **POST** | `/auth/login` | Login user |
| **POST** | `/expenses` | Create a new expense |
| **POST** | `/expenses/<id>/split/equal` | Split expense equally |
| **POST** | `/expenses/<id>/split/exact` | Split expense by exact amounts |
| **POST** | `/expenses/<id>/split/percent` | Split expense by percentage |
| **GET** | `/balances` | Get current user balances |
| **GET** | `/settle` | Settle up debts |

#### Test Users (from Seed)

If you ran `python scripts/seed_db.py` (or used the Docker setup), these users are pre-populated:

| ID | Name | Email | Password |
| :--- | :--- | :--- | :--- |
| **1** | User A | `a@test.com` | `pass` |
| **2** | User B | `b@test.com` | `pass` |
| **3** | User C | `c@test.com` | `pass` |

#### Example: Create Expense
```json
POST /expenses
{
  "description": "Lunch",
  "amount": 100.0,
  "paid_by_id": 1
}
```

-----

### 📂 Project Structure

```
Clone_SplitWise/
├── app/
│   ├── models/         # SQLAlchemy Database models
│   ├── routes/         # Flask Blueprints (API endpoints)
│   ├── templates/      # Jinja2 templates (if applicable)
│   └── __init__.py     # App factory & extension init
├── scripts/
│   ├── init_db.py      # Script to create tables
│   ├── seed_db.py      # Script to seed dummy data
│   └── reset_db.py     # Script to reset DB
├── tests/              # Pytest suite
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker services config (Web + Nginx)
├── nginx.conf          # Nginx configuration
├── requirements.txt    # Python dependencies
└── run.py              # Application entry point
```
