import os
from flask import Flask, render_template, send_from_directory, request
from flask_restful import Resource, Api, reqparse
import werkzeug
import binascii
import CBIR_search as search_image


app = Flask(__name__)
api = Api(app)
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
app.config['DATA_DIR'] = "static/data"

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if 'file' in request.files and request.files['file'].filename != '':
        image = request.files['file']
        print(image)
        image.save('tmp.jpg')

    maxResults = 50
    if 'maxRes' in request.form and request.form['maxRes'] != '':
        maxResults = int(request.form['maxRes'])

    text = None
    if 'text' in request.form and request.form['text'] != '':
        text = request.form['text']

    cbir_images = None
    if 'file' in request.files and request.files['file'].filename != '':
        cbir_images = search_image.run('tmp.jpg', maxResults)

    root_dir = 'static/data/jpg'
    images = []
    if cbir_images is None:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                    if (len(images) >= maxResults):
                        return render_template('search.html', paths=images)
                    images.append(os.path.join(root, file))
    else:
        for file in cbir_images:
            images.append(os.path.join(root_dir, file))
    return render_template('search.html', paths=images)

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
        
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('maxRes', type=int, location='form')
        parser.add_argument('text', type=str, location='form')
        args = parser.parse_args()

        if args['file'] is not None:
            image = args['file']
            print(image)
            image.save('tmp.jpg')

        maxResults = 50
        if args['maxRes'] is not None:
            maxResults = int(args['maxRes'])

        text = None
        if args['text'] is not None:
            text = args['text']

        root_dir = 'static/data/jpg'
        images = []
        if args['file'] is not None:
            cbir_images = search_image.run('tmp.jpg', maxResults)
            
            # if (args['file'] is not None):
            #     return {'message': 'will search with saved image and query: ' + args['file']}, 200

            for file in cbir_images:
                images.append(request.url_root + os.path.join(root_dir, file))
            return {'images': images}, 200
        
        # if (args['text'] is not None):
        #     return {'message': 'will search with query: ' + args['text']}, 200

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                    if (len(images) >= maxResults):
                        return {'images': images}, 200
                    images.append(request.url_root + os.path.join(root, file))
        return {'images': images}, 200
    
api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run()
