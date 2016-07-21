from distutils.core import setup
import py2exe
import sys
import matplotlib

sys.setrecursionlimit(5000)

datafiles = [("yarn_files", ['yarn_search.csv'])]
datafiles.extend(matplotlib.get_py2exe_datafiles()) 

setup(console=['yarnatron.py'],
      data_files=datafiles,
      options={'py2exe': {'excludes': ['_gtkagg', '_tkagg', 'scipy',
                                       'sqlalchemy', 'statsmodels']}})