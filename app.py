from flask import Flask, render_template

app = Flask(__name__)


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
  return render_template('show-tickers.html')


@app.route("/showusers")
def show_users():
  return render_template('show-users.html')


print(__name__)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5000', debug=True)
