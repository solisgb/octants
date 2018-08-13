# -*- coding: utf-8 -*-
"""
driver to call function octants in octants.py
"""

if __name__ == "__main__":

    try:
        from datetime import timedelta
        import logging
        from time import time
        import traceback
        import log_file as lf
        from octants import octants

        startTime = time()

        octants()

        xtime = time() - startTime
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
    except Exception as error:
        logging.error(traceback.format_exc())
        msg = '\n{}'.format(traceback.format_exc())
        lf.write(error.__doc__)
        lf.write(msg)
    finally:
        lf.to_file()
        print('Se ha escrito el fichero log.txt con las incidencias')
