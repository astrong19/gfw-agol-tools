import requests
import json
import urllib

import util

def request_token(agol_creds):
    '''
    :param agol_creds: the name of the local file with the user/pass
    :return: a dictionary with folder_name, folder_id, item_name, item_id
    '''

    user = util.get_token(agol_creds)[0][1]
    password = util.get_token(agol_creds)[1][1]

    d = {"username": user,
         "password": password,
         "referer":"http://www.arcgis.com",
         "f": "json"}

    url = "https://www.arcgis.com/sharing/rest/generateToken"

    r = requests.post(url, data = d)

    response = json.loads(r.content)
    token = response['token']

    if 'error' in response.keys():
        raise Exception(response['message'], response['details'])

    return token

def get_agol_user_content(username):

    parameters = urllib.urlencode({'token':request_token('arcgis_online.config'),'f':'pjson'})
    stem = 'https://www.arcgis.com/sharing/rest/content/users/' + username + '?'

    userContent = urllib.urlopen(stem + parameters).read()
    folders = json.loads(userContent)['folders']

    return userContent, parameters, folders

def get_agol_items(username, feature_types):
    '''
    Adapted from: https://gist.github.com/oevans/6128188
    :param username: used in request path
    :param feature type: feature type we want to categorize (e.g., feature service)
    :return: a dictionary with folder_name, folder_id, item_name, item_id
    '''

    item_dict = {}
    userContent, parameters, folders = get_agol_user_content(username)

    paths = []
    for folder in folders:
        path = 'https://www.arcgis.com/sharing/rest/content/users/' + username + '/' + folder['id'] + '?'
        paths.append(path)

    for path in paths:
        userContent = urllib.urlopen(path + parameters).read()
        current_folder = json.loads(userContent)['currentFolder']
        items = json.loads(userContent)['items']

        for feature_type in feature_types:
            for item in items:
                if feature_type == item['type']:
                    item_id = item['id']
                    item_dict[item_id] = {}

                    item_dict[item_id]['folder_name'] = current_folder['title']
                    item_dict[item_id]['folder_id'] = current_folder['id']
                    item_dict[item_id]['title'] = item['title']
                    item_dict[item_id]['type'] = item['type']

    return item_dict
