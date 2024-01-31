from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user
from functools import wraps
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)
app.app_context().push()  # RuntimeError: Working outside of application context.

# Esta parte para implementar panel
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'damian'
app.config['MYSQL_PASSWORD'] = 'Damian1982-'
app.config['MYSQL_DB'] = 'litos'
mysql = MySQL(app)
#########################################


app.config.from_object('configuracion.ConfiguracionDesarrollo')
db = SQLAlchemy(app)

# LOGIN_FLASK
login_manager = LoginManager()  # Instancia de la clase LoginManager para flask_login
login_manager.init_app(app)  # Instacia de app
login_manager.login_view = "autenticacion.login"
login_manager.login_message = "No tienes permisos"

from app.autenticacion.autenticacion_vista import autenticacion


#VISTAS
app.register_blueprint(autenticacion)