import urllib2
import unittest

from flask.ext.testing import LiveServerTestCase

from prototapes import init_app


class ApiTests(LiveServerTestCase):
    def create_app(self):
        app = init_app()
        app.config['TESTING'] = True
        return app

    def test_server_is_up(self):
        print self.get_server_url()
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_user_get(self):
        pass

if __name__ == '__main__':
    unittest.main()