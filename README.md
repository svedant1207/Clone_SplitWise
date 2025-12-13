# 🧾 Clone SplitWise 💸

A Splitwise-like expense sharing backend built with Flask.

-----

### 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

-----

### 🚀 Features

  * 👤 User management
  * 💸 Expense creation
  * ➗ Equal / Exact / Percentage splits
  * 📊 Balance calculation
  * 🔄 Optimized settlement logic
  * 🧪 Fully unit tested (Pytest)
  * 🔐 Simple login & logout (Flask templates)

-----

### ⚙️ Setup

Follow these commands to get the project running locally:

```bash
# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest


# Initialize the database (creates tables)
if db is not working
  rm splitwise.db
then
  python scripts/init_db.py

# Seed the database with sample data (optional)
python scripts/seed_db.py

# Start the Flask server
flask run
```

-----
