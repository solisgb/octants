# -*- coding: utf-8 -*-
"""
paso un gml de tipo point  a txt separado por tabulador
    con las coordenadas verdaderas del punto
"""

if __name__ == "__main__":

    try:
        from datetime import timedelta
        from time import time
        import log_file as lf
        from octants import octants

        startTime = time()

        octants()

        xtime = time() - startTime
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
    except Exception as error:
        import traceback
        import logging
        logging.error(traceback.format_exc())
        msg = '\n{}'.format(traceback.format_exc())
        lf.write(error.__doc__)
        lf.write(msg)
        print('Se ha producido un error')
    finally:
        lf.to_file()
        print('Se ha escrito el fichero log.txt con las incidencias')
