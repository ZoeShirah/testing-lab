import unittest

import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Setup function that creates testing client."""
        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Makes sure the homepage loads correctly."""
        result = self.client.get("/")
        self.assertIn("I'm having a party", result.data)

    def test_no_rsvp_yet(self):
        """Makes sure RSVP details are there if you have not RSVP-ed"""
        result = self.client.get('/')
        self.assertIn('<h2>Please RSVP</h2>', result.data)
        self.assertNotIn('<h2>Party Details</h2>', result.data)

    def test_rsvp(self):
        """Makes sure the party details are there if you have already RSVP-ed"""
        result = self.client.post("/rsvp",
                                  data={'name': "Jane", 'email': "jane@jane.com"},
                                  follow_redirects=True)
        self.assertNotIn('<h2>Please RSVP</h2>', result.data)
        self.assertIn('<h2>Party Details</h2>', result.data)

    def test_rsvp_mel_correct(self):
        """Makes sure Mel can't RSVP with his correct info."""
        result = self.client.post("/rsvp",
                                  data={'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Sorry, Mel. This is kind of awkward.", result.data)

    def test_rsvp_mel_only_email(self):
        """Makes sure Mel can't RSVP with only his email."""
        result = self.client.post("/rsvp",
                                  data={'name': "Mel", 'email': "mel@ubermelon.com"},
                                  follow_redirects=True)
        self.assertIn("Sorry, Mel. This is kind of awkward.", result.data)

    def test_rsvp_mel_only_name(self):
        """Makes sure Mel can't RSVP with only his name."""
        result = self.client.post("/rsvp",
                                  data={'name': "Mel Melitpolski", 'email': "not_mel@ubermelon.com"},
                                  follow_redirects=True)
        self.assertIn("Sorry, Mel. This is kind of awkward.", result.data)


if __name__ == "__main__":
    unittest.main()
