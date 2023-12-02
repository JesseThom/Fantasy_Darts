from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'its a secret to everybody'

DATABASE = "fantasy_darts"#TODO change schema name
# pythonanywhere database

# DATABASE = "jessethommes$fantasy_darts"