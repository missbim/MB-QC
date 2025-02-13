# -*- coding: utf-8 -*-
__title__ = "Project Grids"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 13.06.2024
_____________________________________________________________________
Description:

Get the Names, Workset and Monitored source of the Project's Grids.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [13.06.2024] - 1 REALESE

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
import os, sys, math, datetime, time                            # Regular Imports

# pyRevit
from pyrevit import script, forms                                       # import pyRevit modules. (Lots of useful features)

#from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Level, Element, WorksharingUtils, BuiltInParameter, WorksetTable, ElementId, Workset, RevitLinkInstance, RevitLinkType  # or Import only classes that are used.

# Custom Imports
from Snippets._convert import convert_internal_to_m                     # lib import

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


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
# ==================================================
# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

# Check if the model is workshared
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


# Create a dictionary to map scope box IDs to their names
def create_scope_box_dict(doc):
    scope_boxes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
    return {sb.Id: sb.Name for sb in scope_boxes}

scope_box_dict = create_scope_box_dict(doc)

# Function to get the scope box name of an element
def get_scope_box_name(element):
    try:
        scope_box_id = element.get_Parameter(BuiltInParameter.DATUM_VOLUME_OF_INTEREST).AsElementId()
        if scope_box_id != ElementId.InvalidElementId and scope_box_id in scope_box_dict:
            return scope_box_dict[scope_box_id]
    except:
        pass
    return "No Scope Box"

def get_monitored_info(grid):
    monitored_info = []
    try:
        monitored_element_ids = grid.GetMonitoredLinkElementIds()
        for elem_id in monitored_element_ids:
            linked_element = doc.GetElement(elem_id)
            if linked_element:
                link_instance = linked_element.Document.GetElement(linked_element.GetTypeId())
                if isinstance(link_instance, RevitLinkInstance):
                    link_name = link_instance.Name
                else:
                    link_name = "Unknown Link"
                link_name = linked_element.Name
                type_name = link_name.split(".rvt")[0]
                monitored_info.append(type_name)
    except:
        pass
    if not monitored_info:
        return "Not Monitored"
    return monitored_info

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# Define the built-in category for Project Base Point
grids_category = BuiltInCategory.OST_Grids

# Create a collector to gather all levels in the document
grids = FilteredElementCollector(doc).OfCategory(grids_category).WhereElementIsNotElementType().ToElements()

# Initialize a list to store levels and their details
grids_info = []

for g in grids:
    grid_name = g.Name
    workset_name = get_workset_name(g)
    scope_box_name = get_scope_box_name(g)
    monitored_info = get_monitored_info(g)
    linkify_grid = output.linkify(g.Id)
    grids_info.append({
        'Name': grid_name,
        'Workset': workset_name,
        'Scope Box': scope_box_name,
        'Monitored By': monitored_info,
        'Look up': linkify_grid,
    })

# Function to sort levels by their elevation
def sort_grids(grids):
    return sorted(grids, key=lambda grid: grid['Name'])

# Sort the levels
sorted_grids = sort_grids(grids_info)

if not grids_info:
    forms.alert("There are no Grids in the project", "Project Grids", "Tool has been developed by Miss BIM.")
else:
    output = script.get_output()
    output.print_table(
        table_data=[[grid['Name'], grid['Workset'], grid['Scope Box'], grid['Monitored By'], grid['Look up']] for grid in sorted_grids],
        title="Grids",
        columns=["Name", "Workset", "Scope Box", "Monitored By", "Look up"]
    )
    print("-" * 50)
    print('Tool has been developed by Miss BIM.')
