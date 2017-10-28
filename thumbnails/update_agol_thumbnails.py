import logging
import os
import urllib
import json

from utilities import arcgis_online

#helpful: https://github.com/Esri/ago-tools/blob/master/samples/updateServiceItemsThumbnail.py
#https://github.com/Esri/ago-tools/blob/master/agoTools/admin.py#L416
class AgolThumbnails(object):
    """
    Class for updating Thumbnails in ArcGIS Online
    """

    def __init__(self):
        logging.debug('Starting AgolThumbnails Class')

        self.items = arcgis_online.get_agol_items('GlobalForestWatch', ['Feature Service', 'Document Link', 'Image Service'])

        self.download_workspace = r"G:"

        self.token = arcgis_online.request_token('arcgis_online.config')

        self.base_url = 'http://www.arcgis.com/sharing/rest/content/users/'

    def update_agol_thumbnails(self, user, items):
        logging.debug('Starting agol thumbnail udpate')

        for key in self.items:
            update_url = self.base_url + user + '/items/' + key + '/update'
            try:
                params = urllib.urlencode({'thumbnailURL' : 'http://gfw.blog.s3.amazonaws.com/ODP_images/thumbnails/{}.PNG'.format(key), 'token' : self.token, 'f' : 'json'})
                response = urllib.urlopen(update_url, params).read()
                message = json.loads(response)
                logging.debug(message)
            except Exception, e:
                logging.debug("{} not found".format(key) + str(e))


    def update(self):

        self.update_agol_thumbnails('GlobalForestWatch', self.items)
