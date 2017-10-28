'''Class for converting markdown to html then cleaning and  escaping the html for AGOL'''

import logging
import html
import markdown2
import re
import sys

# -*- coding: utf-8 -*-
class HtmlEncoder(object):

    def html_clean_up(self, text):
        """add html encoding"""

        #set default encoding
        reload(sys)
        sys.setdefaultencoding('utf8')

        #First remove any encoding errors
        if isinstance(text,unicode) == False:
            try:
                html_clean = unicode(text, errors='replace')
                logging.debug("html decoded")
            except TypeError, e:
                logging.debug("failed to decode because" + str(e))
        else:
            html_clean = text
            logging.debug("overview already unicode")

        #then create html encoding
        html_text = markdown2.markdown(html_clean)
        logging.debug('html encoding added')

        #remove breaks
        html_breaks = re.sub('\n', '', html_text)

        #encode to utf-8
        try:
            html_final = html_breaks.encode('utf-8')
        except UnicodeDecodeError, e:
            logging.debug("failed to encode utf8 because" + str(e))

        return html_final
