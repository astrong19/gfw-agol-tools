# Admin Tools for ArcGIS Online- Designed for Global Forest Watch

This is a suite of tools used to manage [GFW's](http://globalforestwatch.org) ArcGIS Online and ArcGIS Open Data sites.

## Requirements

gfw-agol-tools is pure python and leverages arcpy (installed with ArcGIS), [arcpy_metadata](https://github.com/ucd-cws/arcpy_metadata) to sync metadata with xml files, and [gspread](https://github.com/burnash/gspread) to read the GFW metadata google sheet.

gfw-agol-tools requires access to the GFW metadata spreadsheet and ArcGIS Online account.

## Update Processes

This code will update GFW's ArcGIS Online items from information in GFW's metadata spreadsheet by matching the ArcGIS Online Item ID field in GFW's metadata spreadsheet with the Item ID in ArcGIS Online. A layer must have a ArcGIS Online Item ID present in the metadata spreadsheet for it to be updated in ArcGIS Online.

This script uses arg parse to separate update processes by arguments passed through the command line.
For example, to update metadata run the command:

`python sync.py -metadata`

To update thumbnails, run the command:

`python sync.py -thumbnails`

## Metadata Fields

A list of metadata fields that are synced with ArcGIS Online.

Field | Description
--- | ---
Title | Dataset's official name
Function | Short summary of what the data represents
Geographic Coverage | Keywords to describe the geographic scale of the data
Source | Attribution of the dataset (e.g., scientific journal or organization)
Frequency of Updates | Description of how frequently the data is updated
License | License under which data are published
Cautions | Use limitations to be aware of
Overview | Description or abstract of the data and methodology
Citation | How a user should cite the data
Online Resources | Links to additional downloads or external web pages
Tags | Descriptive keywords to make it easier to search for data
