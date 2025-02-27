from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import flask
from flask_mail import Message
from pymysql import TIMESTAMP  # Import Flask explicitly for session handling
from database import engine
from sqlalchemy import DECIMAL, DateTime, Float, Text, func, text, Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from flask import make_response
import logging
from logging.handlers import RotatingFileHandler
from datetime import date, datetime, timedelta
from mailconfig import configure_mail, send_email, send_email_to_users  # Importing email functions
import os
from database import DB_ENV
from werkzeug.utils import secure_filename
from pathlib import Path
import json

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
PRIVATE_VIDEOS_FILE = 'private_videos.txt' #File to store private videos
PRIVACY_FILE = 'privacy.json' # to store video privacy

app = Flask(__name__)
app.secret_key = 'kshda^&93euyhdqwiuhdIHUWQY'
app.config['SECRET_KEY'] = 'kshda^&93euyhdqwiuhdIHUWQY'

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Or any other preferred type
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=600)  # Adjust the duration as needed
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies

#Video config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # Max upload size (16MB)
app.config['PRIVATE_VIDEOS_FILE'] = PRIVATE_VIDEOS_FILE
app.config['PRIVACY_FILE'] = PRIVACY_FILE

# Configure Flask-Mail
mail = configure_mail(app)

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
    log_test_file.write('Restart : webapp.invetsinbulls.net app home page loaded at : '+ datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

@app.route('/debug_log', methods=['POST'])
def debug_log():
    data = request.get_json()
    message = data.get('message')
    print(message)  # This will print to the terminal/console
    return jsonify({"status": "logged"})

# Handing for login user management ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'loginpage'
login_manager.login_message = "Please log in to access the page."
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(id):
    Session = sessionmaker(bind=engine)
    db_session = Session()
    id = db_session.query(User).filter_by(UserID=id).first()
    #print("Logged in user-id: ",id)
    db_session.close()
    return id


# DB related functions STARTS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

## ADMIN TABLE FUNCTIONS
def load_tickers_for_admin():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TrailStop,ticker_type,TickerStatus,TickerNotes from Tickers ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_admin: {e}', exc_info=True)
  
  return ticker_list

def load_users_details_from_db():
  user_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select Email, UserName, UserPassword, UserRole, user_status, creation_date, expire_date, mobile_number from Users order by UserName"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        user_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_users_details_from_db: {e}', exc_info=True)
  
  return user_list

def load_users_from_db():
  user_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select Email, UserName, UserRole, user_status, creation_date, expire_date, country_code, mobile_number from Users order by UserName"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        user_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_users_from_db: {e}', exc_info=True)
  
  return user_list

def load_targets_from_db():
  target_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select ticker_type, target1, target2, target3, target4 from ticker_targets order by ticker_type DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        target_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_targets_from_db: {e}', exc_info=True)
  
  return target_list


def load_tickers_from_db():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TrailStop,ticker_type,TickerStatus from Tickers ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_from_db: {e}', exc_info=True)
  
  return ticker_list

## USER TABLE FUNCTIONS ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def load_tickers_for_watchlist():
  ticker_list = []
  try:
    with engine.connect() as conn:
      result = conn.execute(text("select UpdateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TrailStop,TickerStatus,TickerNotes,ticker_type from Tickers WHERE TickerStatus in ('Active','Profit-Book','Loss-Book') ORDER BY CreateDate DESC"))
      #result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TrailStop,TickerStatus,TickerNotes from Tickers ORDER BY CreateDate DESC"))
      #print("type(result.all())", type(result.all()))
      #print(result.all())
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_watchlist: {e}', exc_info=True)
  
  return ticker_list

def load_tickers_for_trading():
  ticker_list = []
  try:
    with engine.connect() as conn:
      #result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TickerStatus,TickerNotes from Tickers WHERE DATE(CreateDate) = CURDATE() ORDER BY CreateDate DESC"))
      #Only show last date data
      #result = conn.execute(text("SELECT CreateDate, TickerName, EntryPrice, StopPercent, StopPrice, Target1, Target2, Target3, Target4, TickerStatus,TickerNotes FROM Tickers WHERE TickerStatus='Active' AND DATE(CreateDate) = ( SELECT MAX(DATE(CreateDate)) FROM Tickers ) ORDER BY CreateDate DESC"))
      result = conn.execute(text("SELECT UpdateDate, TickerName, EntryPrice, StopPrice, Target1, Target2, Target3, Target4, TrailStop,TickerStatus, ticker_qty, TickerNotes FROM Tickers WHERE TickerStatus in ('Active','Profit-Book','Loss-Book') and ticker_type='Swing' ORDER BY CreateDate DESC"))
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_trading: {e}', exc_info=True)
  
  return ticker_list

def load_tickers_for_investment():
  ticker_list = []
  try:
    with engine.connect() as conn:
      #result = conn.execute(text("select CreateDate,TickerName,EntryPrice,StopPercent,StopPrice,Target1,Target2,Target3,Target4,TickerStatus,TickerNotes from Tickers WHERE DATE(CreateDate) = CURDATE() ORDER BY CreateDate DESC"))
      #Only show last date data
      #result = conn.execute(text("SELECT CreateDate, TickerName, EntryPrice, StopPercent, StopPrice, Target1, Target2, Target3, Target4, TickerStatus,TickerNotes FROM Tickers WHERE TickerStatus='Active' AND DATE(CreateDate) = ( SELECT MAX(DATE(CreateDate)) FROM Tickers ) ORDER BY CreateDate DESC"))
      result = conn.execute(text("SELECT UpdateDate, TickerName, EntryPrice, StopPrice, Target1, Target2, Target3, Target4, TrailStop,TickerStatus,TickerNotes FROM Tickers WHERE TickerStatus in ('Active','Profit-Book','Loss-Book') and ticker_type='Investment' ORDER BY CreateDate DESC"))
      for row in result.all():
        ticker_list.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_tickers_for_investment: {e}', exc_info=True)
  
  return ticker_list


def load_risk_apt_from_db(user_email_id,type):
  user_risk = []
  try:
    with engine.connect() as conn:
      if type == 'Swing':
        query = text("SELECT swing_capital, swing_percent FROM user_risk_apt WHERE user_email = :user_email AND ticker_type = :type")
      else:
        query = text("SELECT invest_capital, invest_percent FROM user_risk_apt WHERE user_email = :user_email AND ticker_type = :type")
    
      result = conn.execute(query, {"user_email": user_email_id, "type": type})
    
      for row in result.all():
        user_risk.append(row)
  except Exception as e:
    app.logger.error(f'An error occurred in load_risk_apt_from_db: {e}', exc_info=True)
  
  return user_risk or []

# DB related functions ENDS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# All view and redirects link !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# COMMON PAGES
@app.route("/")
def home():
  return render_template('login-page.html')

@app.route("/loginpage")
def loginpage():
  return render_template('login-page.html')

@app.route("/register", methods=['GET'])
def user_register():
  app.logger.info('user_register requested....')
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
  db_session = Session()

  try:
      # Query the user by username
      user = db_session.query(User).filter_by(Email=email).first()

      if user:
          # Update the user's details
          #print("=>",user.UserPassword)
          #print("=>",new_pass)
          if user.UserPassword == new_pass:
            user.UserPassword = new_pass
            flash('New password and existing password are same !', 'info')
          else:
            user.UserPassword = new_pass
            flash('Password updated successfully !', 'info')

          # Commit the session to save changes to the database
          db_session.commit()
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_pass: {e}', exc_info=True)
      flash('Sorry! Unable to reset the password, contact Administrator !', 'error')
      return redirect(url_for('loginpage'))
  finally:
      db_session.close()  # Close the session

  return redirect(url_for('loginpage'))


@app.route("/reset_pass")
def reset_pass():
  return render_template('reset-pass.html')


#Dashboard modules - Admin ||||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/admindashboard")
@login_required
def dashboard_admin():
  return render_template('/admin/dashboard-admin.html', user=current_user)

@app.route("/createticker")
@login_required
def create_ticker():
  return render_template('/admin/ticker-create.html', user=current_user)

@app.route("/showadmintickers")
@login_required
def show_tickers_admin():
  admintickers = load_tickers_for_admin()
  alltargets = load_targets_from_db()
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
          "trail_stop": row[9],
          "ticker_type": row[10],
          "ticker_status": row[11],
          "ticker_notes": row[12]
      } for row in admintickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/show-ticker-admin.html', grouped_tickers=grouped_tickers, targets=alltargets, user=current_user)

  
