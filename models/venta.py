from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venta(db.Model):
    __tablename__ = 'ventas'
    idventas = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuarios.idusuarios'), nullable=False)
    monto = db.Column(db.Float)
    fecha = db.Column(db.Date)
