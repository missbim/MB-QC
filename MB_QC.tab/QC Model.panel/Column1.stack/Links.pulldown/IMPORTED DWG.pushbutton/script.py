# -*- coding: utf-8 -*-
__title__ = "DWG IMPORTS"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 21.05.2024
_____________________________________________________________________
Description:

Get the names of imported DWG files in the model.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [21.05.2024] - 1 RELEASE
- [13.06.2024] - 2 RELEASE (Linkify DWG)

_____________________________________________________________________
Author: Nattalie Mor"""# Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Nattalie Mor"                                       # Script's Author
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2024                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
import os, sys, math, datetime, time                            # Regular Imports
# pyRevit
from pyrevit import script, revit, DB, forms   # import pyRevit modules. (Lots of useful features)
from pyrevit.framework import List

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference('RevitAPI')
clr.AddReference("System")                  # Reference System.dll for import.
clr.AddReference('RevitServices')
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

#from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import FilteredElementCollector, ImportInstance, CADLinkType, BuiltInParameter, View  # or Import only classes that are used.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.
output = script.get_output()

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
# ==================================================
# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.


# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# ==================================================
# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# Collect all ImportInstance elements
imported_cads = FilteredElementCollector(doc).OfClass(ImportInstance)
# List to store names of imported DWGs
dwg_info = []

# Iterate through imported CADs and collect their names and views
for dwg in imported_cads:
    if not dwg.IsLinked:
        symbol = doc.GetElement(dwg.GetTypeId())
        dwg_name = symbol.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        view_id = dwg.OwnerViewId
        linkify_dwg = output.linkify(dwg.Id)

        if view_id != DB.ElementId.InvalidElementId:
            view = doc.GetElement(view_id)
            view_name = view.Name if view else "Unknown View"
        else:
            view_name = "Not Placed in a View"

        dwg_info.append([dwg_name, view_name,linkify_dwg])

# Report the number of imported DWGs
if not dwg_info:
    forms.alert("There are no Imported CADs","DWG IMPORT",'Tool has been developed by Miss BIM.' )
else:
    output = script.get_output()
    output.print_table(
        table_data=dwg_info,
        title="IMPORTED CAD",
        columns=["File Name","View Name", "Lookup"]
    )
    print("-" * 50)
    print('Tool has been developed by Miss BIM.')




