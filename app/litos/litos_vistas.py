from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, session

from app import db, mysql
from app.autenticacion.autenticacion_vista import admin_required
#from app import db, mysql #msyql para implementar el buscador
from flask_login import login_required
from werkzeug.utils import secure_filename
import paramiko, re
from werkzeug.security import check_password_hash

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import date


litos = Blueprint('litos', __name__)

@litos.route('/litos')
def index():
    return render_template('/litos/index.html')