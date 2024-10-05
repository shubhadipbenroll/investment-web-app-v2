from flask import Flask, render_template, request, redirect, url_for, flash, session
import flask  # Import Flask explicitly for session handling
from database import engine
from sqlalchemy import text, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from flask import make_response

app = Flask(__name__)
app.secret_key = 'kshda^&93euyhdqwiuhdIHUWQY'
app.config['SECRET_KEY'] = 'kshda^&93euyhdqwiuhdIHUWQY'

# Handing for login user management ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
login_manager = LoginManager()
login_manager.login_view = 'loginpage'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    id = session.query(User).filter_by(UserID=id).first()
    print("Logged in user-id: ",id)
    session.close()
    return id


# DB related functions STARTS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def load_users_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select Email, UserName, UserPassword, UserRole, user_status, creation_date, expire_date from Users"))
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

# COMMON PAGES
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

#Common
@app.route("/resetuser")
def resetuser():
  return render_template('reset-userinfo.html')

@app.route("/resetuserdone")
def resetuserdone():
  return render_template('login-page.html')




#Dashboard modules - Admin ||||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/admindashboard")
def dashboard_admin():
  return render_template('/admin/dashboard-admin.html')

@app.route("/createticker")
def create_ticker():
  return render_template('/admin/ticker-create.html')

@app.route("/showadmintickers")
def show_tickers_admin():
  alltickers = load_tickers_from_db()
  return render_template('/admin/show-ticker-admin.html', tickers=alltickers)

@app.route("/showusers")
def show_users():
  allusers = load_users_from_db()
  return render_template('/admin/show-users.html', users=allusers)


#Dashboard modules - Users |||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/userdashboard")
def dashboard_user():
  return render_template('/users/dashboard-user.html')

@app.route("/showtickers")
def show_tickers():
  alltickers = load_tickers_from_db()
  return render_template('/users/show-tickers-basic.html', tickers=alltickers)



# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Method based implementation for DB updates !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
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
  id = UserID
  username = UserName
  #generated
  # Example attributes
  def __init__(self, id, username, active=True):
      self.id = id
      self.username = username
      self.active = active

  # Flask-Login requires this method
  def is_authenticated(self):
      return True

  # Flask-Login requires this method to determine if the user is active
  def is_active(self):
      # You can add custom logic here if you want to deactivate users
      return self.active

  # Flask-Login requires this method
  def is_anonymous(self):
      return False

  # Flask-Login requires this method
  def get_id(self):
      # Must return a string or bytes that uniquely identifies this user
      return str(self.id)
  

# Create the users table if it doesn't exist already
Base.metadata.create_all(engine)

# Set up the session maker
Session = sessionmaker(bind=engine)
session = Session()

# CREATE USER .............................................................
@app.route('/create_user', methods=['POST'])
def create_user():
  username = request.form['username']
  if len(username) == 0:
     username = request.form['email']

  email = request.form['email']
  password = request.form['psw']
  #role = request.form['users']
  role = "General"
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
    print(f'An error occurred-create_user: {e}')
    flash('Facing some issue while user registration. Try later !', 'error')
    return render_template('login-page.html')
    #return f'An error occurred: {e}'
  finally:
    session.close()  # Close the session

  return render_template('login-page.html')
  #return 'User created successfully'

@app.route('/delete_user', methods=['POST'])
def delete_user():
  email = request.form['user_id']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(Email=email).first()

      if user:
          # Delete the user from the session
          session.delete(user)

          # Commit the session to remove the user from the database
          session.commit()
          flash('User deleted successfully !', 'info')
      else:
          flash('User not found !', 'error')
  except Exception as e:
      session.rollback()  # Rollback in case of error
      flash('Problem occured in databse while deleting !', 'error')
      #return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session
  return redirect(url_for('manageuser'))


@app.route('/upgrade_user', methods=['POST'])
def upgrade_user():
  flash('Upgrade user will be working soon !', 'info')
  return redirect(url_for('manageuser'))


