from flask import Flask, request
from flask.ext.restful import Api, Resource
from freesound_client import get_tags_for_sound, get_sound
from flickr_client import get_tags_for_image, get_image
from similarities import select_tags

app = Flask(__name__)
api = Api(app)

class GetMoreOf(Resource):
    def __init__(self, prev_data, chosen_id, chosen_type):
        self.prev_data = prev_data
        self.chosen_id = chosen_id
        self.chosen_type = chosen_type

    def get(self):
        # tags = []
        # if self.chosen_type == "sound":
        #     tags = get_tags_for_sound(self.chosen_id)
        # elif self.chosen_type == "photo":
        #     tags = get_tags_for_image(self.chosen_id)

        selected_tags = select_tags(self.prev_data, self.chosen_id)

        tags = ''.join(selected_tags)
        return get_sound(tags) + get_image(tags)

api.add_resource(GetMoreOf, '/<string:type>/<string:id>')

if __name__ == '__main__':
        app.run(debug=True)

