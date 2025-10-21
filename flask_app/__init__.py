from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "super_secret_key_change_me"



bcrypt = Bcrypt(app)

from .controllers import usuarios, peliculas 


 