from django.conf.urls import url
from game_app.views import GamesFetchView, home, game_search, admin_fetch, \
    fetch_done

app_name = 'game_app'
urlpatterns = [
    url(r'^$', home, {'template_name': 'game_app/home.html'}, name='home'),
    url(r'^fetch/$', GamesFetchView.as_view(), name='game-fetch'),
    url(r'^fetch_done/$', fetch_done, name='fetch-done'),
    url(r'^search/$', game_search, name='game-search'),
    url(r'^admin_fetch/$', admin_fetch, name='admin-fetch'),
]