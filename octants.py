# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:16:33 2018

@author: solis

lee el shp que contiene los límites de hojas 1:50000
    y genera un nuevo shp de octantes
"""

# número de divisiones de octantes en el eje X
NXOCT = 4
# número de divisiones de octantes en el eje Y
NYOCT = 2
# número de puntos en el eje X del octante (NPXOCT + 1)
NPXOCT = 4
# número de puntos en el eje Y del octante (NPYOCT + 1)
NPYOCT = 2


def octants():
    """
    lee el shp que contiene los límites de hojas 1:50000
        y genera un nuevo shp de octantes
    El nombre del shp de datos y resultados los toma del módulo
        octants_parameters
    """
    from os.path import join
    import octants_parameters as par
    import ogr
    import gdal

    file_tmp = open('tmp.txt', 'w')

    gdal.UseExceptions()

    drv_name = "ESRI Shapefile"
    data_file_name = join(par.dir_dat, par.file_dat)

    drv = ogr.GetDriverByName(drv_name)
    fi_shp = drv.Open(data_file_name, 0)
    if fi_shp is None:
        raise ValueError('No se puede abrir {}'.format(data_file_name))
    layer = fi_shp.GetLayer()
    if layer.GetGeomType() != 3:
        raise ValueError('La capa de fichero debe ser de tipo polígono')
    fCount = layer.GetFeatureCount()
    print('\n{}\n{}\nFeatures number: {:d}'.format(data_file_name,
          layer.GetSpatialRef(),
          fCount))

    for feature in layer:
        fid = feature.GetFID()
        field_names = feature.keys()
        field_contents = feature.items()
        # field_geom = feature.geometry()

        geomr = feature.GetGeometryRef()
        box = geomr.GetEnvelope()
        file_tmp.write('{}\t{}\t{}\t{}\n'.format(*box))
        for points in _point_octants_get(box):
            write_points(file_tmp, points)
    file_tmp.close()

#        octs = _get_octants_as_points(lines)

#        Create ring
#        ring = ogr.Geometry(ogr.wkbLinearRing)
#        ring.AddPoint(lrX, lrY)
#        ring.AddPoint(lrX, ulY)
#        ring.AddPoint(ulX, ulY)
#        ring.AddPoint(ulX, lrY)
#        ring.AddPoint(lrX, lrY)

#        Create polygon
#        poly = ogr.Geometry(ogr.wkbPolygon)
#        poly.AddGeometry(ring)

    fi_shp = None


def _point_octants_get(box: []):
    """
    genera los puntos de los 8 octantes

    input
    box: tuple de 4 elementos float con los valores de xmin xmax, ymin, ymax

    output
    a list
    """
    lengthx = abs(box[0] - box[1])
    lengthy = abs(box[2] - box[3])
    lx_oct = lengthx / float(NXOCT)
    ly_oct = lengthy / float(NYOCT)
    lx_point = lx_oct / float(NPXOCT)
    ly_point = ly_oct / float(NPYOCT)

    x0 = box[0]
    y0 = box[1]
    for i in range(NXOCT):
        x0 = x0 + float(i) * lx_oct
        y0 = y0 + float(i) * ly_oct
        yield(_points_octant(x0, y0, lx_point, ly_point, NPXOCT, NPYOCT))

    x0 = box[0]
    y0 = box[1] + ly_oct
    for i in range(NXOCT):
        x0 = x0 + float(i) * lx_oct
        y0 = y0 + float(i) * ly_oct
        yield(_points_octant(x0, y0, lx_point, ly_point, NPXOCT, NPYOCT))


def _xymin_oct(octante, n):
    """
    devuelve los valores xmin y ymin de un octante
    """
    return octante[n][0], octante[n][1]


def _points_octant(xmin, ymin, lx_point, ly_point, NPXOCT, NPYOCT):
    """
    genera las coordenadas de un octante a partir de las coordenadas de la
        esquina inferior izquierda
    """
    # linea inferior
    xy = [(xmin, ymin)]
    for i in range(NPXOCT):
        xy.append((xy[-1][0] - lx_point, xy[-1][1]))
    # linea derecha
    for i in range(NPYOCT + 1):
        xy.append((xy[-1][0], xy[-1][1] + ly_point))
    # linea superior
    for i in range(NPXOCT + 1):
        xy.append((xy[-1][0] + lx_point, xy[-1][1]))
    # linea izquierda
    for i in range(NPYOCT + 1):
        xy.append((xy[-1][0], xy[-1][1] - ly_point))
    xy.append((xmin, ymin))
    return xy


def _direc(deltax, deltay):
    """
    determina la dirección
    """
    if deltax < deltay:
        return 'V'
    elif deltax > deltay:
        return 'H'
    else:
        raise ValueError('deltax EQ deltay')


def _get_lines_as_points(xs, ys):
    """
    A partir de los puntos de un poligono de una hoja 1:50000, seleccciona
        las líneas
    """
    direc0 = None
    points = [(xs[0], ys[0])]
    lines = []
    for i, (x1, y1) in enumerate(zip(xs[1:], ys[1:])):
        deltax = abs(x1 - xs[i])
        deltay = abs(y1 - ys[i])
        if direc0 is None:
            direc0 = _direc(deltax, deltay)
            points.append((x1, y1))
            continue
        direc = _direc(deltax, deltay)
        if direc != direc0:
            lines.append(points)
            points = [(xs[i], ys[i])]
            points.append((x1, y1))
            direc0 = direc
        else:
            points.append((x1, y1))
    lines.append(points)
    fo = open('tmp.txt', 'w')
    for line in lines:
        for xy in line:
            fo.write('{:f}\t{:f}\n'.format(xy[0], xy[1]))
        fo.write('\n')
    fo.close()
    return lines


def write_points(fo, xy: []):
    """
    escribo un array de puntos
    """
    fo.write('\n')
    for xy1 in xy:
        fo.write('{:f}\t{:f}\n'.format(xy1[0], xy1[1]))

# def _get_octants_as_points(lines):
#    """
#    forma los octantes a partir de las 4 líneas de una hoja
#    """
#    lengths = []
#    for line in lines:
#        cut_points = []
#        deltax = abs(line[0][0] - line[1][0])
#        deltay = abs(line[0][1] - line[1][1])
#        direc = _direc(deltax, deltay)
#        length = length(np.linalg.norm((line[0][0], line[0][1]),
#                              (line[-1][0], line[-1][1])))
#        length = sqrt((line[0][0] - line[-1][0])**2 +
#                      (line[0][1] - line[-1][1])**2)
#        if direc == 'H':
#            length_oct = length / 4.
#        else:
#            length_oct = length / 2.
