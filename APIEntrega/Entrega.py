from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json


app = Flask(__name__)
api = Api(app)

entregas = []


class EntregasPendientes(Resource):
    def get(self):
        entregas_pendientes = [entrega for entrega in entregas if entrega['estado'] != 'entregada']
        return {'entregas_pendientes': entregas_pendientes}, 200


class EntregasDespacho(Resource):
    
    def get(self):
        entregas_despacho = [entrega for entrega in entregas if entrega['estado'] == 'despacho']
        return {'entregas_despacho': entregas_despacho}, 200
class Entrega(Resource):
    def put(self, id_entrega):
        for entrega in entregas:
            if entrega['id'] == id_entrega:
                entrega['estado'] = request.json['estado']
                return {'message': 'Estado de la entrega cambiado correctamente'}, 200
        return {'message': 'Entrega no encontrada'}, 404


    def post (self):
        body = request.get_json()
        entregas.append(body)

api.add_resource(EntregasPendientes, '/entregas')
api.add_resource(EntregasDespacho, '/entregas/despacho')
api.add_resource(Entrega, '/entrega')

if __name__ == '__main__':
    app.run(debug=True, port=5001)