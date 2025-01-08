# -*- coding: utf-8 -*-
__title__ = "Scope Box"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 17.05.2024
_____________________________________________________________________
Description:

Get the Names and Worksets of Project's Scopeboxes.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [17.05.2024] - 1 REALESE
- [13.06.2024] - 2 REALESE
Linkify Scope Box
_____________________________________________________________________
Author: Nattalie Mor"""# Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Nattalie Mor"                                       # Script's Author
#__helpurl__ = "https://www.youtube.com/watch?v=YhL_iOKH-1M"     # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__ = "new"                                           # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2024                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import os
#from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Element, WorksharingUtils, WorksetTable, BuiltInParameter   # or Import only classes that are used.

# pyRevit
from pyrevit import script, revit, forms                                        # import pyRevit modules. (Lots of useful features)

# Custom Imports
from Snippets._selection import get_selected_elements                   # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference('RevitAPI')
clr.AddReference("System")                  # Reference System.dll for import.
clr.AddReference('RevitServices')
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.
output = script.get_output()

# Define the built-in category for Scope Box
sbx_category = BuiltInCategory.OST_VolumeOfInterest

# Get all Project Base Points in the document
sbx = FilteredElementCollector(doc).OfCategory(sbx_category).WhereElementIsNotElementType().ToElements()

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
# ==================================================

# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.
def is_model_workshared(doc):
    return doc.IsWorkshared

is_workshared = is_model_workshared(doc)

# Function to get the workset name of an element
def get_workset_name(element):
    if is_workshared:
        try:
            workset_id = element.WorksetId
            workset = doc.GetWorksetTable().GetWorkset(workset_id)
            return workset.Name
        except:
            return "Unknown Workset"
    else:
        return "N/A"
# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
scope_box_worksets = []

if not sbx:
    forms.alert("No scope Boxes were found in the document","Scope Boxes",'Tool has been developed by Miss BIM.' )
else:
    for sb in sbx:
        if is_workshared:
            sb_name = sb.Name
            workset_id = sb.WorksetId
            workset = doc.GetWorksetTable().GetWorkset(workset_id)
            linkify_scopebox = output.linkify(sb.Id)
            scope_box_worksets.append([sb_name,workset.Name,linkify_scopebox])
        else:
            sb_name = sb.Name
            workset = "Model is not Workshared"
            linkify_scopebox = output.linkify(sb.Id)
            scope_box_worksets.append([sb_name,workset,linkify_scopebox])


    output = script.get_output()
    output.print_table(
        table_data=scope_box_worksets,
        title="Scope Box Worksets",
        columns=["Scope Box Name", "Workset Name"]
        )

    print("-" * 50)
    print('Tool has been developed by Miss BIM.')
