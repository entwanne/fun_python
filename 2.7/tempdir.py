#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class TempDir(object):
    "Crée un répertoire temporaire sur le système de fichier (usuellement dans /tmp/)"
    def __init__(self):
        from tempfile import mkdtemp
        self.__name = mkdtemp()
    def __del__(self):
        from shutil import rmtree
        rmtree(self.name)
    @property
    def name(self):
        return self.__name
