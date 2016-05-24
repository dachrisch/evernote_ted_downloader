# -*- coding: utf-8 -*-

import unittest
import logging

import sys, os
sys.path.insert(0,os.path.abspath(__file__+"/../.."))
from download.ted_downloader import TedDownloader
from parse.metalink_parser import MetalinkParser
from parse.evernote_ted_parser import EvernoteTedParser, TedNote


class EvernoteTest(unittest.TestCase):

	def __get_ted_node(self, title):
		return TedNote(type('',(object,),{"title": title})())


	def test_collect_all_ted_notes_in_notebook(self):
		ted_note = EvernoteTedParser('S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de', 'daehn').get_ted_notes()[0]

		self.assertEqual('How Airbnb designs for trust', ted_note.title)
		self.assertEqual('Joe Gebbia', ted_note.speaker)

	def test_find_link_in_metalink(self):
		metalink = MetalinkParser('tests/metalink.xml').get_metalink( self.__get_ted_node('TEDTalks (hd) - How Airbnb designs for trust | Joe Gebbia'))
		self.assertEqual('2016/Joe Gebbia - How Airbnb designs for trust.mp4', metalink.title)
		self.assertEqual('http://download.ted.com/talks/JoeGebbia_2016-480p-en.mp4', metalink.url)

	def test_grab_note_and_find_in_metalink(self):
		evernote_parser = EvernoteTedParser('S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de', 
											'daehn')

		metalink_parser = MetalinkParser('tests/metalink.xml')

		for ted_note in evernote_parser.get_ted_notes():
			self.assertEqual('http://download.ted.com/talks/JoeGebbia_2016-480p-en.mp4', metalink_parser.get_metalink(ted_note).url)
	def test_download_all_ted_notes_from_metalink(self):
		




		evernote_parser = EvernoteTedParser('S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de', 
											'daehn')

		ted_downloader = TedDownloader('http://metated.petarmaric.com/metalinks/TED-talks-in-high-quality.en.metalink', 'tests')

		for ted_note in evernote_parser.get_ted_notes():
			file = ted_downloader.download(ted_note)
			self.assertTrue(os.path.exists(file))





if __name__ == '__main__':
	import logging
	logging.basicConfig(filename = 'test_debug.log', level=logging.DEBUG)

	unittest.main()
