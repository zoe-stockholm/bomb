import json

import requests
from django.conf import settings
from django.utils.log import logging

from game_app.models import Game

logger = logging.getLogger(__name__)


def fetch_games_by_keywords(keyword, resource_type):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url='{}search/'.format(settings.GIANTBOMB_PUBLIC_API_BASE_URL),
                            params={'api_key': settings.GIANTBOMB_PUBLIC_API_KEY,
                                    'format': settings.FORMAT,
                                    'query': keyword,
                                    'resources': resource_type},
                            headers=headers)

    if json.loads(response.text).get('status_code') != 1:
        logger.error(json.loads(response.text).get('error'))
    else:
        for g in json.loads(response.text).get('results'):
            game, created = Game.objects.get_or_create(
                game_id=str(g.get('id')))
            game.update_game(g)
