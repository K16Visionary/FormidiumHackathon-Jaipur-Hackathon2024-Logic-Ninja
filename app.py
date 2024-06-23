import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, g, redirect, url_for, session
import mysql.connector
import bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from simple_nlp import SimpleNLP

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Rate Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)
limiter.init_app(app)

# Database Configuration
db_config = {
    'user': 'root',
    'password': '6411',
    'host': 'localhost',
    'database': 'formidium'
}

# Helper function to establish database connection
def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**db_config)
            g.cursor = g.db.cursor()
        except mysql.connector.Error as err:
            return f"Database connection error: {err}"  # Return error message
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Login check
def is_logged_in():
    return 'user_id' in session

# Main page
@app.route('/', methods=['GET', 'POST'])
@limiter.limit("18 per minute")
def index():
    if not is_logged_in():
        return redirect(url_for('login'))

    report = ""  # Initialize report here

    if request.method == 'POST':
        query = request.form['query']
        # Initialize SimpleNLP (with correct table name)
        nlp = SimpleNLP(table_name="accounts")

        keywords = ["account", "balance", "account_type"]  # Update keywords
        table_name = "accounts"  # Update table name
        sql_query = nlp.generate_sql_query(query, keywords) 
        print(sql_query)

        db = get_db()  
        if isinstance(db, str):  # Handle potential connection errors
            report = f"<h2>Error:</h2><p>{db}</p>"
        else:
            try:
                cursor = db.cursor() 
                cursor.execute(sql_query)
                results = cursor.fetchall()

                # Format the results
                report = "<h2>Report:</h2><table>"
                if results:
                    # Add header row based on the first result
                    report += "<tr>" + "".join([f"<th>{col[0]}</th>" for col in cursor.description]) + "</tr>"

                    for row in results:
                        report += "<tr>"
                        for col in row:
                            report += f"<td>{col}</td>"
                        report += "</tr>"
                else:
                    report += "<tr><td colspan='5'>No results found</td></tr>"  # If no results
                report += "</table>"

            except mysql.connector.Error as err:
                if err.errno == 1064:  # Check for SQL syntax error
                    report = "<h2>Invalid Query</h2><p>The query is not valid.</p>"
                else:
                    report += f"<h2>Error:</h2><p>{err}</p>"

    return render_template("index.html", report=report)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        if isinstance(db, str):
            return render_template('login.html', error=db)
        
        g.cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = g.cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Encode both passwords
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db()
        if isinstance(db, str):
            return render_template('login.html', error=db, is_register=True)

        try:
            g.cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            g.db.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return render_template('login.html', error="Registration failed. Please try again.", is_register=True) 

    return render_template('login.html', is_register=True) 


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
