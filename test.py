from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "A", "T", "T", "T"], 
                                 ["B", "A", "T", "T", "T"], 
                                 ["B", "A", "T", "T", "T"], 
                                 ["B", "A", "T", "T", "T"], 
                                 ["B", "A", "T", "T", "T"]]
        response = self.client.get('/check?word=bat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check?word=boggle')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        self.client.get('/')
        response = self.client.get(
            '/check?word=thisisnotaword')
        self.assertEqual(response.json['result'], 'not-word')