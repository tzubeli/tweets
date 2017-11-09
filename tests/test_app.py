import pytest
import os
import json
import app
from unittest.mock import ANY


class TestApp:

    with open(os.path.dirname(__file__) + '/../config.json') as config_file:
        config = json.load(config_file)

    @pytest.mark.parametrize(
        'consumer_key, consumer_secret', (("invalid_key", "invalid_secret"),
                                          ("h3YceHkPLjvyE2Y2mQqfZSA5x", "92839285345"),)
    )
    def test_authenticate_fail(self, consumer_key, consumer_secret):
        authentication = app.authenticate(consumer_key, consumer_secret)
        assert "access_token" not in authentication

    @pytest.mark.parametrize(
        'consumer_key, consumer_token', ((config['consumer_key'], config['consumer_secret']),)
    )
    def test_authenticate_pass(self, consumer_key, consumer_token):
        authentication = app.authenticate(consumer_key, consumer_token)
        assert 'access_token' in authentication

    def test_get_tweets_renders_html(self, mocker):
        render = mocker.patch.object(app, 'render_template')
        app.get_tweets(1)
        render.assert_called_with('tweets.html', tweets=ANY, page=1, total=5)


