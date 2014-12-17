__author__ = 'bromix'

import unittest
from resources.lib import rtlinteractive


class TestClient(unittest.TestCase):
    def test_get_films(self):
        client = rtlinteractive.Client(rtlinteractive.Client.CONFIG_RTL_NOW)
        json_data = client.get_films(format_id=1061, page=1)
        self.assertTrue(json_data['success'])
        pass

    def test_get_formats(self):
        client = rtlinteractive.Client(rtlinteractive.Client.CONFIG_RTL_NOW)
        json_data = client.get_formats()
        self.assertTrue(json_data['success'])
        pass

    def test_tips(self):
        client = rtlinteractive.Client(rtlinteractive.Client.CONFIG_RTL_NOW)
        json_data = client.get_tips()
        self.assertTrue(json_data['success'])

    def test_top_10(self):
        client = rtlinteractive.Client(rtlinteractive.Client.CONFIG_RTL_NOW)
        json_data = client.get_top_10()
        self.assertTrue(json_data['success'])

    def test_search(self):
        client = rtlinteractive.Client(rtlinteractive.Client.CONFIG_RTL_NOW)
        json_data = client.search('bauer')
        self.assertTrue(json_data['success'])
        pass

    pass