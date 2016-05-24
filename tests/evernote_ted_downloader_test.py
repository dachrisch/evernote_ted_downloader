# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient
import unittest

class EvernoteTest(unittest.TestCase):
	def test_developer_login(self):

		access_token = 'S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de'
		client = EvernoteClient(token=access_token)
		userStore = client.get_user_store()
		user = userStore.getUser()
		self.assertEqual('daehn', user.username)

	def test_access_single_ted_note(self):

		access_token = 'S=s1:U=9288d:E=15c3a9bc252:C=154e2ea94e8:P=1cd:A=en-devtoken:V=2:H=c0cba7347df5a0c22cce3fd7d33771de'
		client = EvernoteClient(token=access_token)

		note_store = client.get_note_store()
		notebooks = note_store.listNotebooks()

		self.assertIn('First Notebook', [notebook.name for notebook in notebooks])


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename = 'test_debug.log', level=logging.DEBUG)

    unittest.main()
