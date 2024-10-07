from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import flask  # Import Flask explicitly for session handling
from database import engine
from sqlalchemy import Text, text, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from flask import make_response
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from mailconfig import mail, app  # Import the mail instance and app
from flask_mail import Mail, Message  # Import the Message class

import os

app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

app = Flask(__name__)
app.secret_key = 'kshda^&93euyhdqwiuhdIHUWQY'
app.config['SECRET_KEY'] = 'kshda^&93euyhdqwiuhdIHUWQY'

# Ensure log level is set for the logger
app.logger.setLevel(logging.INFO)

# Create rotating file handler
file_handler = RotatingFileHandler('webapp-investinbulls.log', maxBytes=50*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to the logger
app.logger.addHandler(file_handler)

with open('webapp-investinbulls.log', 'a') as log_test_file:
    log_test_file.write('Restart : webapp.invetsinbulls.net app started at : '+ datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')


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
  user_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select Email, UserName, UserPassword, UserRole, user_status, creation_date, expire_date from Users"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        user_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_users_from_db: {e}', exc_info=True)
  
  return user_list


def load_tickers_from_db():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TickerStatus from Tickers ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_from_db: {e}', exc_info=True)
  
  return ticker_list

def load_tickers_for_users():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,CreateDate from Tickers where TickerStatus = 'Active' ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_users: {e}', exc_info=True)
  
  return ticker_list


def load_tickers_for_admin():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TickerNotes from Tickers ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_admin: {e}', exc_info=True)
  
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

#Common
@app.route("/reset_pass_v1")
def reset_pass_v1():
  return render_template('reset-pass-v1.html')

@app.route("/reset_pass_v1_update", methods=['POST'])
def reset_pass_v1_update():
  email = request.form['email']
  new_pass = request.form['new-password']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(Email=email).first()

      if user:
          # Update the user's details
          print("=>",user.UserPassword)
          print("=>",new_pass)
          if user.UserPassword == new_pass:
            user.UserPassword = new_pass
            flash('New password and existing password are same !', 'info')
          else:
            user.UserPassword = new_pass
            flash('Password updated successfully !', 'info')

          # Commit the session to save changes to the database
          session.commit()
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_pass: {e}', exc_info=True)
      flash('Sorry! Unable to reset the password, contact Administrator !', 'error')
      return redirect(url_for('loginpage'))
  finally:
      session.close()  # Close the session

  return redirect(url_for('loginpage'))


@app.route("/reset_pass")
def reset_pass():
  return render_template('reset-pass.html')

@app.route("/send_pass_email", methods=['POST'])
def send_pass_email():
  email = request.form['email']

  # Create the welcome message
  subject = "Welcome to Our Service!"
  body = "Dear User,\n\nThank you for joining us! We are excited to have you on board.\n\nBest Regards,\nYour Team"

  # Send the email
  msg = Message(subject, recipients=[email])
  msg.body = body

  try:
      mail.send(msg)
      flash('Welcome email sent successfully!', 'success')
  except Exception as e:
      flash(f'Failed to send email: {str(e)}', 'error')
      
  flash('Password sent to your email. Please check !', 'info')
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
  admintickers = load_tickers_for_admin()
  # Convert to dictionary
  tickers = [
      {
          "created_date": row[0],
          "ticker_name": row[1],
          "entry_price": row[2],
          "stop_percent": row[3],
          "stop_price": row[4],
          "target_1": row[5],
          "target_2": row[6],
          "target_3": row[7],
          "target_4": row[8],
          "ticker_notes": row[9]
      } for row in admintickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/show-ticker-admin.html', grouped_tickers=grouped_tickers)

@app.route("/showusers")
def show_users():
  allusers = load_users_from_db()
  return render_template('/admin/show-users.html', users=allusers)


#Dashboard modules - Users |||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/userdashboard")
def dashboard_user():
  return render_template('/users/dashboard-user.html')

@app.route("/show_ticker_user")
def show_ticker_user():
  usertickers = load_tickers_for_users()
  return render_template('/users/show-tickers-user.html', tickers=usertickers)



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
  

  #generated
  # Example attributes
  # Define the __init__ method to handle the fields
  def __init__(self, username, email, userpassword, userrole):
      self.UserName = username
      self.Email = email
      self.UserPassword = userpassword
      self.UserRole = userrole

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
      return str(self.UserID)
  

# Create the users table if it doesn't exist already
Base.metadata.create_all(engine)

# Set up the session maker
Session = sessionmaker(bind=engine)
session = Session()

# CREATE USER .............................................................
@app.route('/create_user', methods=['POST'])
def create_user():
  email = request.form['email']
  username = request.form['username']
  if len(username) == 0:
     username = request.form['email']

  password = request.form['psw']
  #role = request.form['users']
  role = "General"
  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()
  app.logger.info('create_user: Loggin with user email : '+ str(request.form['email'])+ " / " +str(request.form['username'])
                  + " / " +str(request.form['psw'])+ " / " +str(role))
  try:
    # Create a new user instance
    new_user = User(username=username,
                email=email,
                userpassword=password,
                userrole=role)

    # Add the new user to the session
    session.add(new_user)

    # Commit the session to save changes to the database
    session.commit()
    app.logger.info('create_user: User created with user email : '+ str(request.form['email'])+ " / " +str(request.form['username'])
                  + " / " +str(request.form['psw'])+ " / " +str(role))
    flash('User registration done, please Login !', 'info')
  except Exception as e:
    session.rollback()  # Rollback in case of error
    flash('Facing some issue while user registration. Try later !', 'error')
    app.logger.error(f'An error occurred in create_user: {e}', exc_info=True)
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
      app.logger.error(f'An error occurred in delete_user: {e}', exc_info=True)
      #return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session

  return redirect(url_for('manageuser'))


@app.route('/promote_user', methods=['POST'])
def promote_user():
    email = request.form['user_id']  # Get the email from the form

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query the user by email
        user = session.query(User).filter_by(Email=email).first()

        if user:
            # Promote the user to 'Admin'
            user.UserRole = 'Admin'

            # Commit the session to save changes to the database
            session.commit()
            flash('User promoted to Admin successfully!', 'info')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while promoting user!', 'error')
        app.logger.error(f'An error occurred in promote_user: {e}', exc_info=True)
    finally:
        session.close()  # Close the session

    return redirect(url_for('manageuser'))



@app.route('/demote_user', methods=['POST'])
def demote_user():
    email = request.form['user_id']  # Get the email from the form

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query the user by email
        user = session.query(User).filter_by(Email=email).first()

        if user:
            # Promote the user to 'Admin'
            user.UserRole = 'General'

            # Commit the session to save changes to the database
            session.commit()
            flash('User demoted to General successfully!', 'info')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while demoting user!', 'error')
        app.logger.error(f'An error occurred in demote_user: {e}', exc_info=True)
    finally:
        session.close()  # Close the session

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
  TickerNotes = Column(Text, nullable=True)  # New column for storing notes
  
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
  tickerstatus = "Inactive"
  notes = request.form['notes']

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
                    TickerStatus=tickerstatus,
                    TickerNotes=notes)

    # Add the new user to the session
    session.add(new_ticker)

    # Commit the session to save changes to the database
    session.commit()
  except Exception as e:
    session.rollback()  # Rollback in case of error
    app.logger.error(f'An error occurred in save_ticker: {e}', exc_info=True)
    #return f'An error occurred while adding ticker in DB: {e}'
    flash('An error occurred while adding ticker in DB, Please check the Ticker Name !', 'error')
    return render_template('/admin/dashboard-admin.html')
  finally:
    session.close()  # Close the session

  return render_template('/admin/dashboard-admin.html')

@app.route('/update_ticker', methods=['POST'])
def update_ticker():
    app.logger.info('update_ticker: data : '+ str(request.json))
    data = request.json
    # Perform your DB update logic here using data['ticker_name'], data['entry_price'], etc.
    
    # Return a success or failure message
    try:
      # Your database update logic
      

      return jsonify(success=True)
    except:
        flash('Problem occured in database while deleting !', 'error')
        app.logger.error(f'An error occurred in delete_ticker: {jsonify(success=False)}', exc_info=True)
        #return jsonify(success=False)
    
    return render_template('/admin/dashboard-admin.html')

@app.route('/delete_ticker', methods=['POST'])
def delete_ticker():
  tickername = request.form['ticker_name']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      ticker = session.query(Ticker).filter_by(TickerName=tickername).first()

      if ticker:
          # Delete the user from the session
          session.delete(ticker)

          # Commit the session to remove the user from the database
          session.commit()
          flash('Ticker deleted successfully !', 'info')
      else:
          flash('Ticker not found !', 'error')
  except Exception as e:
      session.rollback()  # Rollback in case of error
      flash('Problem occured in database while deleting !', 'error')
      app.logger.error(f'An error occurred in delete_ticker: {e}', exc_info=True)
      #return f'An error occurred: {e}'
  finally:
      session.close()  # Close the session

  return redirect(url_for('manageticker'))


@app.route('/active_ticker', methods=['POST'])
def active_ticker():
    tickername = request.form['ticker_name']

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query the user by email
        ticker = session.query(Ticker).filter_by(TickerName=tickername).first()

        if ticker:
            # Promote the ticker to 'Active'
            ticker.TickerStatus = 'Active'

            # Commit the session to save changes to the database
            session.commit()
            flash('Ticker updated : Active!', 'info')
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while making Active ticker!', 'error')
        app.logger.error(f'An error occurred in active_ticker: {e}', exc_info=True)
    finally:
        session.close()  # Close the session

    return redirect(url_for('manageticker'))



@app.route('/inactive_ticker', methods=['POST'])
def inactive_ticker():
    tickername = request.form['ticker_name']

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query the user by email
        ticker = session.query(Ticker).filter_by(TickerName=tickername).first()

        if ticker:
            # Promote the ticker to 'Incctive'
            ticker.TickerStatus = 'Inactive'

            # Commit the session to save changes to the database
            session.commit()
            flash('Ticker updated : Inactive!', 'info')
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while makeing Inactive ticker!', 'error')
        app.logger.error(f'An error occurred in inactive_ticker: {e}', exc_info=True)
    finally:
        session.close()  # Close the session

    return redirect(url_for('manageticker'))


#<<<<<<<<<<<<<<<<========================This method calls when login clicks =========================>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/auth_user', methods=['POST', 'GET'])
def auth_user():
  app.logger.info('auth_user: Loggin with user email : '+ str(request.form['email']))
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
          app.logger.info('auth_user: Successful Loggin with user email : '+ str(request.form['email']))
          login_user(user,remember=True, duration=None, force=True, fresh=True) # Flask-Login will now work as expected
          # User found, return user details
          if user.UserRole == "Admin":
            #return render_template('/admin/dashboard-admin.html')
            return redirect(url_for('loadadmindashboard'))
          else:
            #return render_template('/users/dashboard-user.html')
            return redirect(url_for('loaduserdashboard'))
      else:
          app.logger.info('auth_user: Failed Loggin with user email : '+ str(request.form['email']))
          flash('Wrong username or password! Please Try again !', 'error')
          return render_template('login-page.html')
  except Exception as e:
      app.logger.error(f'An error occurred in auth_user: {e}', exc_info=True)
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

@app.route('/update_pass', methods=['POST', 'GET'])
def update_pass():
  email = request.form['email']
  old_pass = request.form['current-password']
  new_pass = request.form['new-password']

  # Create a session
  Session = sessionmaker(bind=engine)
  session = Session()

  try:
      # Query the user by username
      user = session.query(User).filter_by(Email=email, UserPassword=old_pass).first()

      if user:
          # Update the user's details
          if user.UserPassword == old_pass:
            user.UserPassword = new_pass
            flash('Password updated successfully !', 'info')
          else:
            flash('User existing password is not matching. Try again !', 'error')
            return redirect(url_for('update_pass'))

          # Commit the session to save changes to the database
          session.commit()
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_pass: {e}', exc_info=True)
      flash('Sorry! Unable to update the password, contact Administrator !', 'error')
      return redirect(url_for('update_pass'))
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
  alltickers = load_tickers_from_db()
  # Convert to dictionary
  tickers = [
      {
          "created_date": row[0],
          "ticker_name": row[1],
          "entry_price": row[2],
          "stop_percent": row[3],
          "stop_price": row[4],
          "target_1": row[5],
          "target_2": row[6],
          "target_3": row[7],
          "target_4": row[8],
          "ticker_status": row[9]
      } for row in alltickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/manage-tickers.html', grouped_tickers=grouped_tickers)

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

@app.route("/update_admin_pass")
def update_admin_pass():
  return render_template('/admin/update-pass.html')

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
  try:
    print("==>", type(session))  # Debugging line to check the session type
    logout_user()
    flask.session.clear()  # Clear all session data
    flash('You have been logged out successfully!', 'info')
  except Exception as e:
    app.logger.error(f'An error occurred in logout: {e}', exc_info=True)
  
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
