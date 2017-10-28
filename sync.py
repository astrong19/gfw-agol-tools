import argparse

from metadata.update_xml_files import XmlFile
from metadata.update_agol_items import AgolItems
from metadata.arcgis_metadata import ArcgisMetadata
from thumbnails.update_agol_thumbnails import AgolThumbnails
from utilities import google_sheet
from utilities import logger
from utilities import settings

def main():
    '''master method to call sub-methods'''

    #parse command line arguments
    parser = argparse.ArgumentParser(description='Separate AGOL update processes in command line')
    parser.add_argument('--process', '-p', required=True, choices=['metadata', 'thumbnails'],
                        help='the update process to kick off')
    args = parser.parse_args()

    # Instantiate logger; write to {dir}\logs
    logging = logger.build_logger()
    logging.info("\n{0}\n{1} v{2}".format('*' * 50, settings.get_settings()['tool_info']['name'],
                                                 settings.get_settings()['tool_info']['version']))
    logging.critical('Starting | ArcGIS Online Update')

    #Get metadata spreadsheet as dict
    metadata_dict = google_sheet.sheet_to_dict('Form Responses 1')

    if args.process == "metadata":
        #update metadata xml files
        XmlFile(metadata_dict).update()
        logging.debug('xml sync finished')

        # sync xmls with items in ArcGIS Online
        AgolItems(metadata_dict).update()
        logging.debug('agol items synced')

    elif args.process == "thumbnails":
        #update AGOL thumbnails
        AgolThumbnails().update()
        logging.debug("agol thumbnails synced")

    else:
        #argument not identified repsonse
        logging.debug("please enter a valid argument")

    logging.critical('Finished | ArcGIS Online Update')

if __name__ == "__main__":
    main()
