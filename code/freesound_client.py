from freesound import freesound
from settings import freesound_token
from memoize import memoized
import similarities as sim

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

    #Sort the sounds by their relevance within the result set
    data = query_result.results
    g = sim.build_graph(data, similarity_threshold=0.3)
    id_ranks = {y: x+1 for x, y in list(enumerate(sim.rank_relevance(g)))}
    for i in data:
        i['rank'] = id_ranks[i['id']]

    return data

@memoized
def get_tags_for_sound(sound_id):
    return client.get_sound(sound_id).tags
