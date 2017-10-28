import requests
import json
import gspread
import os
import logging
from oauth2client.service_account import ServiceAccountCredentials

def open_spreadsheet(sheet_name, custom_key=False):
    """
    Open the spreadsheet for read/update
    :return: a gspread wks object that can be used to edit/update a given sheet
    """

    spreadsheet_file = r"D:\scripts\gfw-agol-tools\tokens\metadata_spreadsheet.json"

    if custom_key:
        spreadsheet_key = custom_key
    else:
        spreadsheet_key = r'1hJ48cMrADMEJ67L5hTQbT5hhV20YCJHpN1NwjXiC3pI'

    # Updated for oauth2client
    # http://gspread.readthedocs.org/en/latest/oauth2.html
    credentials = ServiceAccountCredentials.from_json_keyfile_name(spreadsheet_file,
                                                                   ['https://spreadsheets.google.com/feeds'])

    gc = gspread.authorize(credentials)
    wks = gc.open_by_key(spreadsheet_key).worksheet(sheet_name)

    return wks

def sheet_to_dict(sheet_name):
    """
    Convert the spreadsheet to a dict with {layername: {colName: colVal, colName2: colVal}
    :param gfw_env: the name of the sheet to call (prod | staging)
    :return: a dictionary representing the sheet
    """

    sheet_as_dict = {}
    wks = open_spreadsheet(sheet_name)
    gdoc_as_lists = wks.get_all_values()

    # Pull the header row from the Google doc
    header_row = gdoc_as_lists[0]

    # Iterate over the remaining data rows
    for dataRow in gdoc_as_lists[1:]:

        # Build a dictionary for each row with the column title
        # as the key and the value of that row as the value
        row_as_dict = {k: v for (k, v) in zip(header_row, dataRow)}

        # Grab the technical title (what we know the layer as)
        layer_name = row_as_dict['Technical Title']

        # Add that as a key to the larger outDict dictionary
        sheet_as_dict[layer_name] = {}

        # For the values in each row, add them to the row-level dictionary
        for key, value in row_as_dict.iteritems():
            sheet_as_dict[layer_name][key] = value

    return sheet_as_dict
