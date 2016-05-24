# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import re

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
		return [TedNote(note) for note in note_store.findNotesMetadata(self.access_token, noteFilter, 0, 1, spec).notes]

class TedNote(object):
	def __init__(self, note_metadata):
		match = re.search('TEDTalks \(hd\) - ([^\|]+) \| ([^<]+)', note_metadata.title)
		self.title = match.group(1)
		self.speaker = match.group(2)