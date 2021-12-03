#EQUIPO 2
# LUIS FERNANDO ROJAS
# LEONARDO RUIZ RODRIGUEZ
# GERARDO CASTAÑEDA vega

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
ema = Marshmallow(app)


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
    id_nomina = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    domicilio = db.Column(db.String(50))
    telefono = db.Column(db.String(15))
    rfc = db.Column(db.String(13))
    curp = db.Column(db.String(18))
    imss = db.Column(db.String(11))
    id_puesto = db.Column(db.Integer)
    id_jornada = db.Column(db.Integer)
    edoEmpleado = db.Column(db.String(1))
    fechaingreso = db.Column(db.String(10))
    ctaBancaria = db.Column(db.String(18))
    def __init__(self, nombre, domicilio, telefono, rfc, curp, imss, id_puesto, id_jornada, edoEmpleado, fechaingreso, ctaBancaria):
        self.nombre = nombre
        self.domicilio = domicilio
        self.telefono = telefono
        self.rfc= rfc
        self.curp = curp
        self.imss = imss
        self.id_puesto = id_puesto
        self.id_jornada = id_jornada
        self.edoEmpleado = edoEmpleado
        self.fechaingreso = fechaingreso
        self.ctaBancaria = ctaBancaria

db.create_all()

#creando el escquema
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')
#cuando es una sola respuesta
categoria_schema = CategoriaSchema()
#cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

class EmpleadoSchema(ema.Schema):
    class Meta:
        fields = ('nombre', 'domicilio', 'telefono','rfc', 'curp','imss', 'id_puesto','id_jornada','edoEmpleado','fechaingreso','ctaBancaria')

empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)

#GET ##########################################
@app.route('/categorias', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

@app.route('/empleado', methods=['GET'])
def get_empleados():
    all_empleados = Empleados.query.all()
    result = empleados_schema.dump(all_empleados)
    return jsonify(result)


#get x id #######################

@app.route('/categorias/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

@app.route('/empleado/<id>', methods=['GET'])
def get_empleado_x_id(id):
    un_empleado = Empleados.query.get(id)
    return empleado_schema.jsonify(un_empleado)

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

@app.route('/empleado', methods=['POST'])
def insert_empleado():
    data = request.get_json(force=True)
    nombre = data['nombre']
    domicilio = data['domicilio']
    telefono = data['telefono']
    rfc = data['rfc']
    curp = data['curp']
    imss = data['imss']
    id_puesto = data['id_puesto']
    id_jornada = data['id_jornada']
    edoEmpleado = data['edoEmpleado']
    fechaingreso = data['fechaingreso']
    ctaBancaria = data['ctaBancaria']
    nuevoempleado = Empleados(nombre, domicilio, telefono, rfc, curp, imss, id_puesto, id_jornada,
                              edoEmpleado, fechaingreso, ctaBancaria)
    db.session.add(nuevoempleado)
    db.session.commit()
    return empleado_schema.jsonify(nuevoempleado)



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

@app.route('/empleado/<id>', methods=['PUT'])
def update_empleado(id):
    actualizarempleado= Empleados.query.get(id)
    data = request.get_json(force=True)
    nombre = data['nombre']
    domicilio = data['domicilio']
    telefono = data['telefono']
    rfc = data['rfc']
    curp = data['curp']
    imss = data['imss']
    id_puesto = data['id_puesto']
    id_jornada = data['id_jornada']
    edoEmpleado = data['edoEmpleado']
    fechaingreso = data['fechaingreso']
    ctaBancaria = data['ctaBancaria']
    actualizarempleado.nombre =nombre
    actualizarempleado.domicilio = domicilio
    actualizarempleado.telefono = telefono
    actualizarempleado.rfc = rfc
    actualizarempleado.curp = curp
    actualizarempleado.imss = imss
    actualizarempleado.id_puesto = id_puesto
    actualizarempleado.id_jornada = id_jornada
    actualizarempleado.edoEmpleado = edoEmpleado
    actualizarempleado.fechaingreso = fechaingreso
    actualizarempleado.ctaBancaria = ctaBancaria

    db.session.commit()
    return empleado_schema.jsonify(actualizarempleado)





#delete ####
@app.route('/categorias/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminarcategoria = Categoria.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarcategoria)

@app.route('/empleado/<id>', methods=['DELETE'])
def delete_empleado(id):
    eliminarempleado = Empleados.query.get(id)
    db.session.delete(eliminarempleado)
    db.session.commit()
    return empleado_schema.jsonify(eliminarempleado)



@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'BIENVENIDO AL SISTEMA DE EMPLEADOS REST'})


if __name__=="__main__":
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5000)