@app.route("/showusers")
def show_users():
  allusers = load_users_from_db()
  return render_template('/admin/show-users.html', users=allusers, user=current_user)

@app.route('/show_ticker_targets')
def show_ticker_targets():
  alltargets = load_targets_from_db()
  return render_template('/admin/update-targets.html', targets=alltargets, user=current_user)

@app.route('/update_ticker_targets', methods=['POST'])
@login_required
def update_ticker_targets():
  app.logger.error('update_ticker_targets: ')
  
  
  swingtickername = request.form['swing-ticker-type']
  swingtarget1 = float(request.form['swing-target-1'])
  swingtarget2 = float(request.form['swing-target-2'])
  swingtarget3 = float(request.form['swing-target-3'])
  swingtarget4 = float(request.form['swing-target-4'])

  investtickername = request.form['invest-ticker-type']
  investtarget1 = float(request.form['investment-target-1'])
  investtarget2 = float(request.form['investment-target-2'])
  investtarget3 = float(request.form['investment-target-3'])
  investtarget4 = float(request.form['investment-target-4'])

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()


  try:
    target = db_session.query(Targets).filter_by(ticker_type=swingtickername).first()
    
    if target:
      app.logger.info('update_ticker_targets: updating ticker-type : '+ str(swingtickername))
      
      target.target1=swingtarget1
      target.target2=swingtarget2
      target.target3=swingtarget3
      target.target4=swingtarget4
      

    # Commit the session to save changes to the database
    db_session.commit()

    target = db_session.query(Targets).filter_by(ticker_type=investtickername).first()
    
    if target:
      app.logger.info('update_ticker_targets: updating ticker-type : '+ str(swingtickername))
      
      target.target1=investtarget1
      target.target2=investtarget2
      target.target3=investtarget3
      target.target4=investtarget4
      

    # Commit the session to save changes to the database
    db_session.commit()
  except Exception as e:
    db_session.rollback()  # Rollback in case of error
    app.logger.error(f'An error occurred in update_ticker_targets: {e}', exc_info=True)
    #return f'An error occurred while adding ticker in DB: {e}'
    flash('An error occurred while creating new Target, Seems like same Ticker Type exists!', 'error')
    #return render_template('/admin/dashboard-admin.html')
  finally:
    db_session.close()  # Close the session

  alltargets = load_targets_from_db()
  return render_template('/admin/update-targets.html', targets=alltargets, user=current_user)


#Dashboard modules - Users |||||||||||||||||||||||||||||||||||||||||||||||||||||

@app.route("/show_ticker_user_watchlist")
@login_required
def show_ticker_user_watchlist():
  if DB_ENV == 'NP':
    watchlist = load_tickers_for_watchlist()
    # Convert to dictionary
    tickers = [
        {
            "created_date": row[0],
            "ticker_name": row[1],
            "entry_price": row[2],
            #"stop_price": row[3],
            #"target_1": row[4],
            #"target_2": row[5],
            #"target_3": row[6],
            #"target_4": row[7],
            #"trail_stop": row[8],
            #"ticker_notes": row[9]
            "TickerStatus": row[10],
            "ticker_type": row[12]
        } for row in watchlist
    ]
    # Group tickers by created date
    grouped_tickers = defaultdict(list)
    for ticker in tickers:
      date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
      grouped_tickers[date_only].append(ticker)

    return render_template('/users/show-tickers-watchlist.html', grouped_tickers=grouped_tickers, user=current_user)
  else:
    if 'userloggedinemail' in session:  # Check if user is logged in
      watchlist = load_tickers_for_watchlist()
      # Convert to dictionary
      tickers = [
          {
              "created_date": row[0],
              "ticker_name": row[1],
              "entry_price": row[2],
              #"stop_price": row[3],
              #"target_1": row[4],
              #"target_2": row[5],
              #"target_3": row[6],
              #"target_4": row[7],
              #"trail_stop": row[8],
              "TickerStatus": row[10],
              "ticker_type": row[12]
          } for row in watchlist
      ]
      # Group tickers by created date
      grouped_tickers = defaultdict(list)
      for ticker in tickers:
        date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
        grouped_tickers[date_only].append(ticker)

      return render_template('/users/show-tickers-watchlist.html', grouped_tickers=grouped_tickers, user=current_user)
    else:
      app.logger.error('Session is not valid for show_ticker_user_watchlist')
      return render_template('login-page.html')
  
@app.route("/show_ticker_user_trading")
@login_required
def show_ticker_user_trading():

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  if DB_ENV == 'NP':
    user_email_id = 'test@gmail.com'
    # Get capital and risk for the user from table
    try:
      risk_apt = db_session.query(UserRiskApt).filter_by(user_email=user_email_id).first()
    
      if risk_apt:
        app.logger.info('show_ticker_user_trading: risk-apt found for user  : '+ str(user_email_id)) 
        capital = risk_apt.swing_capital
        risk_apt_percent = risk_apt.swing_percent
      else:
        app.logger.info('show_ticker_user_trading: risk-apt not found for user  : '+ str(user_email_id)) 
        capital = 0
        risk_apt_percent = 0

    except Exception as e:
      app.logger.error(f'An error occurred in show_ticker_user_trading: {e}', exc_info=True)
    finally:
      db_session.close()  # Close the session
  
  else:
    user_email_id = session['userloggedinemail']

    # Get capital and risk for the user from table
    try:
      risk_apt = db_session.query(UserRiskApt).filter_by(user_email=user_email_id).first()
    
      if risk_apt:
        app.logger.info('show_ticker_user_trading: risk-apt found for user  : '+ str(user_email_id)) 
        capital = risk_apt.swing_capital
        risk_apt_percent = risk_apt.swing_percent
      else:
        app.logger.info('show_ticker_user_trading: risk-apt not found for user  : '+ str(user_email_id)) 
        capital = 0
        risk_apt_percent = 0

    except Exception as e:
      app.logger.error(f'An error occurred in show_ticker_user_trading: {e}', exc_info=True)
    finally:
      db_session.close()  # Close the session

  if DB_ENV == 'NP':
    ticklist = load_tickers_for_trading()
    # Convert to dictionary
    tickers = [
        {
            "created_date": row[0],
            "ticker_name": row[1],
            "entry_price": row[2],
            "stop_price": row[3],
            "target_1": row[4],
            "target_2": row[5],
            "target_3": row[6],
            "target_4": row[7],
            "trail_stop": row[8],
            "TickerStatus": row[9],
            "ticker_qty": round(((float(capital) * float(risk_apt_percent)) / 100) / (float(row[2]) - float(row[3]))),
          "ticker_notes": row[11]
        } for row in ticklist
    ]
    # Group tickers by created date
    grouped_tickers = defaultdict(list)
    for ticker in tickers:
      date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
      grouped_tickers[date_only].append(ticker)

    return render_template('/users/show-tickers-trading.html', grouped_tickers=grouped_tickers, user=current_user)
  else:
    if 'userloggedinemail' in session:  # Check if user is logged in
      ticklist = load_tickers_for_trading()
      # Convert to dictionary
      tickers = [
          {
              "created_date": row[0],
              "ticker_name": row[1],
              "entry_price": row[2],
              "stop_price": row[3],
              "target_1": row[4],
              "target_2": row[5],
              "target_3": row[6],
              "target_4": row[7],
              "trail_stop": row[8],
              "TickerStatus": row[9],
              "ticker_qty": round(((float(capital) * float(risk_apt_percent)) / 100) / (float(row[2]) - float(row[3]))),
              "ticker_notes": row[11]
          } for row in ticklist
      ]
      # Group tickers by created date
      grouped_tickers = defaultdict(list)
      for ticker in tickers:
        date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
        grouped_tickers[date_only].append(ticker)

      return render_template('/users/show-tickers-trading.html', grouped_tickers=grouped_tickers, user=current_user)
    else:
      return render_template('login-page.html')
  

