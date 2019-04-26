# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:16:33 2018

@author: solis

lee el shp que contiene los límites de hojas 1:50000
    y genera un nuevo shp de octantes
"""

sql0 = ["set client_encoding to utf8;",
        "set standard_conforming_strings to on;",
        "select dropgeometrytable('mtn50oct');",
        "begin;",
        "drop table if exists mtn50oct;",
        "create schema if not exists ign;",
        "create table if not exists ign.mtn50oct (",
        "    gid serial primary key,",
        "    oct_clas varchar(11) unique);",
        "select AddGeometryColumn('ign','mtn50oct','geom',4019,'MULTIPOLYGON',2);"]

sql2 = 'create index mtn50oct_gist on mtn50oct using gist (geom);\ncommit;\n'



sfmtpsql = ("insert into mtn50oct (oct_clas, geom)",
            "values ('{0}-{1:d}',",
            "ST_GeomFromEWKT('SRID=4019;MULTIPOLYGON((({2})))'));\n")
fmtpoint = "%0.6f %0.6f"


def octants(dir_data, fshp):
    """
    lee el shp que contiene los límites de hojas 1:50000
        y genera un nuevo shp de octantes
    input
    dir_data: directorio del fichero ign shp de hojas del mtn50 (string)
    fshp: nombre y extensión del fichero shp (string)
    output
    null
    """
    from os.path import join, isfile
    import ogr
    import gdal

    gdal.UseExceptions()

    file_out = 'mtn50oct_epsg4019.sql'
    drv_name = "ESRI Shapefile"
    data_file_name = join(dir_data, fshp)
    if not isfile(data_file_name):
        raise ValueError('No se puede abrir {}'.format(data_file_name))

    drv = ogr.GetDriverByName(drv_name)
    fi_shp = drv.Open(data_file_name, 0)
    layer = fi_shp.GetLayer()
    if layer.GetGeomType() != 3:
        raise ValueError('La capa de fichero debe ser de tipo polígono')
    nfeatures = layer.GetFeatureCount()
    print('\n{}\n{}\nFeatures number: {:d}'.format(data_file_name,
          layer.GetSpatialRef(),
          nfeatures))

    fout = open(join(dir_data, file_out), 'w')
    line = '\n'.join(sql0)
    fout.write('{}\n'.format(line))

    for ifeat, feature in enumerate(layer):
        print('{0:d}/{1:d}'.format(ifeat+1, nfeatures))
        h50 = feature.GetField('mtn50_clas')
        geom = feature.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        npoints = ring.GetPointCount()
        if npoints != 33:
            continue
        points = [ring.GetPoint(i) for i in range(0, npoints)]
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        sqls = octantes_aswnt(h50, x, y)

        for sql1 in sqls:
            fout.write('{}'.format(sql1))
        fout.write('\n')
        if ifeat == 99999999:
            break
    fout.write(sql2)
    fout.close()


def octantes_aswnt(h50, x, y):
    """
    genera los octantes a partir de las coordenadas x e y de los puntos
        que definen la geometría de la hoja
    input
    h50: nombre de la hoja 1:50000 ign (string)
    x: lista de reales x coord.
    y: lista de reales y coord.
    output
    lista desentencias sql para insertar lo octantes como multipolígono
    """
    xmax = max(x)
    xmin = min(x)
    ymax = max(y)
    ymin = min(y)
    deltax = abs((xmin-xmax)/4.)
    deltay = (ymax-ymin)/2.
    ymedio = ymax - deltay
    fmtpsql = ' '.join(sfmtpsql)
    sql = []

    # octante1
    points = []
    points.append(fmtpoint % (xmin, ymax))    # 1
    x1 = xmin + deltax
    points.append(fmtpoint % (x1, ymax))      # 2
    points.append(fmtpoint % (x1, ymedio))    # 3
    points.append(fmtpoint % (xmin, ymedio))  # 4
    points.append(fmtpoint % (xmin, ymax))    # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 1, cadena_points))

    # octante2
    points = []
    points.append(fmtpoint % (x1, ymax))      # 1
    x2 = x1 + deltax
    points.append(fmtpoint % (x2, ymax))      # 2
    points.append(fmtpoint % (x2, ymedio))    # 3
    points.append(fmtpoint % (x1, ymedio))    # 4
    points.append(fmtpoint % (x1, ymax))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 2, cadena_points))

    # octante3
    points = []
    points.append(fmtpoint % (x2, ymax))      # 1
    x3 = x2 + deltax
    points.append(fmtpoint % (x3, ymax))      # 2
    points.append(fmtpoint % (x3, ymedio))    # 3
    points.append(fmtpoint % (x2, ymedio))    # 4
    points.append(fmtpoint % (x2, ymax))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 3, cadena_points))

    # octante4
    points = []
    points.append(fmtpoint % (x3, ymax))      # 1
    points.append(fmtpoint % (xmax, ymax))    # 2
    points.append(fmtpoint % (xmax, ymedio))  # 3
    points.append(fmtpoint % (x3, ymedio))    # 4
    points.append(fmtpoint % (x3, ymax))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 4, cadena_points))

    # octante5
    points = []
    points.append(fmtpoint % (xmin, ymedio))    # 1
    points.append(fmtpoint % (x1, ymedio))      # 2
    points.append(fmtpoint % (x1, ymin))        # 3
    points.append(fmtpoint % (xmin, ymin))      # 4
    points.append(fmtpoint % (xmin, ymedio))    # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 5, cadena_points))

    # octante6
    points = []
    points.append(fmtpoint % (x1, ymedio))      # 1
    points.append(fmtpoint % (x2, ymedio))      # 2
    points.append(fmtpoint % (x2, ymin))    # 3
    points.append(fmtpoint % (x1, ymin))    # 4
    points.append(fmtpoint % (x1, ymedio))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 6, cadena_points))

    # octante7
    points = []
    points.append(fmtpoint % (x2, ymedio))      # 1
    points.append(fmtpoint % (x3, ymedio))      # 2
    points.append(fmtpoint % (x3, ymin))        # 3
    points.append(fmtpoint % (x2, ymin))        # 4
    points.append(fmtpoint % (x2, ymedio))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 7, cadena_points))

    # octante8
    points = []
    points.append(fmtpoint % (x3, ymedio))      # 1
    points.append(fmtpoint % (xmax, ymedio))    # 2
    points.append(fmtpoint % (xmax, ymin))      # 3
    points.append(fmtpoint % (x3, ymin))        # 4
    points.append(fmtpoint % (x3, ymedio))      # 1
    cadena_points = ','.join(points)
    sql.append(fmtpsql.format(h50, 8, cadena_points))

    return sql
