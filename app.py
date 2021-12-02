#AQUI VAMOS APEGAR EL CODIGO

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import json
#from Dao import empleados, db

app = Flask(__name__)
#CADENA DE CONEXION
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/ukuarestdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#INSTANCIAR CONEXION
db=SQLAlchemy(app)
ma= Marshmallow(app)

#CREACION DE LA TABLA Y LA CLASE
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))
#creando el constructor
    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp


class Empleados(db.Model):
    emp_id_nomina = db.Column(db.Integer, primary_key=True)
    emp_nombre = db.Column(db.String(50))
    emp_domicilio = db.Column(db.String(50))
    emp_telefono = db.Column(db.String(15))
    emp_rfc = db.Column(db.String(13))
    emp_curp = db.Column(db.String(18))
    emp_imss = db.Column(db.String(11))
    emp_id_puesto = db.Column(db.Integer)
    emp_id_jornada = db.Column(db.Integer)
    emp_edoEmpleado = db.Column(db.String(1))
    emp_fechaingreso = db.Column(db.String(10))
    emp_ctaBancaria = db.Column(db.String(18))
    def __init__(self, nombre, domicilio, telefono, rfc, curp, imss, id_puesto, id_jornada, edoEmpleado, fechaingreso, ctaBancaria):
        self.emp_nombre = nombre
        self.emp_domicilio = domicilio
        self.emp_telefono = telefono
        self.emp_rfc= rfc
        self.emp_curp = curp
        self.emp_imss = imss
        self.emp_id_puesto = id_puesto
        self.emp_id_jornada = id_jornada
        self.emp_edoEmpleado = edoEmpleado
        self.emp_fechaingreso = fechaingreso
        self.emp_ctaBancaria = ctaBancaria

db.create_all()

#creando el escquema
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')
#cuando es una sola respuesta
categoria_schema = CategoriaSchema()
#cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('nopmbre', 'direccion', 'telefono','rfc', 'curp','imss', 'id_puesto','id_jornada','edoEmpleado',
                  'fechaingreso','ctaBancaria')

empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)

#GET ##########################################
@app.route('/categorias', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

@app.route('/empleados', methods=['GET'])
def get_empleados():
    all_empleados = Empleados.query.all()
    resultado = empleados_schema.dump(all_empleados)
    return jsonify(resultado)


#get x id #######################

@app.route('/categorias/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#POST ##################
@app.route('/categorias', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    nuevocategoria = Categoria(cat_nom, cat_desp)
    #insertando el registro
    db.session.add(nuevocategoria)
    db.session.commit()
    return categoria_schema.jsonify(nuevocategoria)


#PUT ########################
@app.route('/categorias/<id>', methods=['PUT'])
def update_categoria(id):
    actualizarcategoria= Categoria.query.get(id)
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    actualizarcategoria.cat_nom = cat_nom
    actualizarcategoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actualizarcategoria)

#delete ####
@app.route('/categorias/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminarcategoria = Categoria.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarcategoria)




@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'BIENVENIDO AL SISTEMA DE EMPLEADOS REST'})


if __name__=="__main__":
    app.run(debug=True)