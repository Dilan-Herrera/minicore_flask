from flask import render_template, request, redirect, url_for
from models.usuario import Usuario
from models.venta import Venta
from models import db
from sqlalchemy.sql import func
from datetime import datetime, date
from flask import flash

# Función para calcular comisión según total de ventas
def calcular_comision(total):
    if total >= 1000:
        return total * 0.15
    elif total >= 800:
        return total * 0.10
    elif total >= 600:
        return total * 0.08
    elif total >= 500:
        return total * 0.06
    else:
        return 0

# Insertar datos de prueba 
def insertar_datos_de_prueba():
    if Usuario.query.count() == 0:
        usuarios = [
            Usuario(nombre="Juan", apellido="Pérez"),
            Usuario(nombre="Ana", apellido="Martínez"),
            Usuario(nombre="Carlos", apellido="Gómez"),
            Usuario(nombre="Lucía", apellido="Sánchez"),
            Usuario(nombre="Pedro", apellido="Ramírez")
        ]
        db.session.add_all(usuarios)
        db.session.commit()

    if Venta.query.count() == 0:
        ventas = [
            Venta(idusuario=1, monto=120.50, fecha=date(2025, 6, 1)),
            Venta(idusuario=1, monto=380.00, fecha=date(2025, 6, 2)),
            Venta(idusuario=2, monto=150.00, fecha=date(2025, 6, 3)),
            Venta(idusuario=2, monto=500.00, fecha=date(2025, 6, 5)),
            Venta(idusuario=3, monto=75.00, fecha=date(2025, 6, 7)),
            Venta(idusuario=3, monto=95.00, fecha=date(2025, 6, 9)),
            Venta(idusuario=4, monto=300.00, fecha=date(2025, 6, 10)),
            Venta(idusuario=4, monto=600.00, fecha=date(2025, 6, 12)),
            Venta(idusuario=5, monto=210.00, fecha=date(2025, 6, 15)),
            Venta(idusuario=5, monto=800.00, fecha=date(2025, 6, 17))
        ]
        db.session.add_all(ventas)
        db.session.commit()

# Mostrar formulario de búsqueda
def mostrar_formulario_busqueda():
    return render_template('formulario_busqueda.html')

# Mostrar resultados de comisiones según rango de fechas
def mostrar_comisiones():
    fecha_inicio_str = request.form.get('fecha_inicio')
    fecha_fin_str = request.form.get('fecha_fin')

    # Convertir strings a objetos date
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

    resultados = (
        db.session.query(
            Usuario.nombre,
            Usuario.apellido,
            func.sum(Venta.monto).label('total_ventas')
        )
        .join(Venta)
        .filter(Venta.fecha.between(fecha_inicio, fecha_fin))
        .group_by(Usuario.idusuarios)
        .all()
    )

    resumen = []
    for r in resultados:
        comision = calcular_comision(r.total_ventas)
        resumen.append({
            "nombre": r.nombre,
            "apellido": r.apellido,
            "total_ventas": r.total_ventas,
            "comision": comision
        })

    return render_template('comision.html', comision=resumen)

# Mostrar formulario para agregar nueva venta
def mostrar_formulario_agregar():
    usuarios = Usuario.query.all()
    return render_template('agregar_venta.html', usuarios=usuarios)

# Guardar nueva venta en la base de datos
def agregar_venta():
    idusuario = int(request.form.get('idusuario'))
    monto = float(request.form.get('monto'))
    fecha_str = request.form.get('fecha')
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()  

    nueva_venta = Venta(idusuario=idusuario, monto=monto, fecha=fecha)
    db.session.add(nueva_venta)
    db.session.commit()
    db.session.commit()
    flash("Venta agregada correctamente", "success")
    return redirect(url_for('mostrar_formulario_busqueda'))