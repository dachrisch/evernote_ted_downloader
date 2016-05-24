# -*- coding: utf-8 -*-

import os
import time
import logging
from progress import Progress
from urllib import urlretrieve

class _DownloadProgressHook:
	def __init__(self, name, interval=1, *args, **kwargs):
		self.log = logging.getLogger('DownloadProgressHook')
		self.actual = 0
		self.interval = interval
		
	def report_hook(self, block_number, block_size, total_size):

			if block_number:
				self._eat(block_size)
			else:
				self._start_reporting(total_size)
				
			if time.time() - self.last_report > self.interval:
				self._log_report()
				self.last_report = time.time()
				
	def _eat(self, count):
		self.log.debug('eating %d bytes [%d/%d]' % (count, self.actual, self.total))
		self.actual += count
		self.eta_calculator.update(self.actual)

	def _start_reporting(self, total):
		self.total = total
		self.eta_calculator = Progress(self.total, unit = 'kb')
		self.last_report = time.time()

	def _log_report(self):
		self.log.info('%02.1f%% [%.0f/%.0f kb]. eta %ds (%dkb/s)' % (self.eta_calculator.percentage(), 
										self.actual / 1024, self.total / 1024, 
										self.eta_calculator.time_remaining(),
										self.eta_calculator.predicted_rate() / 1024))

class DownloadManager(object):
	def __init__(self, url_retriever = urlretrieve):
		self.log = logging.getLogger('DownloadManager')
		self.url_retriever = url_retriever

	def __remove_file_if_exists(self, filename, exception):
		if(os.path.exists(filename)):
			self.log.warn('removing file [%s] after exception: %s' % (filename, str(exception)))
			os.unlink(filename)

	def __copy_stream_to_target(self, url, target_filename):
		if(os.path.exists(target_filename)):
			self.log.warn('skipping already existing file [%s]' % target_filename)
			return

		self.log.debug('downloading [%s] to [%s].', url, target_filename)
		
		download_reporter = _DownloadProgressHook(target_filename)
		
		try:
			self.url_retriever(url, target_filename, download_reporter.report_hook)
		except Exception as e:
			self.__remove_file_if_exists(target_filename, e)
			raise
		except KeyboardInterrupt:
			self.__remove_file_if_exists(target_filename, 'User interrupted')
			raise Exception('User interrupted')	
	def download(self, source_url, target_filename):
		self.__copy_stream_to_target(source_url, target_filename)
		return target_filename