@app.route('/disable_user', methods=['POST'])
def disable_user():
  flash('Disable user will be working soon !', 'info')
  return redirect(url_for('manageuser'))

# CREATE TICKER .............................................................
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

  return render_template('/admin/dashboard-admin.html')



#<<<<<<<<<<<<<<<<========================This method calls when login clicks =========================>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/load_dashboard', methods=['POST', 'GET'])
def load_dashboard():
  # Get the form data
  #username = request.form['username']
  email = request.form['email']
  password = request.form['psw']
    
  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username and password
      user = session.query(User).filter_by(Email=email, UserPassword=password).first()
      # Add the new user to the session
      #print("==>" , user.UserName)
      #print("==>" , user.UserRole)
      if user:
          login_user(user,remember=True, duration=None, force=True, fresh=True) # Flask-Login will now work as expected
          # User found, return user details
          if user.UserRole == "Admin":
            #return render_template('/admin/dashboard-admin.html')
            return redirect(url_for('loadadmindashboard'))
          else:
            #return render_template('/users/dashboard-user.html')
            return redirect(url_for('loaduserdashboard'))
      else:
          flash('Wrong username or password! Please Try again !', 'error')
          return render_template('login-page.html')
  except Exception as e:
      print(f'An error occurred: {e}')
      flash('Problem occured while login! Please Try later !', 'error')
      return redirect(url_for('loginpage'))
  finally:
      session.close()  # Close the session

@app.route("/loadadmindashboard")
@login_required
def loadadmindashboard():
  return render_template('/admin/dashboard-admin.html')

@app.route("/loaduserdashboard")
@login_required
def loaduserdashboard():
  if current_user.is_authenticated:
    return render_template('/users/dashboard-user.html')
  else:
     return render_template('login-page.html')

@app.route("/loaduserdashboard2")
@login_required
def loaduserdashboard2():
    response = make_response(render_template('/users/dashboard-user.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response

@app.route('/updatepass', methods=['POST'])
def updateuser():
  email = request.form['email']
  old_pass = request.form['current-password']
  new_pass = request.form['new-password']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(Email=email).first()

      if user:
          # Update the user's details
          if user.UserPassword == old_pass:
            user.UserPassword = new_pass
            flash('Password updated successfully !', 'info')
          else:
             flash('User existing password is not matching. Try again !', 'error')
          

          # Commit the session to save changes to the database
          session.commit()
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      session.rollback()  # Rollback in case of error
      return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session

  return redirect(url_for('logout'))

#print(__name__)

# Menu Bar functions |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||

#Admin based
@app.route("/adminpanel")
def adminpanel():
  return render_template('/admin/draft.html')

@app.route("/manageticker")
def manageticker():
  return render_template('/admin/draft.html')

@app.route("/manageuser")
def manageuser():
  allusers = load_users_from_db()
  return render_template('/admin/user-manage.html', users=allusers)

@app.route("/adminprofile")
def adminprofile():
  return render_template('/admin/admin-profile.html')

@app.route("/adminusercreate")
def adminusercreate():
  return render_template('/admin/user-register-admin.html')

@app.route("/resetpassword")
def resetpassword():
  return render_template('/admin/reset-pass.html')

#User based
@app.route("/userpanel")
def userpanel():
  return render_template('/users/draft.html')

@app.route("/userprofile")
def userprofile():
  return render_template('/users/user-profile.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
  print("==>", type(session))  # Debugging line to check the session type
  logout_user()
  flask.session.clear()  # Clear all session data
  flash('You have been logged out successfully!', 'info')
  #return render_template('login-page.html')
  return redirect(url_for('loginpage'))

# Menu Bar functions ENDs |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||

@app.after_request
def add_header(response):
    # Disable caching to prevent going back to the previous pages after logout
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# Calling main application !!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == "__main__":
  #app.run()
  app.run(host='0.0.0.0', port='3001', debug=True)