@app.route("/show_ticker_user_investment")
@login_required
def show_ticker_user_investment():
  if DB_ENV == 'NP':
    ticklist = load_tickers_for_investment()
    # Convert to dictionary
    tickers = [
        {
            "created_date": row[0],
            "ticker_name": row[1],
            "entry_price": row[2],
            "stop_price": row[3],
            "target_1": row[4],
            "target_2": row[5],
            "target_3": row[6],
            "target_4": row[7],
            "trail_stop": row[8],
            "TickerStatus": row[9],
            "ticker_notes": row[10]
        } for row in ticklist
    ]
    # Group tickers by created date
    grouped_tickers = defaultdict(list)
    for ticker in tickers:
      date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
      grouped_tickers[date_only].append(ticker)

    return render_template('/users/show-tickers-investment.html', grouped_tickers=grouped_tickers, user=current_user)
  else:
    if 'userloggedinemail' in session:  # Check if user is logged in
      ticklist = load_tickers_for_investment()
      # Convert to dictionary
      tickers = [
          {
              "created_date": row[0],
              "ticker_name": row[1],
              "entry_price": row[2],
              "stop_price": row[3],
              "target_1": row[4],
              "target_2": row[5],
              "target_3": row[6],
              "target_4": row[7],
              "trail_stop": row[8],
              "TickerStatus": row[9],
              "ticker_notes": row[10]
          } for row in ticklist
      ]
      # Group tickers by created date
      grouped_tickers = defaultdict(list)
      for ticker in tickers:
        date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
        grouped_tickers[date_only].append(ticker)

      return render_template('/users/show-tickers-investment.html', grouped_tickers=grouped_tickers, user=current_user)
    else:
      return render_template('login-page.html')


# RISK APETITE !!!!!! $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  !!!!!! 
@app.route('/show_user_trading_risk_apt')
def show_user_risk_apt():
  if DB_ENV == 'NP':
    user_email_id = 'test@gmail.com'
  else:
    user_email_id = session['userloggedinemail']

  user_risk_apt = load_risk_apt_from_db(user_email_id,"Swing")
  
  if not user_risk_apt:
    app.logger.info("No user risk data returned from the database.")
    update_risk_apt_table(user_email_id,"Swing","0","0.00")
    user_risk_apt = load_risk_apt_from_db(user_email_id,"Swing")
    
  return render_template('/users/update-risk-apt.html', user_risk=user_risk_apt, user=current_user)

