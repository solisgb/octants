# -*- coding: utf-8 -*-
"""
@author: solis

parameters
"""

# número de divisiones de octantes en el eje X
NXOCT = 4
# número de divisiones de octantes en el eje Y
NYOCT = 2
# número de puntos en el eje X del octante - sin contar los puntos extremos-
NPXOCT = 4
# número de puntos en el eje Y del octante - sin contar los puntos extremos-
NPYOCT = 2

# ====== NOMBRES DE FICHEROS Y DIRECTORIOS ====================================

home = 0

if home:
    dir_dat = r'C:\Users\solis\Documents\LAYERS\DEV'
    file_dat = 'IGN50_3POLIGONOS.shp'
    dir_out = r'C:\Users\solis\Documents\LAYERS\DEV\out'
    file_out = 'IGN50_3POLIGONOS_octs.shp'
else:
    dir_dat = r'C:\Users\solil\Documents\LUIS\GIS\LAYERS'
    file_dat = 'test_3h50_4019.shp'
    dir_out = r'C:\Users\solil\Documents\LUIS\GIS\LAYERS\out'
    file_out = 'octants_test_4019.shp'
