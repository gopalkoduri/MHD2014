from freesound import freesound
from settings import freesound_token

client = freesound.FreesoundClient()
client.set_token(freesound_token, "token")

def get_sound(tags, coord = None, radius = None):
    if coord and radius:
        # TODO: filter by geolocation
        query_result = client.text_search(query = tags, page_size = 25)
    else:
        query_result = client.text_search(query = tags, page_size = 25)

    result = []
    for s in query.results:
        sound = freesound.Sound(s, client)
        sound.embed_url = "http://www.freesound.org/embed/sound/iframe/" + sound.id + "/simple/medium/"
        result.append(sound)
    return result
