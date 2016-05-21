import json

import requests
from django.conf import settings
from django.utils.log import logging

from game_app.models import Game

logger = logging.getLogger(__name__)


def fetch_games_by_keywords(keyword, resource_type):
    response = requests.get(
        '{}search/?api_key={}&format={}&query={}&resources={}'.format(
            settings.GIANTBOMB_PUBLIC_API_BASE_URL,
            settings.GIANTBOMB_PUBLIC_API_KEY,
            settings.FORMAT,
            keyword,
            resource_type))

    if json.loads(response.text).get('status_code') != 1:
        logger.error(json.loads(response.text).get('error'))
    else:
        for g in json.loads(response.text).get('results'):
            game, created = Game.objects.get_or_create(
                game_id=str(g.get('id')))
            game.update_game(g)
