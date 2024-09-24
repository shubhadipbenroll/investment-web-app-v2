from flask import Flask, render_template, request
from database import engine
from sqlalchemy import text, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

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
def investment_app():
  return render_template('home.html')


@app.route("/login")
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
    new_user = __tablename__(UserName=username,
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


print(__name__)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5000', debug=True)
