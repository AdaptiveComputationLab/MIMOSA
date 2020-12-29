import logging

from detection_engine.utils import import_plugins

logging.basicConfig()

class Detection(object):
    def __init__(self):
        pass

    def detect(self):
        pass

plugins = import_plugins(__file__, "detection_engine.heuristic", globals(), Detection)
names = dict((plugin.name, plugin) for plugin in plugins)
