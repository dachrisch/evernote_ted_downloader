# -*- coding: utf-8 -*-

import os
from download.downloader import DownloadManager
from parse.metalink_parser import MetalinkParser

class TedDownloader(object):
	def __init__(self, metalink_url, basedir):
		self.metalink_url = metalink_url
		self.basedir = basedir
		self.__need_setup = True
		self._download_manager = DownloadManager()
	def download(self, ted_note):
		self.__setup()
		ted_metalink = self.metalink_parser.get_metalink(ted_note)
		return self._download_manager.download(ted_metalink.url, os.path.join(self.basedir, ted_metalink.title))
	def __setup(self):
		if self.__need_setup:
			metalink_file = self._download_manager.download(self.metalink_url, os.path.join(self.basedir, 'ted_talks.metalink'))
			self.metalink_parser = MetalinkParser(metalink_file)
			self.__need_setup = False
