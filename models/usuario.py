from . import db
from .venta import Venta

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    idusuarios = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    ventas = db.relationship('Venta', backref='usuario', lazy=True)