@app.route('/update_risk_apetite_for_trading', methods=['POST'])
def update_risk_apetite_for_trading():
  app.logger.info('update_risk_apetite_for_trading calling ...')
  ticklist = load_tickers_for_trading()
  
  if not ticklist:
    app.logger.error("No tickers found for trading.")
  
  ticker_type = 'Swing'
  capital = request.form['total-capital-price']
  risk_apt_percent = float(request.form['risk-apetite-percent'].replace('$', '').replace(',', ''))
  #app.logger.info("=ticker_qty=>>"+ str(((float(capital) * float(risk_apt_percent)) / 100) / (float(row[2]) - float(row[3]))))

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  if DB_ENV == 'NP':
    user_email_id = 'test@gmail.com'
    # Update DB with user defined risk apetite
    update_risk_apt_table(user_email_id,ticker_type,capital,risk_apt_percent)
    # Get capital and risk for the user from table
    try:
      risk_apt = db_session.query(UserRiskApt).filter_by(user_email=user_email_id).first()
    
      if risk_apt:
        app.logger.info('update_risk_apetite_for_trading: risk-apt found for user  : '+ str(user_email_id)) 
        capital = risk_apt.swing_capital
        risk_apt_percent = risk_apt.swing_percent
      else:
        app.logger.info('update_risk_apetite_for_trading: risk-apt not found for user  : '+ str(user_email_id)) 
        capital = 0
        risk_apt_percent = 0

    except Exception as e:
      app.logger.error(f'An error occurred in update_risk_apetite_for_trading: {e}', exc_info=True)
    finally:
      db_session.close()  # Close the session
  else:
    user_email_id = session['userloggedinemail']
    # Update DB with user defined risk apetite
    update_risk_apt_table(user_email_id,ticker_type,capital,risk_apt_percent)
    
    # Get capital and risk for the user from table
    try:
      risk_apt = db_session.query(UserRiskApt).filter_by(user_email=user_email_id).first()
    
      if risk_apt:
        app.logger.info('update_risk_apetite_for_trading: risk-apt found for user  : '+ str(user_email_id)) 
        capital = risk_apt.swing_capital
        risk_apt_percent = risk_apt.swing_percent
      else:
        app.logger.info('update_risk_apetite_for_trading: risk-apt not found for user  : '+ str(user_email_id)) 
        capital = 0
        risk_apt_percent = 0

    except Exception as e:
      app.logger.error(f'An error occurred in update_risk_apetite_for_trading: {e}', exc_info=True)
    finally:
      db_session.close()  # Close the session

  
  
  #round() will round 5.9 to 6 and 5.4 to 5.
  #int() will 5.9 becomes 5
  # Convert to dictionary
  tickers = [
      {
          "created_date": row[0],
          "ticker_name": row[1],
          "entry_price": row[2],
          "stop_price": row[3],
          "target_1": row[4],
          "target_2": row[5],
          "target_3": row[6],
          "target_4": row[7],
          "trail_stop": row[8],
          "ticker_qty": round(((float(capital) * float(risk_apt_percent)) / 100) / (float(row[2]) - float(row[3]))),
          "ticker_notes": row[10]
      } for row in ticklist
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/users/show-tickers-trading.html', grouped_tickers=grouped_tickers, user=current_user)


#### UPDATE RISK APT TABLE

def update_risk_apt_table(user_email_id,ticker_type,capital,risk_apt_percent):
  app.logger.info('update_risk_apt_table for user : '+ str(user_email_id))

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
    risk_apt = db_session.query(UserRiskApt).filter_by(user_email=user_email_id).first()
    
    if risk_apt:
      app.logger.info('update_ticker_targets: updating ticker-type : '+ str(user_email_id))
      
      if ticker_type == 'Swing':
        risk_apt.ticker_type=ticker_type
        risk_apt.swing_capital=capital
        risk_apt.swing_percent=risk_apt_percent
      else:
        risk_apt.ticker_type=ticker_type
        risk_apt.invest_capital=capital
        risk_apt.invest_percent=risk_apt_percent
    else:
      app.logger.info('update_ticker_targets: adding risk_apt for user : '+ str(user_email_id))

      if ticker_type == 'Swing':
        new_user_risk_apt = UserRiskApt(user_email=user_email_id,
                                        ticker_type=ticker_type,
                                        swing_capital=capital,
                                        swing_percent=risk_apt_percent)
      else:
        new_user_risk_apt = UserRiskApt(user_email=user_email_id,
                                        ticker_type=ticker_type,
                                        invest_capital=capital,
                                        invest_percent=risk_apt_percent)

      # Add the new user to the session
      db_session.add(new_user_risk_apt)

    # Commit the session to save changes to the database
    db_session.commit()

  except Exception as e:
    db_session.rollback()  # Rollback in case of error
    app.logger.error(f'An error occurred in update_ticker_targets: {e}', exc_info=True)
    #return f'An error occurred while adding ticker in DB: {e}'
    flash('An error occurred while creating new Target, Seems like same Ticker Type exists!', 'error')
    #return render_template('/admin/dashboard-admin.html')
  finally:
    db_session.close()  # Close the session


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
  country_code = Column(String, nullable=False)
  mobile_number = Column(String, nullable=False)
  

  #generated
  # Example attributes
  # Define the __init__ method to handle the fields
  def __init__(self, username, email, userpassword, userrole,country_code,mobile_number):
      self.UserName = username
      self.Email = email
      self.UserPassword = userpassword
      self.UserRole = userrole
      self.country_code = country_code
      self.mobile_number = mobile_number

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
db_session = Session()

# CREATE USER .............................................................
@app.route('/create_user', methods=['POST'])
def create_user():
  email = request.form['email']
  username = request.form['username']
  if len(username) == 0:
     username = request.form['email']

  password = request.form['psw']
  concode = request.form['country-code']
  mobnumber = request.form['mobile-number']

  #role = request.form['users']
  role = "General"
  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()
  app.logger.info('create_user: Loggin with user email : '+ str(request.form['email'])+ " / " +str(request.form['username'])
                  + " / " +str(request.form['mobile-number'])+ " / " +str(role))
  try:
    # Query the user by username and password
    user = db_session.query(User).filter_by(Email=email, UserPassword=password).first()
    # Add the new user to the session
    #print("==>" , user.UserName)
    #print("==>" , user.UserRole)
    if user:
       print('User is already registered.')
       flash('User is already registered. Please check your email !', 'error')
    else:
      # Create a new user instance
      new_user = User(username=username,
                  email=email,
                  userpassword=password,
                  userrole=role,
                  country_code=concode,
                  mobile_number=mobnumber)

      # Add the new user to the session
      db_session.add(new_user)

      # Commit the session to save changes to the database
      db_session.commit()
      app.logger.debug('create_user: User created with user email : '+ str(request.form['email'])+ " / " +str(request.form['username'])
                    + " / " +str(request.form['psw'])+ " / " +str(role))
      flash('Registration successful! please check your email for further information !', 'info')
      
      #Email send...
      app.logger.info('Sending email to new register user....')
      #email = request.form['email']
      to_email = email
      # Create the welcome message
      subject = "Welcome to Team Investinbulls!"
      #message_body = f"Dear {username},\n\nThank you for joining us! \n\nEach morning, you’ll receive a list of stocks that have the potential to breakout during the day. \nOnce the breakout happens, we will send you an alert directly to your email or text message. \nThis alert will include important details such as the breakout price, target levels, and a predefined stop loss to manage your risk effectively..\n\nBest Regards,\nInvestinbulls.net"
      message_body = f"Dear {username},\n\nThank you for joining Team Investinbulls! We’re excited to have you on board. \n\nYou have successfully registered with the following credentials:\n\nLogin: {email}\n\nPassword: {password}\n\nEach morning, you’ll receive a Watchlist of stocks with potential breakout opportunities. Once a breakout occurs, we will send you an alert directly to your email. This alert will include key details such as:\n\nBreakout Price\nEntry Price\nTarget Levels\nPredefined Stop Loss\nThese insights are designed to help you manage your risk effectively.\n\nIf you have any questions, feel free to reach out.\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      try:
        send_email(mail, to_email, subject, message_body)
        #return jsonify({"status": "success", "email_status": send_status})
      except Exception as e:
        app.logger.error(f'An error occurred in create_user send_email: {e}', exc_info=True)
        #return jsonify({"status": "error", "error": str(e)}), 500
  except Exception as e:
    db_session.rollback()  # Rollback in case of error
    flash('Facing some issue while user registration. Try later !', 'error')
    app.logger.error(f'An error occurred in create_user: {e}', exc_info=True)
    return render_template('user-register.html')
    #return f'An error occurred: {e}'
  finally:
    db_session.close()  # Close the session    

  return render_template('user-register.html')
  #return 'User created successfully'


# Admin will send email to all users
@app.route('/send_email_to_all', methods=['POST'])
def send_email_to_all():
    app.logger.info("send_email_to_all")
    data = request.json
    subject = data.get("subject")
    body = data.get("body")  # HTML content, including pasted images
    
    try:
        #get all email address 
        allusers = load_users_details_from_db()

        for user in allusers:
          #Email send...
          #app.logger.info('Preparing email for registered email : '+ str(user.Email))
          #email = request.form['email']
          to_email = user.Email

          #to_email = "chatterjee.paromita9@gmail.com"
          app.logger.info('Sending personalized email to registered email : '+ str(to_email))

          try:
            send_status = send_email_to_users(mail, to_email, subject, body)
            #return jsonify({"status": "success", "email_status": send_status})
          except Exception as e:
            app.logger.error(f'An error occurred in send_email_to_all send_email: {e}', exc_info=True)

        return jsonify({"message": send_status})
    except Exception as e:
      app.logger.error(f"An error occurred in send_email_to_all while sending emails: {e}", exc_info=True)
      return jsonify({"status": "error"}), 500

@app.route('/delete_user', methods=['POST'])
def delete_user():
  email = request.form['user_id']

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
      # Query the user by username
      user = db_session.query(User).filter_by(Email=email).first()

      if user:
          # Delete the user from the session
          db_session.delete(user)

          # Commit the session to remove the user from the database
          db_session.commit()
          flash('User deleted successfully !', 'info')
      else:
          flash('User not found !', 'error')
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      flash('Problem occured in databse while deleting !', 'error')
      app.logger.error(f'An error occurred in delete_user: {e}', exc_info=True)
      #return f'An error occurred: {e}'
  finally:
      db_session.close()  # Close the session

  return redirect(url_for('manageuser'))


@app.route('/promote_user', methods=['POST'])
def promote_user():
    email = request.form['user_id']  # Get the email from the form

    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        user = db_session.query(User).filter_by(Email=email).first()

        if user:
            # Promote the user to 'Admin'
            user.UserRole = 'Admin'

            # Commit the session to save changes to the database
            db_session.commit()
            flash('User promoted to Admin successfully!', 'info')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while promoting user!', 'error')
        app.logger.error(f'An error occurred in promote_user: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

    return redirect(url_for('manageuser'))



@app.route('/demote_user', methods=['POST'])
def demote_user():
    email = request.form['user_id']  # Get the email from the form

    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        user = db_session.query(User).filter_by(Email=email).first()

        if user:
            # Promote the user to 'Admin'
            user.UserRole = 'General'

            # Commit the session to save changes to the database
            db_session.commit()
            flash('User demoted to General successfully!', 'info')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while demoting user!', 'error')
        app.logger.error(f'An error occurred in demote_user: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

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
  TrailStop  = Column(Integer, nullable=False)
  ticker_qty  = Column(Integer, nullable=False)
  TickerStatus  = Column(String, nullable=False)
  TickerNotes = Column(Text, nullable=True)  # New column for storing notes
  ticker_type  = Column(String, nullable=False)
  # Timestamps
  #CreateDate = Column(DateTime)  # On insert
  #UpdateDate = Column(DateTime)  # On insert and update
  # Timestamps
  CreateDate = Column(DateTime, default=func.now())  # On insert
  #UpdateDate = Column(DateTime, default=func.now(), onupdate=func.now())  # On insert and update
  UpdateDate = Column(DateTime, default=func.now())  # On insert and update


class Targets(Base):
    __tablename__ = 'ticker_targets'
    
    ticker_type = Column(String(255), primary_key=True, nullable=False, default='Unknown')
    target1 = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    target2 = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    target3 = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    target4 = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    created_by = Column(String(255), nullable=False, default='Admin')
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now())

class UserRiskApt(Base):
    __tablename__ = 'user_risk_apt'

    # Columns
    user_email = Column(String, primary_key=True, nullable=False)
    ticker_type = Column(String, primary_key=True, nullable=False)
    swing_capital = Column(Integer, nullable=False, default=0)
    swing_percent = Column(Float, nullable=False, default=0.0)
    invest_capital = Column(Integer, nullable=False, default=0)
    invest_percent = Column(Float, nullable=False, default=0.0)
    updated_time = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (f"<UserRiskApt(user_email={self.user_email}, "
                f"ticker_type={self.ticker_type}, swing_capital={self.swing_capital}, "
                f"swing_percent={self.swing_percent}, invest_capital={self.invest_capital}, "
                f"invest_percent={self.invest_percent}, "
                f"updated_time={self.updated_time})>")


## THIS METHOS IS NOT IN USE ANYMORE -- WILL REMOVE LATER  
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
  tickertype = request.form['type']
  trailStop = 0
  tickerstatus = "Inactive"
  notes = request.form['notes']

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

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
                    TrailStop=trailStop,
                    TickerStatus=tickerstatus,
                    TickerNotes=notes,
                    ticker_type=tickertype)

    # Add the new user to the session
    db_session.add(new_ticker)

    # Commit the session to save changes to the database
    db_session.commit()
  except Exception as e:
    db_session.rollback()  # Rollback in case of error
    app.logger.error(f'An error occurred in save_ticker: {e}', exc_info=True)
    #return f'An error occurred while adding ticker in DB: {e}'
    #flash('An error occurred while creating new Ticker, Seems like same Ticker Name exists!', 'error')
    return render_template('/admin/dashboard-admin.html', user=current_user)
  finally:
    db_session.close()  # Close the session

  return render_template('/admin/dashboard-admin.html', user=current_user)

@app.route('/save_ticker_new', methods=['POST'])
def save_ticker_new():
  username = "Admin" #session['username']
  trailStop = 0
  tickerQty = 0
  tickerstatus = "Inactive"

  tickername = request.form['tickername']
  entryprice = float(request.form['entryprice'].replace('$', '').replace(',', ''))
  stoppercent = float(request.form['stoppercent'].replace('$', '').replace(',', ''))
  stopprice = float(request.form['stopprice'].replace('$', '').replace(',', ''))
  target1 = float(request.form['target1'].replace('$', '').replace(',', ''))
  target2 = float(request.form['target2'].replace('$', '').replace(',', ''))
  target3 = float(request.form['target3'].replace('$', '').replace(',', ''))
  target4 = float(request.form['target4'].replace('$', '').replace(',', ''))
  tickertype = request.form['tickertype']
  notes = request.form['notes']

  # Retrieve data from request.json
  """data = request.json
  
  # Extract values and store them in variables
  tickername = data.get('ticker_name')
  entryprice = float(data.get('entry_price').replace('$', '').replace(',', ''))
  stoppercent = float(data.get('stop_percent').replace('$', '').replace(',', ''))
  stopprice = float(data.get('stop_price').replace('$', '').replace(',', ''))
  target1 = float(data.get('target_1').replace('$', '').replace(',', ''))
  target2 = float(data.get('target_2').replace('$', '').replace(',', ''))
  target3 = float(data.get('target_3').replace('$', '').replace(',', ''))
  target4 = float(data.get('target_4').replace('$', '').replace(',', ''))
  tickertype = data.get('ticker_type')
  notes = data.get('ticker_notes')
  tickerstatus = "Inactive"""
  
  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

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
                    TrailStop=trailStop,
                    ticker_type=tickertype,
                    ticker_qty=tickerQty,
                    TickerStatus=tickerstatus,
                    TickerNotes=notes
                    )

    # Add the new user to the session
    db_session.add(new_ticker)

    # Commit the session to save changes to the database
    db_session.commit()
  except Exception as e:
    db_session.rollback()  # Rollback in case of error
    app.logger.error(f'An error occurred in save_ticker_new: {e}', exc_info=True)
    #return f'An error occurred while adding ticker in DB: {e}'
    flash('An error occurred while creating new Ticker, Seems like same Ticker Name exists!', 'error')
    #return render_template('/admin/dashboard-admin.html')
  finally:
    db_session.close()  # Close the session

  #added:
  admintickers = load_tickers_for_admin()
  alltargets = load_targets_from_db()
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
          "trail_stop": row[9],
          "ticker_type": row[10],
          "ticker_status": row[11],
          "ticker_notes": row[12]
      } for row in admintickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/show-ticker-admin.html', grouped_tickers=grouped_tickers, targets=alltargets, user=current_user)


