# -*- coding: utf-8 -*-
"""
@author: Julien Bourassa et Benoit Lemieux

#==============================================================================
Dependances:
- Le module "pandas" doit etre installe.
- Rouler le script avec python 2.7.

Description du fonctionnement du script:
1- Ouvrir le BOM generer par KiBom.
2- Lire le fichier.
3- Generer le csv Project_MasterBom.
4- Ecrire dans le Project_MasterBom.
5- Generer les csv Digikey_MasterBom, Wurth_MasterBom, autre_MasterBom.
6- Parser le csv pour les différents suppliers.
7- Ecrire dans les csv des suppliers respectifs.

Comment utiliser ce script?
1- Generer le BOM avec KiBOM comme a la normale.
2- Copier le BOM a "parser" dans le meme repertoire que ce script python.
3- Renommer le BOM "bom.csv".
4- Rouler le script.  Les BOMs Digikey et Wurth seront genere.

TO-DO:
- Interface graphique.
- Modifier KiBOM pour qu'il appelle ce script automatiquement.
- Ajouter le nom du responsable de la commande.
#==============================================================================
"""

# Import modules
import pandas as pd
import os

# Obtain file path.
from os import path

def bom_splitter(bom_file):

    fp = path.relpath("bom.csv")

    # Read KiBOM-generated BOM file.
    df1=pd.read_csv(fp)

    # Read columns standard for Eclipse parts orders.
    df2 = pd.DataFrame(df1, columns = ['Component', 'References', 'Value', 'Footprint', 'Quantity Per PCB', 'Description', 'Manufacturer', 'Manufacturer Part Number', 'Supplier', 'Supplier Part Number'])

    # Write new master BOM.  NOTE:  Really necessary???
    df2.to_csv('MasterBom.csv', index = False)

    # Include only imortant columns.
    df3 = pd.DataFrame(df1, columns = ['Manufacturer', 'Description', 'Manufacturer Part Number', 'Supplier', 'Supplier Part Number', 'Quantity Per PCB'])

    # Parse for Digikey Supplier.  Do not include Wurth Electronics parts.
    df4 = df3[df3['Supplier'].notnull() & (df3['Supplier'] == "Digikey")& (df3['Manufacturer'] != "Wurth Electronics Inc.")]
    # Index = 0.
    df4 = df4.reset_index(drop=True)
    # Index = 1.
    df4.index =  df4.index + 1
    # Write Digikey BOM.
    df4.to_csv('DigikeyBom.csv')

    # Scan for Wurth Electronics sponsored parts.
    df5 = df3[df3['Supplier'].notnull() & (df3['Manufacturer'] == "Wurth Electronics Inc.")]
    # Index = 0.
    df5 = df5.reset_index(drop=True)
    # Index = 1.
    df5.index =  df5.index + 1
    # Write Wurth BOM.
    df5.to_csv('WurthBom.csv')

    # Scan for other suppliers (Not Digikey or Wurth).
    df6 =  df3[df3['Supplier'].notnull() & (df3['Manufacturer'] != "Wurth Electronics Inc.") & (df3['Supplier'] != "Digikey")]
    # Index = 0.
    df6 = df6.reset_index(drop=True)
    # Index = 1.
    df6.index =  df6.index + 1
    # Write "Other" BOM.
    df6.to_csv('OtherBom.csv')

bom_file = path.relpath("bom.csv")
bom_splitter(bom_file)
#==============================================================================
# import tkinter
# from tkinter.filedialog import askopenfilename
#
#==============================================================================







#==============================================================================
# def browse():
#     global infile
#     infile=askopenfilename()
#
# def newfile();:
#     global oufile
#     outfine=askopenfilename()
#
# def BomFunction(outfile=outfile)
#     df = pandas.read_csv(infile)
#
#
#
#==============================================================================



#==============================================================================
#
# root=tkinter.Tk()
#
# root.title("Bom Generator")
#
#
# label=tkinter.Label(root, text="Bom Generator for Eclipse")
# label.pack()
#
#
# browseButton=tkinter.Button(root,text="Browse", command=browse)
# browseButton.pack()
#
#
#
# root.mainloop()
#
#
#==============================================================================



# For windows installer
# pip install pyinstaller
# pyinstaller --onefile --windoed "name.py"
