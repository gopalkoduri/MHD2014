from flask import Flask, request
from flask.ext.restful import Api, Resource
from freesound_client import get_tags_for_sound, get_sound
from flickr_client import get_tags_for_image, get_image

app = Flask(__name__)
api = Api(app)

class GetMoreOf(Resource):
    def get(self, type, id):
        tags = []
        if type == "sound":
            tags = get_tags_for_sound(id)
        elif type == "photo":
            tags = get_tags_for_image(id)
        # Gopala magic here

        tags = ''.join(tags)
        return get_sound(tags) + get_image(tags)

api.add_resource(GetMoreOf, '/<string:type>/<string:id>')

if __name__ == '__main__':
        app.run(debug=True)

