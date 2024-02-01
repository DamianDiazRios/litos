from app import db
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SelectField, SubmitField, BooleanField, DateField
from wtforms.validators import InputRequired, EqualTo, Email
from werkzeug.security import check_password_hash, generate_password_hash

class Arbol(db.Model):
    __tablename__ = 'arbol'
    __table_args__ = {'extend_existing': True}
    id_arbol = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(255))
    tipo = db.Column(db.String(50))
    fechaCompra = db.Column(db.Date, default=None)
    precioCompra = db.Column(db.Float(10), default=None)
    origen = db.Column(db.String(255))
    fechaVenta = db.Column(db.Date, default=None)
    precioVenta = db.Column(db.Float(10), default=None)
    destino = db.Column(db.String(255), default=None)