import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import boto3
from botocore.exceptions import NoCredentialsError
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# Flask
app = Flask(__name__)
api = Api(app)

# DynamoDB

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1',
                          aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key=os.getenv("aws_secret_access_key"))
table = dynamodb.Table('mytable')

# Définir un analyseur de demande pour traiter les données JSON
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')

# ressource pour gérer les éléments


class ItemResource(Resource):
    def get(self, item_id):
        response = table.get_item(Key={'id': item_id})
        item = response.get('Item', {})
        return item, 200

    def put(self, item_id):
        args = parser.parse_args()
        item = {
            'id': item_id,
            'name': args['name'],
            'description': args['description']
        }
        table.put_item(Item=item)
        return item, 201

    def delete(self, item_id):
        table.delete_item(Key={'id': item_id})
        return '', 204


api.add_resource(ItemResource, '/items/<string:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
