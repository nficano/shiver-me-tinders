# -*- coding: utf-8 -*-
import logging
import yaml
from collections import namedtuple

import requests

log = logging.getLogger(__name__)


class Tinder(object):
    base_url = "https://api.gotinder.com"

    def __init__(self, fb_token, fb_id, lat, lon):
        """Initialize Tinder object.

        :param str fb_token: Your Facebook Token
        :param str fb_id: Your Facebook ID
        :param long lat: Your latitude.
        :param long lat: Your longitude.
        """
        self.fb_token = fb_token
        self.fb_id = fb_id
        self.location = {'lat': lat, 'lon': lon}
        self.auth()
        self.ping()

    @classmethod
    def config_from_file(cls, path_to_yaml):
        """Initialize Tinder object via yaml file.

        :param str path_to_yaml: Absolute path to config.yaml.
        """
        with open(path_to_yaml, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        fb_token = cfg.get('facebook', {}).get('token')
        fb_id = cfg.get('facebook', {}).get('id')
        lat = cfg.get('location', {}).get('lat')
        lon = cfg.get('location', {}).get('lon')
        return cls(fb_token, fb_id, lat, lon)

    def auth(self):
        """Get the auth token for signing tinder requests.
        """
        endpoint = "/auth"
        payload = {
            "locale": "en",
            "facebook_token": self.fb_token,
            "facebook_id": self.fb_id
        }
        resp = requests.post(self.base_url + endpoint, json=payload)
        if resp.ok:
            self.profile = resp.json()
            self.token = resp.json().get('token', {})
        if not resp.ok:
            raise Exception(resp.text)
        return self.token

    def ping(self):
        """Tell the server your location.
        """
        endpoint = "/user/ping"
        headers = {
            'Token': 'token="%s"' % self.token,
            'X-Auth-Token': self.token
        }
        resp = requests.post(self.base_url + endpoint, headers=headers,
                             json=self.location)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()

    def get_matches(self):
        """Returns a list of Tinder matches as User objects.
        """
        User = namedtuple('User', ['id', 'name', 'bio', 'photos'])
        endpoint = "/user/recs"
        headers = {
            'Token': 'token="%s"' % self.token,
            'X-Auth-Token': self.token
        }
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        for r in resp.json().get('results', []):
            photos = [p.get('url') for p in r.get('photos')]
            yield User(id=r.get('_id'), name=r.get('name'), bio=r.get('bio'),
                       photos=photos)

    def iter_matches(self):
        """Wraps the `get_matches()` method to serve matches infinately.
        """
        while True:
            matches = self.get_matches()
            for match in matches:
                yield match

    def like(self, user):
        """Like a user.

        :param object user: An instance of a user object.
        """
        if 'tinder_rate_limited_id_' in user.id:
            raise Exception(user.bio)

        log.debug('tips hat at %s', user.name)
        endpoint = "/like/%s" % user.id
        headers = {
            'Token': 'token="%s"' % self.token,
            'X-Auth-Token': self.token
        }
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()

    def dislike(self, user):
        """Pass on a user.

        :param object user: An instance of a user object.
        """
        if 'tinder_rate_limited_id_' in user.id:
            raise Exception(user.bio)
        endpoint = "/pass/%s" % user.id
        headers = {
            'Token': 'token="%s"' % self.token,
            'X-Auth-Token': self.token
        }
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()


if __name__ == '__main__':
    tinder = Tinder.config_from_file('config.yaml')
    for match in tinder.iter_matches():
        tinder.like(match)
