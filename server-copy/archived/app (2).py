from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import engine
from sqlalchemy import text, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

"""
File Name: myapp.py
Purpose: Handles routing and server setup for the investment web application.
Version: 1.0.0
Author: Shubhadip Bera
Date Created: 2024-09-29
Last Modified: 2024-09-29
Modified By: Shubhadip Bera
Description:
    This file sets up the Flask application, handles routes for user interactions, 
    and manages the integration with the backend services.
"""

app = Flask(__name__)


def load_users_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from Users"))
    #print("type(result.all())", type(result.all()))
    #print(result.all())
    user_list = []
    for row in result.all():
      user_list.append(row)

    return user_list


def load_tickers_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from Tickers"))
    #print("type(result.all())", type(result.all()))
    #print(result.all())
    ticker_list = []
    for row in result.all():
      ticker_list.append(row)

    return ticker_list


@app.route("/")
def home():
  return render_template('login-page.html')


@app.route("/loginpage")
def login_page():
  return render_template('login-page.html')


@app.route("/register")
def user_register():
  return render_template('user-register.html')


@app.route("/dashboard")
def dashboard_page():
  return render_template('dashboard.html')


@app.route("/ticker")
def create_ticker():
  return render_template('ticker-create.html')


@app.route("/showtickers")
def show_tickers():
  alltickers = load_tickers_from_db()
  return render_template('show-tickers.html', tickers=alltickers)


@app.route("/showusers")
def show_users():
  allusers = load_users_from_db()
  return render_template('show-users.html', users=allusers)


@app.route("/resetpass")
def reset_pass():
  return render_template('reset-pass.html')


@app.route("/usermanage")
def user_manage():
  return render_template('user-manage.html')


Base = declarative_base()


# Define the User model
class User(Base):
  __tablename__ = 'Users'  # The name of the table in the database

  UserID = Column(Integer, primary_key=True, autoincrement=True
                  )  # Assuming UserID is the primary key with AUTO_INCREMENT
  UserName = Column(String, nullable=False)
  Email = Column(String, nullable=False)
  UserPassword = Column(String, nullable=False)
  UserRole = Column(String, nullable=False)


# Create the users table if it doesn't exist already
Base.metadata.create_all(engine)

# Set up the session maker
Session = sessionmaker(bind=engine)


@app.route('/create_user', methods=['POST'])
def create_user():
  username = request.form['username']
  email = request.form['email']
  password = request.form['psw']
  role = request.form['users']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
    # Create a new user instance
    new_user = User(UserName=username,
                    Email=email,
                    UserPassword=password,
                    UserRole=role)

    # Add the new user to the session
    session.add(new_user)

    # Commit the session to save changes to the database
    session.commit()
  except Exception as e:
    session.rollback()  # Rollback in case of error
    return f'An error occurred: {e}'
  finally:
    session.close()  # Close the session

  return 'User created successfully'


@app.route('/login', methods=['POST'])
def login():
  # Get the form data
  username = request.form['username']
  password = request.form['psw']

  # Create a session
  db_session = Session()

  try:
    # Query the User table to check if the user exists with the provided username and password
    user = db_session.query(User).filter_by(UserName=username,
                                            UserPassword=password).first()

    if user:
      # If user is found, store user information in the session
      session['username'] = user.UserName
      flash('Login successful!', 'success')
      return redirect(
          url_for('dashboard')
      )  # Redirect to a dashboard or another page after successful login
    else:
      # If no user is found, show error message
      flash('Invalid username or password. Please try again.', 'danger')
      return redirect(url_for('home'))
  except Exception as e:
    db_session.rollback()
    flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('home'))
  finally:
    db_session.close()


@app.route('/dashboard')
def dashboard():
  if 'username' in session:
    return f'Welcome, {session["username"]}! This is your dashboard.'
  else:
    flash('You are not logged in. Please log in first.', 'danger')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
  session.pop('username', None)
  flash('You have been logged out.', 'success')
  return redirect(url_for('home'))


print(__name__)

if __name__ == "__main__":
  app.run()
#  app.run(host='0.0.0.0', port='3001', debug=False)