@app.route('/update_ticker', methods=['POST'])
def update_ticker():
  app.logger.info('update_ticker: data : '+ str(request.json))

  username = "Admin" #session['username']
  tickerstatus = "Active"
  # Retrieve data from request.json
  data = request.json
  
  # Extract values and store them in variables
  created_date = data.get('created_date')
  ticker_name = data.get('ticker_name')
  entry_price = float(data.get('entry_price').replace('$', '').replace(',', ''))
  stop_percent = float(data.get('stop_percent').replace('$', '').replace(',', ''))
  stop_price = float(data.get('stop_price').replace('$', '').replace(',', ''))
  target_1 = float(data.get('target_1').replace('$', '').replace(',', ''))
  target_2 = float(data.get('target_2').replace('$', '').replace(',', ''))
  target_3 = float(data.get('target_3').replace('$', '').replace(',', ''))
  target_4 = float(data.get('target_4').replace('$', '').replace(',', ''))
  trail_stop = float(data.get('trail_stop').replace('$', '').replace(',', ''))
  ticker_type = data.get('ticker_type')
  status = data.get('ticker_status')
  ticker_notes = data.get('ticker_notes')

  if target_3 is None: 
     target_3 = 0
  if target_4 is None: 
     target_4 = 0
     

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()
  #print("==>",ticker_name)
  #print("==>",created_date)
  try:
    ticker = db_session.query(Ticker).filter_by(TickerName=ticker_name, CreateDate=created_date).first()
    
    if ticker:
      app.logger.info('update_ticker: updating ticker : '+ str(ticker_name))
      ticker.EntryPrice=entry_price
      ticker.StopPercent=stop_percent
      ticker.StopPrice=stop_price
      ticker.Target1=target_1
      ticker.Target2=target_2
      ticker.Target3=target_3
      ticker.Target4=target_4
      ticker.TrailStop=trail_stop
      ticker.ticker_type=ticker_type
      ticker.TickerStatus=status
      ticker.TickerNotes=ticker_notes
      # Commit the session to save changes to the database
      db_session.commit()

      if status == "Active":
         send_active_broadcast_email(ticker)
      else:
         app.logger.info('update_ticker: not sending broadcast email as Ticker Status : '+ str(status))

    """else:
      app.logger.info('update_ticker: adding a new ticker : '+ str(ticker_name))
      # Create a new user instance
      new_ticker = Ticker(UserName=username,
                      TickerName=ticker_name,
                      EntryPrice=entry_price,
                      StopPercent=stop_percent,
                      StopPrice=stop_price,
                      Target1=target_1,
                      Target2=target_2,
                      Target3=target_3,
                      Target4=target_4,
                      ticker_type=ticker_type,
                      TickerStatus=tickerstatus,
                      TickerNotes=ticker_notes)

      # Add the new user to the session
      db_session.add(new_ticker)"""

    return jsonify(success=True)
  except:
      flash('Problem occured in database while updating Ticker !', 'error')
      app.logger.error(f'An error occurred in update_ticker: {jsonify(success=False)}', exc_info=True)
      #return jsonify(success=False)
  finally:
    db_session.close()  # Close the session

  #added:
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
          "trail_stop": row[9],
          "ticker_status": row[10],
          "ticker_notes": row[11]
      } for row in admintickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/show-ticker-admin.html', grouped_tickers=grouped_tickers, user=current_user)


