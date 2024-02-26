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
        print(current_user)
        flash("No tienes permisos ")
        return redirect(url_for('litos.index'))
    formulario = Login(meta={'csrf':False})
    if formulario.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario=formulario.usuario.data).first()
        if usuario and usuario.check_password(formulario.password.data) and usuario.activo == True:
            login_user(usuario)
            flash ("Bienvenido "+ current_user.usuario)
            next = request.form['next']
            return redirect(next or url_for('litos.index'))
        else:
            flash("Usuario o la contraseña no son correctos", 'danger')
    if formulario.errors:
        flash(formulario.errors, 'danger')
    return render_template('autenticacion/login.html', login=formulario)

@autenticacion.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('autenticacion.login'))


@autenticacion.route('/registro_usuario', methods = ('GET', 'POST'))
def registro():
    if session.get('usuario'):
        print(session['username'])
    formulario = RegistroUsuario(meta={'csrf':False})
    if formulario.validate_on_submit():
        usuario = Usuario(formulario.usuario.data, formulario.apellido1.data, formulario.apellido2.data, formulario.password.data, formulario.rol.data, formulario.correo.data)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario creado con éxito")
        return redirect(url_for('autenticacion.registro'))
    if formulario.errors:
        flash(formulario.errors, 'danger')

    return render_template('/autenticacion/registro.html', registro = formulario)


@autenticacion.route('/usuarios', methods=('GET', 'POST'))
def usuarios():
    usuario = Usuario.query.order_by(Usuario.usuario.asc())
    for usu in usuario:
        print(usu.usuario)#Este bucle es para recordar como leer los datos de la consulta sqlalchemy
    return render_template('/autenticacion/lista_usuarios.html', usuario=usuario)

@autenticacion.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    formulario = EditarForm(meta={'csrf':False})

    if request.method == 'GET':
        formulario.usuario.data = usuario.usuario
        formulario.apellido1.data = usuario.apellido1
        formulario.apellido2.data = usuario.apellido2
        formulario.rol.data = usuario.rol
        formulario.correo.data = usuario.rol
        formulario.activo.data = usuario.activo

    if formulario.validate_on_submit():
        usuario.usuario = formulario.usuario.data
        usuario.apellido1 = formulario.apellido1.data
        usuario.apellido2 = formulario.apellido2.data
        usuario.correo = formulario.correo.data
        usuario.rol = formulario.rol.data
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario actualizado")
        return redirect(url_for('autenticacion.usuarios'))

    if formulario.errors:
        flash(formulario.errors, 'danger')
    return render_template('/autenticacion/usuario-editar.html', usuario=usuario, formulario=formulario)

@autenticacion.route('/pass-editar/<int:id>', methods=['GET', 'POST'])
def passeditar(id):
    usuario = Usuario.query.get_or_404(id)
    formularioPasswd = EditarPass(meta={'csrf':False})
    if request.method == 'GET':
        formularioPasswd.password.data = usuario.password

    if formularioPasswd.validate_on_submit():
        password = formularioPasswd.password.data
        usuario.password = generate_password_hash(password)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario actualizado")
        return redirect(url_for('autenticacion.usuarios'))

    if formularioPasswd.errors:
        flash(formularioPasswd.errors, 'danger')
    return render_template('/autenticacion/pass-editar.html', usuario=usuario, formulario=formularioPasswd)