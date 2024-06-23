# FormidiumHackathon-Jaipur-Hackathon2024-Logic-Ninja


README for FormidiumHackathon - Jaipur Hackathon 2024 - Logic Ninja

Project Description

This project is a Flask-based web application designed to integrate generative AI capabilities into an accounting platform. It enables users to generate customized financial reports using natural language queries, while ensuring the privacy and security of individual user data.

Key Features

Prompt-Based Report Generation: Users can create custom reports by entering queries in plain English.
Generative AI: Leverages a SimpleNLP module to translate natural language queries into SQL queries for database interaction.
Data Security: Ensures that each user can only access their own financial data.
User Authentication: Provides a login and registration system for secure access.
Rate Limiting: Includes a rate limiter to prevent abuse and protect the application.
Technical Stack

Framework: Flask
Database: MySQL
Libraries: mysql.connector, bcrypt, Flask-Limiter, dotenv, SimpleNLP (or a similar NLP module)
Frontend: HTML/CSS (using Jinja2 templating in Flask)
Installation and Setup

Clone the Repository:

Bash
git clone https://github.com/FormidiumHackathon/Team9.git
Use code with caution.
content_copy
Create a Virtual Environment:

Bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
Use code with caution.
content_copy
Install Dependencies:

Bash
pip install -r requirements.txt
Use code with caution.
content_copy
Configure Environment Variables:

Create a .env file in the project root directory.
Add your database credentials and a secret key:
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=your_mysql_host  # Usually 'localhost'
DB_NAME=your_database_name
FLASK_SECRET_KEY=your_secret_key  
Run the Application:

Bash
flask run