@app.route('/active_ticker', methods=['POST'])
def active_ticker():
    tickername = request.form['ticker_name']
    createddate = request.form['created_date']
   
    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        ticker = db_session.query(Ticker).filter_by(TickerName=tickername, CreateDate=createddate).first()

        if ticker:
            # Promote the ticker to 'Active'
            ticker.TickerStatus = 'Active'
            #ticker.UpdateDate = datetime.now()
            ticker.UpdateDate = func.now()
            # Commit the session to save changes to the database
            db_session.commit()
            #flash('Ticker updated : Active!', 'info')
            # Create a separate thread to run the send_msg method with an argument
            #thread = threading.Thread(target=send_active_broadcast_email, args=(ticker,))
            #thread.start()  # Start the thread
            send_active_broadcast_email(ticker)
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while making Active ticker!', 'error')
        app.logger.error(f'An error occurred in active_ticker: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

    return redirect(url_for('manageticker'))

#Broadcast email on active ticker
def send_active_broadcast_email(ticker):
  app.logger.info('send_active_broadcast_email for ticker : '+ str(ticker.TickerName))
  
  try:
    #get all email address 
    allusers = load_users_details_from_db()

    for user in allusers:
      #Email send...
      app.logger.info('Preparing email for registered email : '+ str(user.Email))
      #email = request.form['email']
      to_email = user.Email

      today = date.today()
      # Create the welcome message
      subject = f"Team Investinbulls Stock update {ticker.TickerName} - {today}"

      message_body = f"Dear {user.UserName},\n\nStock {ticker.TickerName} is active to trade now.\nEntry Price : {ticker.EntryPrice}\nStop Price : {ticker.StopPrice}\nTarget-1 : {ticker.Target1}\nTarget-2 : {ticker.Target2}\nTarget-3 : {ticker.Target3}\nTarget-4 : {ticker.Target4}\nTrailstop : {ticker.TrailStop}\nTicker Notes : {ticker.TickerNotes}\n\nPlease login to www.investinbulls.net for more details.\n\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      
      #message_body = f"Dear {username},\n\nThank you for joining us! \n\nEach morning, you’ll receive a list of stocks that have the potential to breakout during the day. \nOnce the breakout happens, we will send you an alert directly to your email or text message. \nThis alert will include important details such as the breakout price, target levels, and a predefined stop loss to manage your risk effectively..\n\nBest Regards,\nInvestinbulls.net"
      if ticker.Target3 == 0.00 and ticker.Target4 == 0.00:
        message_body = f"Dear {user.UserName},\n\nStock {ticker.TickerName} is active to trade now.\nEntry Price : {ticker.EntryPrice}\nStop Price : {ticker.StopPrice}\nTarget-1 : {ticker.Target1}\nTarget-2 : {ticker.Target2}\nTarget-3 : TBD \nTarget-4 : TBD \nTrailstop : {ticker.TrailStop}\nTicker Notes : {ticker.TickerNotes}\n\nPlease login to www.investinbulls.net for more details.\n\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      elif ticker.Target3 != 0.00 and ticker.Target4 == 0.00:
        message_body = f"Dear {user.UserName},\n\nStock {ticker.TickerName} is active to trade now.\nEntry Price : {ticker.EntryPrice}\nStop Price : {ticker.StopPrice}\nTarget-1 : {ticker.Target1}\nTarget-2 : {ticker.Target2}\nTarget-3 : {ticker.Target3}\nTarget-4 : TBD \nTrailstop : {ticker.TrailStop}\nTicker Notes : {ticker.TickerNotes}\n\nPlease login to www.investinbulls.net for more details.\n\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      elif ticker.Target3 == 0.00 and ticker.Target4 != 0.00:
        message_body = f"Dear {user.UserName},\n\nStock {ticker.TickerName} is active to trade now.\nEntry Price : {ticker.EntryPrice}\nStop Price : {ticker.StopPrice}\nTarget-1 : {ticker.Target1}\nTarget-2 : {ticker.Target2}\nTarget-3 : TBD \nTarget-4 : {ticker.Target4}\nTrailstop : {ticker.TrailStop}\nTicker Notes : {ticker.TickerNotes}\n\nPlease login to www.investinbulls.net for more details.\n\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      else:
        message_body = f"Dear {user.UserName},\n\nStock {ticker.TickerName} is active to trade now.\nEntry Price : {ticker.EntryPrice}\nStop Price : {ticker.StopPrice}\nTarget-1 : {ticker.Target1}\nTarget-2 : {ticker.Target2}\nTarget-3 : {ticker.Target3}\nTarget-4 : {ticker.Target4}\nTrailstop : {ticker.TrailStop}\nTicker Notes : {ticker.TickerNotes}\n\nPlease login to www.investinbulls.net for more details.\n\n\nBest Regards,\nInvestinbulls.net\nwww.investinbulls.net"
      
      try:
        #app.logger.info('Subject: '+ str(subject))
        #app.logger.info('Email-Body: '+ str(message_body))
        #thread = threading.Thread(target=send_email, args=(mail, to_email, subject, message_body))
        #thread.start()  # Start the thread
        # paromita2k4@gmail.com / chatterjee.paromita9@gmail.com / vikram@investinbulls.net
        #if to_email == "chatterjee.paromita9@gmail.com":
        app.logger.info('Sending email to registered email : '+ str(to_email))
        send_email(mail, to_email, subject, message_body)

        #return jsonify({"status": "success", "email_status": send_status})
        time.sleep(1)
      except Exception as e:
        app.logger.error(f'An error occurred in send_active_broadcast_email send_email: {e}', exc_info=True)
  except Exception as e:
    app.logger.error(f'An error occurred in send_active_broadcast_email: {e}', exc_info=True)

# This function is not in use
@app.route('/inactive_ticker', methods=['POST'])
def inactive_ticker():
    tickername = request.form['ticker_name']
    createddate = request.form['created_date']
    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        ticker = db_session.query(Ticker).filter_by(TickerName=tickername, CreateDate=createddate).first()

        if ticker:
            # Promote the ticker to 'Incctive'
            ticker.TickerStatus = 'Inactive'

            # Commit the session to save changes to the database
            db_session.commit()
            #flash('Ticker updated : Inactive!', 'info')
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while makeing Inactive ticker!', 'error')
        app.logger.error(f'An error occurred in inactive_ticker: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

    return redirect(url_for('manageticker'))

@app.route('/profit_ticker', methods=['POST'])
def profit_ticker():
    tickername = request.form['ticker_name']
    createddate = request.form['created_date']
    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        ticker = db_session.query(Ticker).filter_by(TickerName=tickername, CreateDate=createddate).first()

        if ticker:
            # Promote the ticker to 'Incctive'
            ticker.TickerStatus = 'Profit-Book'

            # Commit the session to save changes to the database
            db_session.commit()
            #flash('Ticker updated : Inactive!', 'info')
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while makeing profit_ticker !', 'error')
        app.logger.error(f'An error occurred in profit_ticker: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

    return redirect(url_for('manageticker'))

@app.route('/loss_ticker', methods=['POST'])
def loss_ticker():
    tickername = request.form['ticker_name']
    createddate = request.form['created_date']
    # Create a session
    Session = sessionmaker(bind=engine)
    db_session = Session()

    try:
        # Query the user by email
        ticker = db_session.query(Ticker).filter_by(TickerName=tickername, CreateDate=createddate).first()

        if ticker:
            # Promote the ticker to 'Incctive'
            ticker.TickerStatus = 'Loss-Book'

            # Commit the session to save changes to the database
            db_session.commit()
            #flash('Ticker updated : Inactive!', 'info')
        else:
            flash('Ticker not found!', 'error')
    except Exception as e:
        db_session.rollback()  # Rollback in case of error
        flash('Problem occurred in database while makeing loss_ticker!', 'error')
        app.logger.error(f'An error occurred in loss_ticker: {e}', exc_info=True)
    finally:
        db_session.close()  # Close the session

    return redirect(url_for('manageticker'))

@app.route('/delete_ticker', methods=['POST'])
def delete_ticker():
  tickername = request.form['ticker_name']
  createddate = request.form['created_date']
  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
      # Query the user by username
      ticker = db_session.query(Ticker).filter_by(TickerName=tickername, CreateDate=createddate).first()

      if ticker:
          # Delete the user from the session
          db_session.delete(ticker)

          # Commit the session to remove the user from the database
          db_session.commit()
          #flash('Ticker deleted successfully !', 'info')
      else:
          flash('Ticker not found !', 'error')
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      flash('Problem occured in database while deleting !', 'error')
      app.logger.error(f'An error occurred in delete_ticker: {e}', exc_info=True)
      #return f'An error occurred: {e}'
  finally:
      db_session.close()  # Close the session

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
  db_session = Session()

  try:
      # Query the user by username and password
      user = db_session.query(User).filter_by(Email=email, UserPassword=password).first()
      # Add the new user to the session
      #print("==>" , user.UserName)
      #print("==>" , user.UserRole)
      if user:
          app.logger.info('auth_user: Successful Loggin with user email : '+ str(request.form['email']))
          #login_user(user,remember=True, duration=None, force=True, fresh=True) # Flask-Login will now work as expected
          login_user(user,remember=True) # Flask-Login will now work as expected

          session['userloggedinemail'] = email
          # User found, return user details
          if user.UserRole == "Admin":
            #return render_template('/admin/dashboard-admin.html', user=current_user)
            #return redirect(url_for('loadadmindashboard'))
            response = make_response(render_template('/admin/dashboard-admin.html', user=current_user))
            return clear_cache(response)
          else:
            #return render_template('/users/dashboard-user.html', user=current_user)
            #return redirect(url_for('loaduserdashboard'))
            response = make_response(render_template('/users/dashboard-user.html', user=current_user))
            return clear_cache(response)
      else:
          app.logger.info('auth_user: Failed Loggin with user email : '+ str(request.form['email']))
          flash('Wrong username or password! Please Try again !', 'error')
          return render_template('login-page.html')
  except Exception as e:
      app.logger.error(f'An error occurred in auth_user: {e}', exc_info=True)
      flash('Problem occured while login! Please Try later !', 'error')
      return redirect(url_for('loginpage'))
  finally:
      db_session.close()  # Close the session

@app.route("/loadadmindashboard")
@login_required
def loadadmindashboard():
  if 'userloggedinemail' in session:  # Check if user is logged in
    if current_user.is_authenticated:
      return render_template('/admin/dashboard-admin.html', user=current_user)
    else:
      return render_template('login-page.html')
  else:
    # User is not logged in, redirect to login page
    return render_template('login-page.html')
  
@app.route("/loaduserdashboard")
@login_required
def loaduserdashboard():
  if DB_ENV == 'NP':
     return render_template('/users/dashboard-user.html', user=current_user)
  else:
    if 'userloggedinemail' in session:  # Check if user is logged in
      return render_template('/users/dashboard-user.html', user=current_user)
    else:
      return render_template('login-page.html')

@app.route('/update_pass', methods=['POST', 'GET'])
def update_pass():
  email = request.form['email']
  old_pass = request.form['current-password']
  new_pass = request.form['new-password']

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
      # Query the user by username
      user = db_session.query(User).filter_by(Email=email, UserPassword=old_pass).first()

      if user:
          # Update the user's details
          if user.UserPassword == old_pass:
            user.UserPassword = new_pass
            flash('Password updated successfully !', 'info')
          else:
            flash('User existing password is not matching. Try again !', 'error')
            return redirect(url_for('update_pass'))

          # Commit the session to save changes to the database
          db_session.commit()
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_pass: {e}', exc_info=True)
      flash('Sorry! Unable to update the password, contact Administrator !', 'error')
      return redirect(url_for('update_pass'))
  finally:
      db_session.close()  # Close the session

  return redirect(url_for('logout'))

#print(__name__)

# Menu Bar functions |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||

#Admin based
@app.route("/adminpanel")
def adminpanel():
  return render_template('/admin/send-email.html', user=current_user)

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
          "trail_stop": row[9],
          "ticker_type": row[10],
          "ticker_status": row[11]
      } for row in alltickers
  ]
  # Group tickers by created date
  grouped_tickers = defaultdict(list)
  for ticker in tickers:
    date_only = ticker['created_date'].date()  # Assuming CreateDate is a datetime object
    grouped_tickers[date_only].append(ticker)

  return render_template('/admin/manage-tickers.html', grouped_tickers=grouped_tickers, user=current_user)

@app.route("/manageuser")
def manageuser():
  allusers = load_users_details_from_db()
  return render_template('/admin/user-manage.html', users=allusers, user=current_user)

@app.route("/adminprofile")
def adminprofile():
  return render_template('/admin/admin-profile.html', user=current_user)

@app.route("/adminusercreate")
def adminusercreate():
  return render_template('/admin/user-register-admin.html', user=current_user)

@app.route("/update_admin_pass")
def update_admin_pass():
  return render_template('/admin/update-pass.html', user=current_user)

#User based
@app.route("/user_notificatuons")
def user_notificatuons():
  if 'userloggedinemail' in session:  # Check if user is logged in
    return render_template('/users/draft.html', user=current_user)
  else:
    return render_template('login-page.html')

@app.route("/userprofile")
def userprofile():
  if 'userloggedinemail' in session:  # Check if user is logged in
    return render_template('/users/user-profile.html', user=current_user)
  else:
    return render_template('login-page.html')
  
@app.route("/update_user_pass")
def update_user_pass():
  if 'userloggedinemail' in session:  # Check if user is logged in
    return render_template('/users/update-pass.html', user=current_user)
  else:
    return render_template('login-page.html')
  
@app.route("/update_mobile_no")
def update_mobile_no():
  if 'userloggedinemail' in session:  # Check if user is logged in
    return render_template('/users/update-mobileno.html', user=current_user)
  else:
    return render_template('login-page.html')

@app.route('/update_user_pass_db', methods=['POST', 'GET'])
def update_user_pass_db():
  email = request.form['email']
  old_pass = request.form['current-password']
  new_pass = request.form['new-password']

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
      # Query the user by username
      user = db_session.query(User).filter_by(Email=email, UserPassword=old_pass).first()

      if user:
          # Update the user's details
          if user.UserPassword == old_pass:
            user.UserPassword = new_pass
            # Commit the session to save changes to the database
            db_session.commit()
            flash('Password updated successfully !', 'info')
          else:
            flash('User existing password is not matching. Try again !', 'error')
            return redirect(url_for('update_user_pass'))
          
          #return f'User {user} updated successfully'
      else:
          flash('Email address not found !', 'error')
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_user_pass_db: {e}', exc_info=True)
      flash('Sorry! Unable to update the password, contact Administrator !', 'error')
      return redirect(url_for('update_user_pass'))
  finally:
      db_session.close()  # Close the session

  return redirect(url_for('update_user_pass'))

@app.route('/update_mobile_no_db', methods=['POST', 'GET'])
def update_mobile_no_db():
  email = request.form['email']
  concode = request.form['country-code']
  mobnumber = request.form['mobile-number']

  # Create a session
  Session = sessionmaker(bind=engine)
  db_session = Session()

  try:
      # Query the user by username
      user = db_session.query(User).filter_by(Email=email).first()

      if user:
          # Update the user's details
          user.country_code == concode
          user.mobile_number = mobnumber
        
          # Commit the session to save changes to the database
          db_session.commit()
          #return f'User {user} updated successfully'
          flash('Mobile number updated successfully !', 'info')

      else:
          flash('Email address not found, Try again !', 'error')
          return redirect(url_for('update_mobile_no'))
      
  except Exception as e:
      db_session.rollback()  # Rollback in case of error
      app.logger.error(f'An error occurred in update_user_pass_db: {e}', exc_info=True)
      flash('Sorry! Unable to update the mobile number, contact Administrator !', 'error')
      return redirect(url_for('update_mobile_no'))
  finally:
      db_session.close()  # Close the session

  return redirect(url_for('update_mobile_no'))



#### VIDEO UPLOAD #############################################
class Video:
    def __init__(self, name, is_private=True):
        self.name = name
        self.is_private = is_private

class Folder:
  def __init__(self, name, count):
        self.name = name
        self.count = count

#Load privacy data
def load_privacy_data():
    if os.path.exists(app.config['PRIVACY_FILE']):
        with open(app.config['PRIVACY_FILE'], 'r') as f:
            return json.load(f)
    return {}

#Save privacy data
def save_privacy_data(data):
    with open(app.config['PRIVACY_FILE'], 'w') as f:
        json.dump(data, f, indent=4)

def get_private_videos():
    """Returns set of private videos"""
    private_videos = set()
    if os.path.exists(app.config['PRIVATE_VIDEOS_FILE']):
        with open(app.config['PRIVATE_VIDEOS_FILE'], 'r') as f:
            for line in f:
                private_videos.add(line.strip())
    return private_videos


def save_private_videos(private_videos):
    """save set of private videos in text file"""
    with open(app.config['PRIVATE_VIDEOS_FILE'], 'w') as f:
        for video in private_videos:
            f.write(video + '\n')


def is_video_private(file_path):
    """Check if video is private"""
    private_videos = get_private_videos()
    return file_path in private_videos

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_video_folders():
    """Returns a list of all video folders created so far with counts"""
    folders = []
    for item in os.listdir(app.config['UPLOAD_FOLDER']):
        item_path = os.path.join(app.config['UPLOAD_FOLDER'], item)
        if os.path.isdir(item_path):
            video_count = len([f for f in os.listdir(item_path) if allowed_file(f)])
            folders.append({'name': item, 'count': video_count})
    return folders

@app.route('/uploadvideos', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser might
        # submit an empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        print("file name: ",file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gallery')) # Redirect to Gallery
    return render_template('/gallery/uploadvideos.html')

@app.route('/gallery')
def gallery():
    video_files = []
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(f):
            video_files.append({
                'name': f,
                'is_private': is_video_private(os.path.join(app.config['UPLOAD_FOLDER'], f))
            })

    return render_template('/gallery/gallery.html', video_files=video_files, video_folders=get_video_folders())

@app.route('/play/<filename>')
def play_video(filename):
    return render_template('/gallery/video_player.html', filename=filename)


@app.route('/move_video', methods=['POST'])
def move_video():
    """Moves a video to a folder"""
    if request.method == 'POST':
        filename = request.form.get('video_to_move')
        folder_name = request.form.get('folder_name')
        
        if not folder_name:
            return redirect(url_for('gallery'))  # Don't move, if no folder is given

        source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        dest_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        dest_path = os.path.join(dest_folder_path, filename)
        
        #create folder if not already there
        os.makedirs(dest_folder_path, exist_ok=True)
        
        os.rename(source_path, dest_path)
        
        return redirect(url_for('gallery')) 

@app.route('/folder/<folder_name>')
def folder_view(folder_name):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    if not os.path.isdir(folder_path):
        return "Folder not found", 404
    
    video_files = []
    for f in os.listdir(folder_path):
        if allowed_file(f):
           video_files.append({
                'name': f,
                'is_private': is_video_private(os.path.join(folder_path, f))
           })

    return render_template('/gallery/folder_view.html', folder_name=folder_name, video_files=video_files, video_folders=get_video_folders())

@app.route('/rename_video', methods=['POST'])
def rename_video():
    if request.method == 'POST':
        old_filename = request.form.get('old_filename')
        new_filename = request.form.get('new_filename')
        folder_name = request.form.get('folder_name')

        if not old_filename or not new_filename:
            return redirect(url_for('gallery'))
        
        _, file_extension = os.path.splitext(old_filename)
        new_filename_with_extension = new_filename + file_extension

        if folder_name:
          old_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, old_filename)
          new_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, new_filename_with_extension)
        else:
           old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
           new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename_with_extension)


        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            #update the private video if it exist there as well
            private_videos = get_private_videos()
            if old_path in private_videos:
                private_videos.remove(old_path)
                private_videos.add(new_path)
                save_private_videos(private_videos)

    return redirect(url_for('gallery'))



