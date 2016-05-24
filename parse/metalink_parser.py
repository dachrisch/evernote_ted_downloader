# -*- coding: utf-8 -*-

import logging
import xmltodict

class Metalink(object):
	def __init__(self, node):
		self.title = node['@name']
		self.url = node['resources']['url']['#text']

class MetalinkParser(object):
	def __init__(self, file):
		self.log = logging.getLogger(self.__class__.__name__)
		with open(file) as fd:
			self.doc = xmltodict.parse(fd.read())

	def get_metalink(self, ted_note):
		file_or_files = self.doc['metalink']['files']['file'] 
		files = file_or_files if type(file_or_files) == list else (file_or_files, )
		self.log.debug("searching for [%s] in [%d] metalinks" % (ted_note.speaker, len(files)))
		for file in files:
			if ted_note.speaker in file['@name']:
				if ted_note.title in file['@name']:
					return Metalink(file)
