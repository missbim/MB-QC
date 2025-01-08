# -*- coding: utf-8 -*-
__title__ = "Floors Structure"
__author__ = "Nattalie Mor"
__version__ = 'Version: 1'
__doc__ = """Version: 1
Date    = 18.08.2024
_____________________________________________________________________
Description:

Export elements from selected levels.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [18.08.2024] - 1 REALESE
_____________________________________________________________________
Author: Nattalie Mor"""
from pyrevit import forms, script
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection, ObjectType

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
#.NET Imports
import clr
clr.AddReference('System')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.UI import TaskDialog, UIApplication, RevitCommandId, PostableCommand
from Autodesk.Revit.DB import *
from rpw.ui.forms import FlexForm, ComboBox, Label, Separator, TextBox, Button
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import Pipe
from Autodesk.Revit.DB.Mechanical import Duct
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
uiapp  = DocumentManager.Instance.CurrentUIApplication
doc    = __revit__.ActiveUIDocument.Document
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ==================================================

class ISF_box(ISelectionFilter):
    def AllowElement(self, element):
        # Check if the element is either a scope box or a section box
        if element.Category.Id.IntegerValue == int(BuiltInCategory.OST_VolumeOfInterest) or element.Category.Id.IntegerValue == int(BuiltInCategory.OST_SectionBox):
            return True
        return False
    def AllowReference(self, reference, position):
        # Not needed for this filter but must be implemented
        return True

# Apply ISelectionFilter to PickElementsByRectangle

levels = FilteredElementCollector(doc)\
                .OfCategory(BuiltInCategory.OST_Levels)\
                .WhereElementIsNotElementType()\
                .ToElements()


basic_floors_param = ParameterValueProvider(ElementId(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM))
f_rule = FilterStringRule(basic_floors_param, FilterStringEquals(), "Floor")
basic_floors_filter = ElementParameterFilter(f_rule)
floor_types = FilteredElementCollector(doc).OfClass(FloorType).WherePasses(basic_floors_filter).ToElements()

output = script.get_output()

# ╔╗ ╔═╗╦ ╦╔╗╔╔╦╗╦╔╗╔╔═╗  ╔╗ ╔═╗═╗ ╦  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ╠╩╗║ ║║ ║║║║ ║║║║║║║ ╦  ╠╩╗║ ║╔╩╦╝  ║║║║ ║ ║╣ ╠╦╝╚═╗║╣ ║   ║ ╚═╗  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╚═╝╚═╝╝╚╝═╩╝╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╚═  ╩╝╚╝ ╩ ╚═╝╩╚═╚═╝╚═╝╚═╝ ╩ ╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═

floor_type_info = []

for floor_type in floor_types:
    floor_name = floor_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    floor_width = floor_type.get_Parameter(BuiltInParameter.FLOOR_ATTR_DEFAULT_THICKNESS_PARAM).AsDouble()
    floor_structure = floor_type.GetCompoundStructure()
    firstlayercore = floor_structure.GetFirstCoreLayerIndex()
    lastlayercore = floor_structure.GetLastCoreLayerIndex()
    floor_layers = floor_structure.GetLayers()

    layer_info_table = (
        "<table border='1'><tr><th>Layer</th><th>Material</th><th>Thickness (cm)</th><th>Inside Core</th></tr>"
    )
    layer_info = []
    for layer in floor_layers:
        layer_name = layer.Function.ToString()
        lay_id = int(layer.LayerId)
        if firstlayercore <= lay_id <= lastlayercore:
            iscore = "✅"
        else:
            iscore = ""
        layer_mat = doc.GetElement(layer.MaterialId)
        if layer_mat:
            mat_name = layer_mat.Name.encode('utf-8').decode('utf-8')
        else:
            mat_name = "No Material"
        layer_width_cm = UnitUtils.ConvertFromInternalUnits(layer.Width, UnitTypeId.Centimeters)

        layer_info_table += "<tr><td>" + layer_name + "</td><td>" + mat_name + "</td><td>" + str(layer_width_cm) + "</td><td>" + str(iscore) + "</td><tr>"
    layer_info_table += "</table>"
        # layer_info.append({
        #     'Layer': layer_name,
        #     'Material': mat_name,
        #     'Thickness': layer_width_cm,
        # })
    floor_width_cm = UnitUtils.ConvertFromInternalUnits(floor_width, UnitTypeId.Centimeters)
    floor_function = floor_type.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString()
    if floor_type.get_Parameter(BuiltInParameter.STRUCTURAL_MATERIAL_PARAM):
        floor_material = floor_type.get_Parameter(BuiltInParameter.STRUCTURAL_MATERIAL_PARAM).AsValueString()
    else:
        floor_material = "No Structural Material"
    linkify_floor_type = output.linkify(floor_type.Id)

    floor_type_info .append({
        'Name': floor_name,
        'Width': floor_width_cm,
        'Function': floor_function,
        'Structural Material': floor_material,
        'Layers': layer_info_table,
        'Look up': linkify_floor_type,
    })

def sort_floor_type(floors_type):
    return sorted(floors_type, key=lambda floor_name: floor_name['Name'])

# Sort the levels
sorted_floors = sort_floor_type(floor_type_info)

if not floor_type_info:
    forms.alert("There are no floor type in the project", "floor Types", "Tool has been developed by Miss BIM.")

else:
    output = script.get_output()
    output.print_table(
        table_data=[[floor['Name'], floor['Width'], floor['Function'], floor['Structural Material'], floor['Layers'], floor['Look up']] for floor in sorted_floors],
        title="Basic floor Types",
        columns=["Name", "Width (cm)", "Function", "Structural Material","layers", "Look up"]
    )
    print("-" * 50)
    print('Tool has been developed by Miss BIM.')