@app.route('/delete_video', methods=['POST'])
def delete_video():
    if request.method == 'POST':
        filename = request.form.get('filename')
        folder_name = request.form.get('folder_name')

        if folder_name:
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, filename)
        else:
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(file_path):
            os.remove(file_path)

            #remove the file from private videos as well
            private_videos = get_private_videos()
            if file_path in private_videos:
                private_videos.remove(file_path)
                save_private_videos(private_videos)
    return redirect(url_for('gallery'))

@app.route('/toggle_privacy2', methods=['POST'])
def toggle_privacy2():
    filename = request.form.get('filename')
    if filename:
        privacy_data = load_privacy_data()
        if filename in privacy_data:
            privacy_data[filename]['public'] = not privacy_data[filename].get('public', False)
            save_privacy_data(privacy_data)
    return redirect(url_for('gallery'))

@app.route('/toggle_privacy', methods=['POST'])
def toggle_privacy():
    if request.method == 'POST':
        filename = request.form.get('filename')
        folder_name = request.form.get('folder_name')

        if folder_name:
          file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, filename)
        else:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)


        private_videos = get_private_videos()

        if file_path in private_videos:
            private_videos.remove(file_path)
        else:
            private_videos.add(file_path)

        save_private_videos(private_videos)
    return redirect(url_for('gallery'))

