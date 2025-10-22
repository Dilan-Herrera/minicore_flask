from flask import Flask
from models import db
from controllers import ventas_controller

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'clave123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minicore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db.init_app(app)

# Rutas
app.add_url_rule('/', 'home', ventas_controller.mostrar_formulario_busqueda)
app.add_url_rule('/comisiones', 'comisiones', ventas_controller.mostrar_comisiones, methods=['POST'])
app.add_url_rule('/agregar_venta', 'form_agregar', ventas_controller.mostrar_formulario_agregar)
app.add_url_rule('/agregar_venta_post', 'agregar_venta', ventas_controller.agregar_venta, methods=['POST'])

# MAIN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ventas_controller.insertar_datos_de_prueba()
    app.run(debug=True, host='0.0.0.0', port=5000)