# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import unittest
import re
from urlparse import urlparse
import xmltodict

class EvernoteTedParser(object):
	def __init__(self, access_token, username):
		self.access_token = access_token
		self.username = username
	def get_ted_notes(self):
		client = EvernoteClient(token = self.access_token)
		userStore = client.get_user_store()
		user = userStore.getUser()
		assert self.username == user.username

		noteFilter = NoteStore.NoteFilter()
		noteFilter.ascending = False
		noteFilter.words = "TED"
		spec = NoteStore.NotesMetadataResultSpec()
		spec.includeTitle = True

		note_store = client.get_note_store()
		return note_store.findNotesMetadata(self.access_token, noteFilter, 0, 1, spec).notes

class TedNote(object):
	def __init__(self, note_metadata):
		match = re.search('TEDTalks \(hd\) - ([^\|]+) \| ([^<]+)', note_metadata.title)
		self.title = match.group(1)
		self.speaker = match.group(2)

class Metalink(object):
	def __init__(self, node):
		self.title = node['@name']
		self.url = node['resources']['url']['#text']

class MetalinkParser(object):
	def __init__(self, file):
		with open(file) as fd:
			self.doc = xmltodict.parse(fd.read())

	def get_metalink(self, ted_note):
		file_or_files = self.doc['metalink']['files']['file'] 
		files = file_or_files if type(file_or_files) == list else (file_or_files, )
		for file in files:
			print "searching for %s in [%s]: %s" % (ted_note.speaker, file, file['@name'])
			if ted_note.speaker in file['@name']:
				if ted_note.title in file['@name']:
					return Metalink(file)


class EvernoteTest(unittest.TestCase):

	def __get_ted_node(self, title):
		return TedNote(type('',(object,),{"title": title})())


	def test_collect_all_ted_notes_in_notebook(self):
		note_metadata = EvernoteTedParser('S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de', 'daehn').get_ted_notes()[0]

		self.assertIn('TEDTalks (hd) - How Airbnb designs for trust | Joe Gebbia', note_metadata.title)

	def test_grab_speaker_and_title_from_note(self):
		ted_note = self.__get_ted_node('TEDTalks (hd) - How Airbnb designs for trust | Joe Gebbia')

		self.assertEqual('How Airbnb designs for trust', ted_note.title)
		self.assertEqual('Joe Gebbia', ted_note.speaker)

	def test_find_link_in_metalink(self):
		metalink = MetalinkParser('tests/metalink.xml').get_metalink( self.__get_ted_node('TEDTalks (hd) - How Airbnb designs for trust | Joe Gebbia'))
		self.assertEqual('2016/Joe Gebbia - How Airbnb designs for trust.mp4', metalink.title)
		self.assertEqual('http://download.ted.com/talks/JoeGebbia_2016-480p-en.mp4', metalink.url)

	def xtest_grab_note_and_find_in_metalink(self):
		note_metadatas = self._get_ted_notes('S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de', 
											'daehn')
		self.assertEqual('http://download.ted.com/talks/JoeGebbia_2016-480p-en.mp4', self._get_download_link(note_metadatas[0]))




if __name__ == '__main__':
    import logging
    logging.basicConfig(filename = 'test_debug.log', level=logging.DEBUG)

    unittest.main()
