# -*- coding: utf-8 -*-
__title__ = "Links"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 19.05.2024
_____________________________________________________________________
Description:

Get the Names, Workset, and PBP's values from Revit Links in the model.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [13.05.2024] - 1 RELEASE
- [13.06.2024] - 2 RELEASE (Exception for no links)
_____________________________________________________________________
Author: Nattalie Mor"""# Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Nattalie Mor"                                       # Script's Author
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2024                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import os, sys, math, datetime, time                            # Regular Imports

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference('RevitAPI')
clr.AddReference("System")                  # Reference System.dll for import.
clr.AddReference('RevitServices')
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

# pyRevit
from pyrevit import script, forms                                     # import pyRevit modules. (Lots of useful features)

#from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, RevitLinkInstance, XYZ, BuiltInParameter  # or Import only classes that are used.
# Custom Imports
from Snippets._convert import convert_internal_to_m                     # lib import



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

def collect_link_names(doc):
    link_collector = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
    link_names = []
    for link in link_collector:
        try:
            link_name = link.Name
            link_location = link_name.split("location")[1]
            link_type_name = link.GetLinkDocument().Title
            link_names.append((link_name, link_type_name, link_location))
        except Exception as e:
            link_name = link.Name
            link_type_name = link_name.split(".rvt")[0]
            link_location = "Not Loaded"
            link_names.append((link_name, link_type_name, link_location))
            #output.print_md("**Error processing link: {}** - {}".format(link.Name, str(e)))
    return link_names

""""if not link_collector:
    forms.alert("There are no Revit Links in the document.", "Revit Links", "Tool has been developed by Miss BIM")
else:"""

def collect_project_base_points(doc):
    base_point_category = BuiltInCategory.OST_ProjectBasePoint
    link_collector = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
    base_point_values = []
    for link in link_collector:
        link_doc = link.GetLinkDocument()
        if not link_doc:
            base_point_values.append(("N/A", "N/A", "N/A", "N/A"))
            continue
        project_base_points = FilteredElementCollector(link_doc).OfCategory(base_point_category).WhereElementIsNotElementType().ToElements()
        if project_base_points:
            project_base_point = project_base_points[0]
            north_south_PARAM = project_base_point.LookupParameter("N/S")
            east_west_PARAM = project_base_point.LookupParameter("E/W")
            elevation_PARAM = project_base_point.LookupParameter("Elevation")
            angle_to_true_north_PARAM = project_base_point.LookupParameter("Angle to True North")

            north_south = north_south_PARAM.AsValueString() if north_south_PARAM else "Not Set"
            east_west = east_west_PARAM.AsValueString() if east_west_PARAM else "Not Set"
            elevation = elevation_PARAM.AsValueString() if elevation_PARAM else "Not Set"
            angle_to_true_north = angle_to_true_north_PARAM.AsValueString() if angle_to_true_north_PARAM else "Not Set"
            base_point_values.append((north_south, east_west, elevation, angle_to_true_north))
        else:
            base_point_values.append(("N/A", "N/A", "N/A", "N/A"))
    return base_point_values


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
        return "Model is not Workshared"


# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# Collect link names
link_names = collect_link_names(doc)

# Collect project base point values
project_base_points = collect_project_base_points(doc)

# Collect worksets
workset_names = []

for link in FilteredElementCollector(doc).OfClass(RevitLinkInstance):
    workset_name = get_workset_name(link)
    workset_names.append(workset_name)

combined_data = []
for (link_name, link_type, link_location), workset_name, project_base_point in zip(link_names, workset_names, project_base_points):
    combined_data.append((link_name, link_type, link_location, workset_name) + project_base_point)

combined_data.sort(key=lambda x: x[0])


if not link_names:
    forms.alert("There are no Links in the project", "RVT Links", "Tool has been developed by Miss BIM.")
else:
    output = script.get_output()
    output.print_table(
        table_data=combined_data,
        title="Revit Links",
        columns=["Link Name", "Link Type", "Shared Site", "Workset", "N/S", "E/W", "Elevation", "Angle to True North"]
    )
    print("-" * 50)
    print('Tool has been developed by Miss BIM.')
