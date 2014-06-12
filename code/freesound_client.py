from freesound import freesound
from settings import freesound_token
from memoize import memoized

client = freesound.FreesoundClient()
client.set_token(freesound_token, "token")

def get_sound(tags, coord = None, radius = None):
    if coord and radius:
        # TODO: filter by geolocation
        query_result = client.text_search(query = tags, page_size = 25)
    else:
        query_result = client.text_search(query = tags, page_size = 25)

    for sound in query_result.results:
        sound["embed_url"] = "http://www.freesound.org/embed/sound/iframe/" + str(sound["id"]) + "/simple/medium/"
        sound["description"] = client.get_sound(sound["id"]).description

    return query_result.results

@memoized
def get_tags_for_sound(sound_id):
    return client.get_sound(sound_id).tags
