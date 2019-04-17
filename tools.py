# this file is for your TOOLS
# if you don't have data collecting during running your project, you should run this file first to collect data once
# if you want to collect data after some user input, you can import some functinos in your main app.py
import requests
import json
from db import db
from models import Media, Artist


CACHE = 'cache.json'
try:
    with open(CACHE, 'r') as cache_file:
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


# the following two funcs can be used for caching API calls and also scraping
def params_unique_combination(baseurl, params_d, private_keys=["apikey"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}={}".format(k, params_d[k]))
    return baseurl + "?" + "&".join(res)


def get_data_w_cache(url, params = {}, headers = {}):
    unique_ident = params_unique_combination(url, params)
    if unique_ident in CACHE_DICTION:
        print("* Getting cached data for url", unique_ident, "...")
        return CACHE_DICTION[unique_ident]
    print("* Making a request to get new data from url", unique_ident, "...")
    data = requests.get(url, params = params, headers = headers).text
    if '<!DOCTYPE html>' not in data:
        data = json.loads(data)  # extract json data
    CACHE_DICTION[unique_ident] = data
    dumped_json_cache = json.dumps(CACHE_DICTION, indent = 2)
    with open(CACHE, 'w') as cache_file:
        cache_file.write(dumped_json_cache)
    return data


def get_itunes_media(keyword, limit):
    params = {}
    params["term"] = keyword
    params["limit"] = limit
    return get_data_w_cache('https://itunes.apple.com/search', params = params)


def look_up_artist_info(artist_id):
    params = {}
    params["id"] = artist_id
    return get_data_w_cache('https://itunes.apple.com/lookup', params = params)


def populate_data_into_db(media_list):
    for media in media_list:
        new_media = Media(media_dict = media)
        if Media.query.filter_by(name = new_media.name, artist_id = new_media.artist_id).first():
            continue  # just in case you have same two media in db
        if Artist.query.filter_by(id=new_media.artist_id).first() == None:
            artist_dict = look_up_artist_info(new_media.artist_id)
            new_artist = Artist(artist_dict = artist_dict)
            new_artist.save_to_db()  # you have to save artist first, before you save a new media
        new_media.save_to_db()
    print("* Finish populating the data.")




    
