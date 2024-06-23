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


