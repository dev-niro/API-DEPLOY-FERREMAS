from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json


app = Flask(__name__)
api = Api(app)

# Lista para almacenar las entregas
entregas = []

# Clase para manejar las entregas pendientes
class EntregasPendientes(Resource):
    # Método para obtener todas las entregas pendientes
    def get(self):
        entregas_pendientes = [entrega for entrega in entregas if entrega['estado'] != 'entregada']
        return {'entregas_pendientes': entregas_pendientes}, 200

# Clase para manejar las entregas en proceso de despacho
class EntregasDespacho(Resource):
    # Método para obtener todas las entregas en proceso de despacho
    def get(self):
        entregas_despacho = [entrega for entrega in entregas if entrega['estado'] == 'despacho']
        return {'entregas_despacho': entregas_despacho}, 200

# Clase para manejar una entrega específica
class Entrega(Resource):
    # Método para cambiar el estado de una entrega
    def put(self, id_entrega):
        for entrega in entregas:
            if entrega['id'] == id_entrega:
                entrega['estado'] = request.json['estado']
                return {'message': 'Estado de la entrega cambiado correctamente'}, 200
        return {'message': 'Entrega no encontrada'}, 404

    # Método para marcar una entrega como realizada
    def post(self, id_entrega):
        for entrega in entregas:
            if entrega['id'] == id_entrega:
                entrega['estado'] = 'entregada'
                return {'message': 'Entrega marcada como realizada correctamente'}, 200
        return {'message': 'Entrega no encontrada'}, 404

# Rutas de la API
api.add_resource(EntregasPendientes, '/entregas')
api.add_resource(EntregasDespacho, '/entregas/despacho')
api.add_resource(Entrega, '/entrega/<int:id_entrega>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
