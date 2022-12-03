import os
from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse
import werkzeug

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

class HelloWorld(Resource):
    def get(self):
        return {'message': 'hello world'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('name', required=True, help='Name cannot be blank', location='args')
        args = parser.parse_args()
        
        return {'message': 'hello ' + args['name']}, 200
    
class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('image', required=False, type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('query', required=False, location='form')
        args = parser.parse_args()
        
        if (args['image'] is not None):
            image = args['image']
            image.save('tmp.jpg')
            
            if (args['query'] is not None):
                return {'message': 'will search with saved image and query: ' + args['query']}, 200

            return {'message': 'will search with image'}, 200
        
        if (args['query'] is not None):
            return {'message': 'will search with query: ' + args['query']}, 200
        
        return {'message': 'will search anything'}, 200
    
api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run()
