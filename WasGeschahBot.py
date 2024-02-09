#!/usr/bin/env python3
import logging
import sys
from subprocess import Popen, PIPE

from credentials import username, password
from mastodon import Mastodon, MastodonIllegalArgumentError
from datetime import date

API_BASE_URL = 'https://botsin.space'
CLIENT_SECRET_FILE = 'pytooter_clientcred_wasgeschah.secret'


def register():
    Mastodon.create_app(
        'pytooterapp_wasgeschah',
        api_base_url=API_BASE_URL,
        to_file=CLIENT_SECRET_FILE)


def login():
    mastodon = Mastodon(client_id=CLIENT_SECRET_FILE, api_base_url=API_BASE_URL)
    version = mastodon.retrieve_mastodon_version()
    logging.debug(f"Mastodon version {version}")
    return mastodon.log_in(username, password)  # , to_file=userCredentialsFile)


def get_instance(token):
    return Mastodon(client_id=CLIENT_SECRET_FILE, api_base_url=API_BASE_URL, access_token=token)


def toot_daily(token):
    mastodon = get_instance(token)
    today = date.today()
    mastodon.toot(f"""Was geschah heute #vor100Jahren?
https://chroniknet.de/extra/was-war-am/?ereignisdatum={today.day}.{today.month}.{today.year - 100}""")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # register(); sys.exit()  # this only needs to be done once
    try:
        access_token = login()
        logging.debug(f"access_token: {access_token}")
        toot_daily(access_token)
        get_instance(access_token).revoke_access_token()
    except MastodonIllegalArgumentError as e:
        Popen(["mail", "-s", "Failed to login", username], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(str(e.args).encode())
