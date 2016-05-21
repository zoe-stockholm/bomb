from django.conf.urls import url

import game_app
from game_app.views import GamesSearchView, GamesFilterView

app_name = 'game_app'
urlpatterns = [
    url(r'^$', GamesSearchView.as_view(), name='game-search'),
    url(r'^filter/$', GamesFilterView.as_view(), name='game-filter'),
]