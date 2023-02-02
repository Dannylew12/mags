from flask import Flask
app = Flask(__name__)

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument




app.secret_key = "34de5rf6tg7yh8uji9"
DATABASE = "users_and_magazines_schema"
