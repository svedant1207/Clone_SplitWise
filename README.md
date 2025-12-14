# 🧾 Clone SplitWise 💸

A Splitwise-like expense sharing backend application built with Flask. This project allows users to manage shared expenses, split costs in various ways, and settle up balances.

-----

### 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

-----

### 🚀 Features

*   **👤 User Management**: Register and authenticate users.
*   **💸 Expense Creation**: Add expenses paid by a specific user.
*   **➗ Flexible Splitting**: Support for Equal, Exact, and Percentage based splits.
*   **📊 Balance Calculation**: Automatically calculate how much each user owes or is owed.
*   **🔄 Settlement Logic**: Efficiently settle debts between users.
*   **🧪 Tested**: Comprehensive unit tests using Pytest.
*   **🔐 Authentication**: Simple login/logout implementation.

-----

### ⚙️ Setup & Installation

Follow these steps to get the project running locally on your machine.

#### 1. Clone & Environment Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Database Initialization

You need to initialize the SQLite database before running the app.

```bash
# Initialize the database (creates splitwise.db and tables)
python scripts/init_db.py

# Optional: Seed the database with sample data (Users A, B, C)
python scripts/seed_db.py
```

> **Note:** If you need to wipe the database and start fresh, you can run:
> ```bash
> python scripts/reset_db.py
> ```

#### 4. Run the Application

```bash
flask run
```

The server will start at `http://127.0.0.1:5000`.

#### 5. Run Tests

To ensure everything is working correctly, run the test suite:

```bash
pytest
```

-----

### 💡 API Usage & Quick Start

The API is fully functional. You can interact with it using tools like **Postman** or **Insomnia**.

#### 1. Initial Users (from Seed)

If you ran `python scripts/seed_db.py`, the following users are available:

| ID | Name | Email | Password |
| :--- | :--- | :--- | :--- |
| **1** | User A | `a@test.com` | `pass` |
| **2** | User B | `b@test.com` | `pass` |
| **3** | User C | `c@test.com` | `pass` |

#### 2. key Endpoints

Here are some of the primary endpoints you can use:

*   **Health Check**: `GET /`
*   **Create Expense**: `POST /expenses`
    *   Requires `paid_by_id` (User ID).
*   **Split Expense**:
    *   `POST /expenses/<expense_id>/split/equal`
    *   `POST /expenses/<expense_id>/split/exact`
    *   `POST /expenses/<expense_id>/split/percent`
*   **Get Balances**: `GET /balances`
*   **Settle Up**: `GET /settle`

#### 3. Example Request (Create User)

**POST** `/auth/register` (or appropriate route depending on implementation)

```json
{
  "email": "newuser@test.com",
  "name": "New User",
  "password": "password123"
}
```

-----

### 📂 Project Structure

```
Clone_SplitWise/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # API routes (Blueprints)
│   ├── templates/      # HTML templates
│   └── __init__.py     # App factory
├── scripts/
│   ├── init_db.py      # Create DB tables
│   ├── seed_db.py      # Populate DB with dummy data
│   └── reset_db.py     # Reset DB
├── tests/              # Pytest tests
├── requirements.txt    # Python dependencies
└── run.py              # Entry point
```
