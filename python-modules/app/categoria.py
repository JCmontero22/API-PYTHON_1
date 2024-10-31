from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/Appi-Python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion tabla categoria
class CategoriaDos(db.Model):
    categoria_id = db.Column(db.Integer, primary_key=True)
    categoria_nombre = db.Column(db.String(100))
    categoria_descripcion = db.Column(db.String(100))

    def __init__(self, categoria_nombre, categoria_descripcion):
        self.categoria_nombre = categoria_nombre
        self.categoria_descripcion = categoria_descripcion



#Esquema 
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('categoria_id', 'categoria_nombre', 'categoria_descripcion')
        
        
#Una sola respuesta 
categoria_schema = CategoriaSchema()        


#varias respuestas
categorias_schema = CategoriaSchema(many=True)


#peticion GET 
@app.route('/categoria', methods=['GET'])
def get_cateogiras():
        all_categorias = CategoriaDos.query.all()
        result = categorias_schema.dump(all_categorias)
        return jsonify(result)


# peticion GET por id
@app.route('/categoriaId/<id>', methods=['GET'])
def get_categoriaID(id):
        una_categoria = CategoriaDos.query.get(id)
        return categoria_schema.jsonify(una_categoria)


# Peticion POST para registro
@app.route('/crearCategoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    categoria_nombre = data['categoria_nombre']
    categoria_descripcion = data['categoria_descripcion']
    
    nuevo_registro = CategoriaDos(categoria_nombre, categoria_descripcion)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)
    

#********* MENSAJE DE BIENVENIDA ******************************
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': 'Hola mundo'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

#Prueba desde el de mesa