import arcpy_metadata as md
import glob
import os
import logging

from utilities import arcgis_online
from arcgis_metadata import ArcgisMetadata

class XmlFile(ArcgisMetadata):
    """
    XmlFile class inherits from ArcgisMetadata class
    """

    def __init__(self, metadata_dict):
        logging.debug('Starting Xml Class')

        super(XmlFile, self).__init__(metadata_dict)

    def create_metadata_xmls(self, titles):
        '''
        Modeled from: https://github.com/wri/arcpy_metadata/blob/master/arcpy_metadata/metadata_editor.py#L207
        Creates empty xml files for the inputs
        :param titles: list of titles for the xml files
        '''

        for title in titles:

            try:

                if self.download_workspace + "\\" + title + ".xml" in glob.glob(self.download_workspace + "\\*"):
                    logging.debug("xml already created for {}".format(title))
                else:
                    md.MetadataEditor(metadata_file= self.download_workspace + "\\" + title + ".xml")
                    logging.debug("xml file created for {}".format(title))

            except NameError as inst:
                logging.debug("error for {0}, {1}".format(title, inst))

    def sync_metadata_xmls(self, metadata, items):
        '''
        method to sync metadata from spreadhseet to xml files
        '''
        #first make sure all xmls are there
        #Need ids for both document links and feature services types
        agol_ids = []
        for key in items:
            agol_ids.append(key)

        self.create_metadata_xmls(agol_ids)

        #match metadata xml id with agol id listed in metadata spreadsheet
        logging.debug("Starting xml sync")
        for xml in glob.glob(self.download_workspace + "\\*"):
            item_id = os.path.basename(xml).split(".")[0]
            for key in metadata:
                if item_id in metadata[key]['ArcGIS Online Item ID'].split(','):
                    try:
                        #Add core metadata fields
                        write = md.MetadataEditor(metadata_file=xml)
                        write.title = metadata[key]['Title']
                        write.purpose = metadata[key]['Function']
                        # write.scale_resolution = metadata[key]['Resolution']
                        write.extent_description = metadata[key]['Geographic Coverage']
                        write.source = metadata[key]['Source']
                        write.update_frequency_description = metadata[key]['Frequency of Updates']
                        write.temporal_extent_description = metadata[key]['Date of Content']
                        write.limitation = metadata[key]['License']
                        write.supplemental_information = metadata[key]['Cautions']
                        write.abstract = metadata[key]['Overview']
                        write.citation = metadata[key]['Citation']
                        logging.debug("Core metadata added for %s" %(key))

                        #Add online resources (download links)
                        logging.debug("Adding online resources")

                        if write.online_resource:
                            logging.debug("popping off existing resources for %s" %(key))
                            write.online_resource.pop()
                            logging.debug("popped")

                        if metadata[key]['Link to Data in Amazon S3']:
                            write.online_resource.new()
                            write.online_resource[0].link = metadata[key]['Link to Data in Amazon S3']
                            write.online_resource[0].name = 'Direct Download'
                            write.online_resource[0].function = 'download'
                            logging.debug('Direct Download added for %s' %(key))
                        else:
                            logging.debug("{} has no S3 link".format(key))

                        # Add learn more links to online resources
                        logging.debug("Adding Learn more links")

                        if metadata[key]['Learn More']:
                            write.online_resource.new()
                            write.online_resource[1].link = metadata[key]['Learn More']
                            write.online_resource[1].name = 'Learn More'
                            write.online_resource[1].function = 'download'
                            logging.debug('Learn more link added for %s' %(key))
                        else:
                            logging.debug("{} has no learn more link".format(key))

                        #Add tags
                        logging.debug("Adding Tags")
                        write.tags = metadata[key]['Tags'].split(',')
                        logging.debug('Tags added for %s' %(key))

                        #Save metadata
                        logging.debug("Saving metadata")
                        write.save()
                        write.cleanup()
                        write.finish()

                    except Exception as e:
                        logging.debug("error for {} because {}".format(item_id, str(e)))

                        if "acii" or "no element found" in str(e):
                            write.abstract = self.metadata_og[key]['Overview']
                            logging.debug("wrote original overview for %s" %(key))

    def update(self):

        self.sync_metadata_xmls(self.metadata_dict, self.items)
