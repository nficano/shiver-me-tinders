# -*- coding: utf-8 -*-
import logging
import yaml
from collections import namedtuple

import requests

log = logging.getLogger(__name__)

APP_VERSION = 371
OS_VERSION = 9000000002
PLATFORM = 'ios'
USER_AGENT = 'Tinder/4.6.1 (iPhone; 9.0.2; Scale/2.00)'


class Tinder(object):
    base_url = "https://api.gotinder.com"

    def __init__(self, fb_token, fb_id, lat, lon):
        """Initialize Tinder object.

        :param str fb_token:
            Your Facebook token.
        :param str fb_id:
            Your Facebook ID.
        :param long lat:
            Your latitude.
        :param long lat:
            Your longitude.
        """
        self.fb_token = fb_token
        self.fb_id = fb_id
        self.location = {'lat': lat, 'lon': lon}
        self.auth()
        self.ping()

    @classmethod
    def config_from_file(cls, path_to_yaml):
        """Initialize Tinder object via yaml file.

        :param str path_to_yaml:
            Absolute path to config.yaml.
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
        headers = self._get_auth_header()
        resp = requests.post(self.base_url + endpoint, headers=headers,
                             json=self.location)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()

    def get_matches(self):
        """Returns a list of Tinder matches as User objects.
        """
        User = namedtuple('User', [
            'id', 'name', 'bio', 'birth_date', 'photos'])
        endpoint = "/user/recs?locale=en-US"
        headers = self._get_auth_header()
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        for r in resp.json().get('results', []):
            photos = [p.get('url') for p in r.get('photos')]
            yield User(id=r.get('_id'), name=r.get('name'), bio=r.get('bio'),
                       birth_date=r.get('birth_date'), photos=photos)

    def iter_matches(self):
        """Wraps the `get_matches()` method to serve matches infinately.
        """
        while True:
            matches = self.get_matches()
            for match in matches:
                yield match

    def like(self, user):
        """Like a user.

        :param object user:
            An instance of a user object.
        """
        if 'tinder_rate_limited_id_' in user.id:
            raise Exception(user.bio)

        log.debug('tips hat at %s', user.name)
        endpoint = "/like/%s" % user.id
        headers = self._get_auth_header()
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()

    def dislike(self, user):
        """Pass on a user.

        :param object user:
            An instance of a user object.
        """
        if 'tinder_rate_limited_id_' in user.id:
            raise Exception(user.bio)
        endpoint = "/pass/%s" % user.id
        headers = self._get_auth_header()
        resp = requests.get(self.base_url + endpoint, headers=headers)
        if not resp.ok:
            raise Exception(resp.text)
        return resp.json()

    def _get_auth_header(self):
        return {
            'Authorization': 'Token token="%s"' % self.token,
            'User-Agent': USER_AGENT,
            'X-Auth-Token': self.token,
            'app-version': APP_VERSION,
            'os_version': OS_VERSION,
            'platform': PLATFORM,
        }
