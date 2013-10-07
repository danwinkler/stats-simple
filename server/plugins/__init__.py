import os
import ss_plugin

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module == 'ss_plugin.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module