@app.route('/set_privacy', methods=['POST'])
def set_privacy():
    """Sets privacy of a video to public or private"""
    if request.method == 'POST':
      filename = request.form.get('video_name')
      is_public = request.form.get('is_public') == 'true' # convert str to bool

      privacy_data = load_privacy_data()
      privacy_data[filename]['public'] = is_public
      save_privacy_data(privacy_data)
      
    return redirect(url_for('gallery'))

@app.route('/usergallery')
def user_gallery():
    """Displays only public videos"""
    video_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    privacy_data = load_privacy_data()
    
    public_videos = []
    for video in video_files:
      if video in privacy_data and privacy_data[video]['public']:
        public_videos.append(video)
    
    return render_template('/gallery/usergalleryadmin.html', public_videos=public_videos, video_folders = get_video_folders())

@app.route('/usergalleryview')
def user_gallery_view():
    """Displays only public videos"""
    video_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    privacy_data = load_privacy_data()
    
    public_videos = []
    for video in video_files:
      if video in privacy_data and privacy_data[video]['public']:
        public_videos.append(video)
    
    return render_template('/gallery/usergallery.html', public_videos=public_videos, video_folders = get_video_folders())

##########################################################################################################

@app.route('/logout')
@login_required
def logout():
  app.logger.info('logout: Successful Logout with user email : ' + str(current_user))
  try:
    #print("==>", type(session))  # Debugging line to check the session type
    logout_user()
    flask.session.clear()  # Clear all session data
    # Remove user session data
    session.pop('userloggedinemail', None)  # Clear user ID from session
    session.clear()
    flash('You have been logged out successfully!', 'info')
  except Exception as e:
    app.logger.error(f'An error occurred in logout: {e}', exc_info=True)
  
  app.logger.info("logout:current_user.is_authenticated : ",current_user.is_authenticated)
  #return render_template('login-page.html')
  response = make_response(redirect(url_for('loginpage')))
  return clear_cache(response)
  #return redirect(url_for('loginpage'))

# Menu Bar functions ENDs |||||||||||||||||||||||||| MENU BAR ||||||||||||||||||||||||||||||||||||||||||

def clear_cache(response):
    """Set headers to clear the cache and ensure fresh content is loaded."""
    app.logger.info('clear_cache: Set headers to clear the cache.'+ str(response))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.after_request
def add_header(response):
    # Disable caching to prevent going back to the previous pages after logout
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# Calling main application !!!!!!!!!!!!!!!!!!!!!!!!!!!

# A flag to ensure server info is printed only once
server_info_logged = False

@app.before_request
def log_server_info():
    global server_info_logged
    if not server_info_logged:
        # Get server name and port from the incoming request
        server_name = request.host.split(':')[0]  # The server name
        server_port = request.host.split(':')[1] if ':' in request.host else '80'  # The port
        
        # Log the server and port information
        if DB_ENV == 'NP':
          app.logger.info(f"Non-Production Server is running on: {server_name}:{server_port}")
        if DB_ENV == 'PROD':
          app.logger.info(f"Production Server is running on: {server_name}:{server_port}")
        if DB_ENV == 'UAT':
          app.logger.info(f"UAT Server is running on: {server_name}:{server_port}")
          
        #print(f"Server is running on: {server_name}:{server_port}")
        server_info_logged = True  # Ensure this runs only once


if __name__ == "__main__":
  # Use the DB_ENV variable in logic
  if DB_ENV == 'NP':
      app.logger.info('Running in Non-Production environment')
      app.run(host='0.0.0.0', port='3001', debug=True)
  elif DB_ENV == 'PROD':
      app.logger.info('Running in Production environment')
      app.run()
  elif DB_ENV == 'UAT':
      app.logger.info('Running in UAT environment')
      app.run()
  else:
      app.logger.info('Running in UNDEFINED environment')
      #app.run()
  #app.run()
  #app.run(host='0.0.0.0', port='3001', debug=True)
