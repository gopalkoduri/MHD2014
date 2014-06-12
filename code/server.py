from flask import Flask, request
from flask.ext.restful import Api, Resource
from freesound_client import get_tags_for_sound, get_sound
from flickr_client import get_tags_for_image, get_image
from similarities import select_tags

app = Flask(__name__)
api = Api(app)

class GetMoreOf(Resource):
    def get(self, data):
        # tags = []
        # if self.chosen_type == "sound":
        #     tags = get_tags_for_sound(self.chosen_id)
        # elif self.chosen_type == "photo":
        #     tags = get_tags_for_image(self.chosen_id)

        image_ids = []
        sound_ids = []
        data = data.split(',')

        temp = data[-1].split(':')
        chosen_type = temp[0]
        chosen_id = temp[1]

        for i in data:
            parts = i.split(':')
            if parts[0] == 'p':
                image_ids.append(parts[1])
            else:
                sound_ids.append(parts[1])

        if chosen_type == 'p':
            data = {id: get_tags_for_image(id) for id in image_ids}
            selected_tags = select_tags(data, chosen_id)
        else:
            data = {id: get_tags_for_sound(id) for id in sound_ids}
            selected_tags = select_tags(data, chosen_id)

        tags = ' '.join(selected_tags)
        return {'sounds': get_sound(tags), 'images': get_image(tags)}

api.add_resource(GetMoreOf, '/<string:data')

if __name__ == '__main__':
        app.run(debug=True)

