from settings import flickr_url
from settings import flickr_token
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
            tags = tags.replace(' ',','),
            format = "json",
            per_page = 25
            )
    return _to_json(requests.get(flickr_url, params = payload).text)["photos"]["photo"]

def flickr_api_get_image_info(photo_id):
    payload = dict(
            method = "flickr.photos.getInfo",
            api_key = flickr_token,
            photo_id = photo_id,
            format = "json",
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
        info = flickr_api_get_image_info(photo["id"])
        photo["username"] = info["owner"]["username"]
        photo["name"] = info["title"]["_content"]
        photo["tags"] = [t["_content"] for t in info["tags"]["tag"]]
        photo["description"] = info["description"]["_content"]
        photo["embed_url"] = "https://www.flickr.com/photos/" + photo["username"] + "/" + photo["id"] + "/player"

        result.append(photo)
    return result
