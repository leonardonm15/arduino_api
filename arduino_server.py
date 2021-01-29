from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaase.db'
db = SQLAlchemy(app)

infos = reqparse.RequestParser()
infos.add_argument('temp', type=float, help='Temperatura do ambiente', required=True)
infos.add_argument('horario', type=datetime.datetime, help='Horário do momento do request', required=False)
infos.add_argument('humidade', type=float, help='Humidade do ambiente', required=True)


resorce_fields = {
    'id': fields.Integer,
    'temp': fields.Float,
    'horario': fields.DateTime,
    'humidade': fields.Float
}


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    humidade = db.Column(db.Integer, nullable=False)


@app.route('/')
def home():
    return 'ARDUINO API :)'


class Info(Resource):
    @marshal_with(resorce_fields)
    def put(self):
        args = infos.parse_args()
        registro = Database(temp=args['temp'], horario=args['horario'], humidade=args['humidade'])
        db.session.add(registro)
        db.session.commit()
        return registro, 200


class GetInfos(Resource):
    @marshal_with(resorce_fields)
    def get(self, id):
        registro = Database.query.filter_by(id=id).first()
        if registro:
            return registro
        else:
            abort(404, message='Data nao encontrada')


class AllRegisters(Resource):
    @marshal_with(resorce_fields)
    def get(self):
        linhas = Database.query.all()
        return linhas

    @marshal_with(resorce_fields)
    def delete(self):
        sql = 'DELETE FROM Database'
        db.engine.execute(sql)
        return '', 200


api.add_resource(GetInfos, '/infos/<int:id>')
api.add_resource(Info, '/infos')
api.add_resource(AllRegisters, '/infos/registers')


while True:
    app.run(debug=True)
