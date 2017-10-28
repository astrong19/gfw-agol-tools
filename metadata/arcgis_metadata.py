import logging

from utilities import arcgis_online
from utilities.metadata_cleanup import HtmlEncoder

class ArcgisMetadata(object):
    """
    A General ArcGIS Metadata class used to define an ArcGIS metadata environment
    and pass information to other metadata update classes
    """

    def __init__(self, metadata_dict):

        self.download_workspace = r"D:\data\gfw-sync-scratch\downloads\metadata"

        self.metadata_og = metadata_dict

        self.metadata_dict = self.clean_overview(metadata_dict)

        self.items = arcgis_online.get_agol_items('GlobalForestWatch', ['Feature Service', 'Document Link', 'Image Service'])


    def clean_overview(self, metadata_dict):
        '''clean metadata from html and other encoding'''

        for layer in metadata_dict:
            #clean overview
            overview_clean = HtmlEncoder().html_clean_up(metadata_dict[layer]['Overview'])
            metadata_dict[layer]['Overview'] = overview_clean
            #clean cautions
            cautions_clean = HtmlEncoder().html_clean_up(metadata_dict[layer]['Cautions'])
            metadata_dict[layer]['Cautions'] = cautions_clean

        return metadata_dict
