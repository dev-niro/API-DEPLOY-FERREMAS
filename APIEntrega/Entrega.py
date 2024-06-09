from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

entregas = []

class EntregasPendientes(Resource):
    def get(self):
        entregas_pendientes = [entrega for entrega in entregas if entrega['estado'] != 'Entregado' and entrega['tipo_envio'] == 'Retiro']
        despachos_pendientes = [entrega for entrega in entregas if entrega['estado'] != 'Entregado' and entrega['tipo_envio'] == 'Despacho']
        return {'entregas_pendientes': entregas_pendientes,
                'despachos_pendientes': despachos_pendientes,}, 200

class Entrega(Resource):
    def put(self, id_entrega):
        for entrega in entregas:
            if entrega['id'] == id_entrega:
                entrega['estado'] = request.json['estado']
                return {'message': 'Estado de la entrega cambiado correctamente'}, 200
        return {'message': 'Entrega no encontrada'}, 404

class Entregas(Resource):
    def post (self):
        body = request.get_json()
        body['estado'] = 'Pendiente'
        body['id'] = 'C' + str(len(entregas)+1).zfill(3)
        entregas.append(body)

    def get(self):
        return {'entregas': entregas}, 200
    
api.add_resource(Entrega, '/api/entrega/<id_entrega>')
api.add_resource(Entregas, '/api/entregas')
api.add_resource(EntregasPendientes, '/api/pendientes')

if __name__ == '__main__':
    app.run(debug=True, port=5001)