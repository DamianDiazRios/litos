from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, get_flashed_messages
from app.autenticacion.autenticacion_bbdd import Usuario,RegistroUsuario, Login, EditarForm, EditarPass
from flask_login import login_user, logout_user, current_user, login_required
from app import login_manager, wraps
from app import db, mysql
from werkzeug.security import check_password_hash, generate_password_hash

autenticacion = Blueprint('autenticacion', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        usu = str(current_user.rol)

        if usu == 'normal':
            return redirect(url_for('autenticacion.login'))
        return f(*args, **kws)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

@autenticacion.route ('/', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash("No tienes permisos " +current_user.usuario)
        return redirect(url_for('litos.index'))

