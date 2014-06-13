from settings import flickr_url
from settings import flickr_token
from memoize import memoized
import similarities as sim
from unidecode import unidecode

import requests
import re
import json


_jsonp_remover = re.compile(r"\(|\)")
def _to_json(text):
    return json.loads(' '.join(_jsonp_remover.split(text)[1:-1]))

def flickr_api_get_image_list(tags):
    payload = dict(
            method = "flickr.photos.search",
            api_key = flickr_token,
            tag_mode = "all",
            text = tags,
            format = "json",
            per_page = 25,
            sort = 'relevance',
            extras = 'tags, farm, server, owner_name'
            )
    return _to_json(requests.get(flickr_url, params = payload).text)["photos"]["photo"]

def flickr_api_get_image_info(photo_id):
    payload = dict(
            method = "flickr.photos.getInfo",
            api_key = flickr_token,
            photo_id = photo_id,
            format = "json"
            )
    text = requests.get(flickr_url, params = payload).text
    return _to_json(text)["photo"]

def get_image(tags, coord = None, radius = None):
    if coord and radius:
        #TODO implement filter by geolocation
        pass
    photos = flickr_api_get_image_list(tags)
    result = []

    for photo in photos:
        #TODO: Does this function search in tags, description and everything?
        #info = flickr_api_get_image_info(photo["id"])
        #photo["username"] = info["owner"]["username"]
        #photo["name"] = info["title"]["_content"]
        #photo["tags"] = [t["_content"] for t in info["tags"]["tag"]]
        photo["tags"] = photo["tags"].split()
        #photo["description"] = info["description"]["_content"]
        username = unidecode(photo["ownername"]).replace(' ','-')
        photo["embed_url"] = ("https://farm" + str(photo["farm"]) + ".staticflickr.com/" +
                str(photo["server"]) + "/" + str(photo["id"]) + "_" + str(photo["secret"]) + ".jpg")
        result.append(photo)

    #Sort the sounds by their relevance within the result set
    g = sim.build_graph(result, similarity_threshold=0.3)
    id_ranks = {y: x+1 for x, y in list(enumerate(sim.rank_relevance(g)))}
    print id_ranks
    print result
    for i in result:
        print i["id"]
        print id_ranks[i["id"]]
        i['rank'] = id_ranks[i['id']]

    return result

@memoized
def get_tags_for_image(image_id):
    info = flickr_api_get_image_info(image_id)
    return [t["_content"] for t in info["tags"]["tag"]]
