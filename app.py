from flask import Flask, render_template
from database import engine
from sqlalchemy import text

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


print(__name__)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5000', debug=True)
