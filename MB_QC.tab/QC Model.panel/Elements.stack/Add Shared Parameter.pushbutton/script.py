# -*- coding: utf-8 -*-
__title__ = "Miss BIM CopyRight"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 27.06.2024
_____________________________________________________________________
Description:

Create a New Shared Parameter and assign to Categories.

_____________________________________________________________________
How-to:

- Enter Parameter Name
- Enter Parameter Group in the Shared Parameter Folder
- Choose Parameter Type Storage
- Choose Parameter Group
- Choose instance or Type Parameter
- Enter Names of Categories to assign the Parameter to
_____________________________________________________________________
Last update:
- [27.06.2024] - 1 REALESE
- [23.10.2024] - 1 REALESE
_____________________________________________________________________
Author: Nattalie Mor"""# Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Nattalie Mor"                                       # Script's Author
#__helpurl__ = "https://www.youtube.com/watch?v=YhL_iOKH-1M"     # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__ = "new"                                           # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2024                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.


# Import necessary modules
from pyrevit import revit, DB
from pyrevit import forms, script

# File path to the shared parameters file
shared_param_file = r'C:\Users\natim\Dropbox\Miss BIM\Template\MissBIM_Shared Parameters.txt'
# Shared parameters names
param_1 = "Copy Rights"
param_2 = "Copy Rights®Miss BIM"

# Open shared parameters file
app = revit.doc.Application
app.SharedParametersFilename = shared_param_file
shared_param_file = app.OpenSharedParameterFile()

# Find the parameters in the shared parameters file
def get_shared_parameter_definition(param_name):
    for group in shared_param_file.Groups:
        for defn in group.Definitions:
            if defn.Name == param_name:
                return defn
    return None

# Add shared parameters to the document
def add_shared_parameter(param_def, param_group, is_instance=False):
    with revit.Transaction('Add Shared Parameter'):
        # Set up the binding
        param_binding = revit.doc.FamilyManager if revit.doc.IsFamilyDocument else revit.doc.ParameterBindings
        if not revit.doc.IsFamilyDocument:
            # Create binding for project documents
            binding = DB.InstanceBinding(app.Create.NewCategorySet())
            revit.doc.ParameterBindings.Insert(param_def, binding, param_group)
        else:
            # Create parameter for family documents
            family_manager = revit.doc.FamilyManager
            family_manager.AddParameter(param_def, param_group, is_instance)

# Add the formula to the shared parameter in family or project
def set_parameter_formula(param_name, formula):
    if revit.doc.IsFamilyDocument:
        with revit.Transaction("Set Parameter Formula"):
            param = revit.doc.FamilyManager.get_Parameter(param_name)
            if param:
                revit.doc.FamilyManager.SetFormula(param, formula)
    else:
        with revit.Transaction("Set Parameter Formula"):
            param = revit.doc.GetElement(param_name)
            if param:
                param.SetFormula(formula)


# Get shared parameters definitions
param_1_def = get_shared_parameter_definition(param_1)
param_2_def = get_shared_parameter_definition(param_2)

if param_1_def and param_2_def:
    # Add shared parameters to the document under 'Identity Data' group
    group = DB.BuiltInParameterGroup.PG_IDENTITY_DATA
    add_shared_parameter(param_1_def, group)
    add_shared_parameter(param_2_def, group)

    # Set formulas
    set_parameter_formula(param_1, 'Copy Rights®Miss BIM')
    set_parameter_formula(param_2, '"Miss BIM"')
else:
    script.exit('Shared parameters not found.')