from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import engine
from sqlalchemy import text, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from functools import wraps


app = Flask(__name__)
app.secret_key = 'kshda^&93euyhdqwiuhdIHUWQY'
app.config['SECRET_KEY'] = 'kshda^&93euyhdqwiuhdIHUWQY'

# DB related functions STARTS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
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

# DB related functions ENDS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# All view and redirects link !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Login Page modules

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Check if user is logged in
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))  # Redirect to login
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
  return render_template('login-page.html')

@app.route("/loginpage")
def loginpage():
  return render_template('login-page.html')

@app.route("/register")
def user_register():
  return render_template('user-register.html')

@app.route("/resetpass")
def reset_pass():
  return render_template('reset-pass.html')


#Dashboard modules - Admin ||||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/admindashboard")
def dashboard_admin():
  print(f"Username: {loggedinuser.UserName}")
  return render_template('dashboard-admin.html')

@app.route("/createticker")
def create_ticker():
  return render_template('ticker-create.html')

@app.route("/showadmintickers")
def show_tickers_admin():
  alltickers = load_tickers_from_db()
  return render_template('show-ticker-admin.html', tickers=alltickers)

@app.route("/showusers")
def show_users():
  allusers = load_users_from_db()
  return render_template('show-users.html', users=allusers)


#Dashboard modules - Users |||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/userdashboard")
def dashboard_user():
  return render_template('dashboard-user.html')

@app.route("/showtickers")
def show_tickers():
  alltickers = load_tickers_from_db()
  return render_template('show-tickers-basic.html', tickers=alltickers)




# Method based implementation for DB updates !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
session = Session()
loggedinuser = User()

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
    flash('User registration done, please Login !', 'info')
  except Exception as e:
    session.rollback()  # Rollback in case of error
    flash('Seems like User is already exists !', 'error')
    return render_template('login-page.html')
    #return f'An error occurred: {e}'
  finally:
    session.close()  # Close the session

  return render_template('login-page.html')
  #return 'User created successfully'



#<<<<<<<<<<<<<<<<========================This method calls when login clicks =========================>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/load_dashboard', methods=['POST'])
def load_dashboard():
  # Get the form data
  username = request.form['username']
  password = request.form['psw']

  """if username == "Admin" and password == "Admin":
    return render_template('dashboard-admin.html')
  else:
    flash('Wrong username or password!', 'error')
    return render_template('login-page.html')"""
    
  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username and password
      user = session.query(User).filter_by(UserName=username, UserPassword=password).first()
      # Add the new user to the session
      
      if user:
          loggedinuser = user
          session.add(loggedinuser)
          # User found, return user details
          if user.UserRole == "Admin":
            return render_template('dashboard-admin.html')
          else:
            return render_template('dashboard-user.html')
      else:
          flash('Wrong username or password! Try again !', 'error')
          return render_template('login-page.html')
  except Exception as e:
      return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session


@app.route('/update_user', methods=['POST'])
def update_user():
  username = request.form['username']
  new_email = request.form['email']
  new_password = request.form['psw']
  new_role = request.form['users']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(UserName=username).first()

      if user:
          # Update the user's details
          user.Email = new_email
          user.UserPassword = new_password
          user.UserRole = new_role

          # Commit the session to save changes to the database
          session.commit()
          return f'User {username} updated successfully'
      else:
          return 'User not found'
  except Exception as e:
      session.rollback()  # Rollback in case of error
      return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session


@app.route('/delete_user', methods=['POST'])
def delete_user():
  username = request.form['username']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(UserName=username).first()

      if user:
          # Delete the user from the session
          session.delete(user)

          # Commit the session to remove the user from the database
          session.commit()
          return f'User {username} deleted successfully'
      else:
          return 'User not found'
  except Exception as e:
      session.rollback()  # Rollback in case of error
      return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session



class Ticker(Base):
  __tablename__ = 'Tickers'  # The name of the table in the database

  TickerID = Column(Integer, primary_key=True, autoincrement=True
                  )  # Assuming UserID is the primary key with AUTO_INCREMENT
  UserName = Column(String, nullable=False)
  TickerName  = Column(String, nullable=False)
  EntryPrice = Column(Integer, nullable=False)
  StopPercent = Column(Integer, nullable=False)
  StopPrice = Column(Integer, nullable=False)
  Target1  = Column(Integer, nullable=False)
  Target2 = Column(Integer, nullable=False)
  Target3 = Column(Integer, nullable=False)
  Target4 = Column(Integer, nullable=False)
  #CreateDate  = Column(timestamp, nullable=False)
  TickerStatus  = Column(String, nullable=False)

@app.route('/save_ticker', methods=['POST'])
def save_ticker():
  username = "Admin" #session['username']
  tickername = request.form['tickername']
  entryprice = float(request.form['entryprice'].replace('$', '').replace(',', ''))
  stoppercent = float(request.form['stoppercent'].replace('$', '').replace(',', ''))
  stopprice = float(request.form['stopprice'].replace('$', '').replace(',', ''))
  target1 = float(request.form['target1'].replace('$', '').replace(',', ''))
  target2 = float(request.form['target2'].replace('$', '').replace(',', ''))
  target3 = float(request.form['target3'].replace('$', '').replace(',', ''))
  target4 = float(request.form['target4'].replace('$', '').replace(',', ''))
  tickerstatus = "Active"

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
    # Create a new user instance
    new_ticker = Ticker(UserName=username,
                    TickerName=tickername,
                    EntryPrice=entryprice,
                    StopPercent=stoppercent,
                    StopPrice=stopprice,
                    Target1=target1,
                    Target2=target2,
                    Target3=target3,
                    Target4=target4,
                    TickerStatus=tickerstatus)

    # Add the new user to the session
    session.add(new_ticker)

    # Commit the session to save changes to the database
    session.commit()
  except Exception as e:
    session.rollback()  # Rollback in case of error
    return f'An error occurred while adding ticker in DB: {e}'
  finally:
    session.close()  # Close the session

  return render_template('dashboard-admin.html')


@app.route('/admindashboard')
def dashboard():
  if 'username' in session:
    return f'Welcome, {session["username"]}! This is your dashboard.'
  else:
    flash('You are not logged in. Please log in first.', 'danger')
    return redirect(url_for('home'))





#print(__name__)

# Menu Bar functions |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||
@app.route("/adminpanel")
def adminpanel():
  return render_template('draft.html')

@app.route("/manageticker")
def manageticker():
  return render_template('draft.html')

@app.route("/manageuser")
def manageuser():
  allusers = load_users_from_db()
  return render_template('user-manage.html', users=allusers)

@app.route("/userprofile")
def userprofile():
  return render_template('draft.html')

@app.route("/generaluserprofile")
def generaluserprofile():
  return render_template('draft-user.html')

@app.route('/logout')
def logout():
  #session.clear()  # Clear all session data
  flash('You have been logged out successfully!', 'info')
  #return render_template('login-page.html')
  return redirect(url_for('loginpage'))

# Menu Bar functions |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||


# Calling main application !!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='3001', debug=True)
