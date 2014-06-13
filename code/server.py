from flask import Flask, request
from flask.ext.restful import Api, Resource
from freesound_client import get_tags_for_sound, get_sound
from flickr_client import get_tags_for_image, get_image
from similarities import select_tags
import json

app = Flask(__name__)
api = Api(app)

class RawSearch(Resource):
    def get(self):
        tags = request.form.keys()[0]
        print tags
        print [image["id"] for image in get_image(tags)]
        return {'sounds': get_sound(tags), 'images': get_image(tags)}, 200, {'Access-Control-Allow-Origin': '*'}
    post = get

    def options (self):
       return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET' }

class CoNavigate(Resource):
    def get(self, type, id):
        items= json.loads(request.form.keys()[0])
        image_ids = items["images"]
        sound_ids = items["sounds"]
        chosen_type = type
        chosen_id = int(id)
        if chosen_type == 'p':
            data = {int(id): get_tags_for_image(id) for id in image_ids}
            selected_tags = select_tags(data, chosen_id)
        else:
            data = {int(id): get_tags_for_sound(id) for id in sound_ids}
            selected_tags = select_tags(data, chosen_id)
        tags = ' '.join(selected_tags)
        return {'sounds': get_sound(tags), 'images': get_image(tags)}, 200, {'Access-Control-Allow-Origin': '*'}
    post = get

    def options (self):
       return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET' }

api.add_resource(RawSearch,'/search')
api.add_resource(CoNavigate, '/<string:type>/<string:id>')

if __name__ == '__main__':
        app.run(debug=True)

