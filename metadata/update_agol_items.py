import requests
import glob
import json
import logging
import os

from arcgis_metadata import ArcgisMetadata
from utilities import arcgis_online

class AgolItems(ArcgisMetadata):
    """
    AgolItems class inherits from ArcgisMetadata class
    """

    def __init__(self, metadata_dict):
        logging.debug('Starting AgolItems Class')

        super(AgolItems, self).__init__(metadata_dict)

    def update_agol_metadata(self, user, items):
        logging.debug('Starting agol metadata udpate')

        #request token for ArcGIS Online
        token = arcgis_online.request_token('arcgis_online.config')

        #list xmls in download workspace
        metadata_xmls = glob.glob(self.download_workspace + '\\*')

        #update params
        d = {"overwrite": "true",
             "token" :token,
             "f":"json"}

        #match xmls with items and send post with metadata
        for xml in metadata_xmls:
            xml_id = os.path.basename(xml).split(".")[0]
            for key in items:
                if xml_id == key:
                    f = {'metadata': ('metadata.xml', open(xml, 'rb'), 'text/xml', {'Expires': '0'})}
                    url = 'http://www.arcgis.com/sharing/rest/content/users/{0}/{1}/items/{2}/update'.format(user, items[key]['folder_id'], key)

                    r = requests.post(url, data = d, files = f)
                    response = json.loads(r.content)

                    # if 'error' in response.keys():
                    #     logging.debug("error for {0} because {1}".format(items[key]['title'], response['error'])
                    # else:
                    #     logging.debug(response)

                    logging.debug(response)

    def update(self):

        self.update_agol_metadata('GlobalForestWatch', self.items)
