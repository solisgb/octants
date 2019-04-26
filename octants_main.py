# -*- coding: utf-8 -*-
"""
driver to call function octants in octants.py
"""

dir_data = r'C:\Users\solis\Documents\DEV\python3\GIS\mtn50sinCanarias'
fshp = 'mdt50sinCanarias.shp'

if __name__ == "__main__":

    try:
        from datetime import timedelta
        from time import time
        from octants import octants

        startTime = time()

        octants(dir_data, fshp)

        xtime = time() - startTime
    except Exception as error:
        import traceback
        msg = traceback.format_exc()
        print(msg)
    finally:
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
