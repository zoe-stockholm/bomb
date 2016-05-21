import datetime
from django.shortcuts import render_to_response
from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse
from game_app.forms import GamesSearchForm, GameFilterForm
from game_app.models import Game
from game_app.tasks import fetch_games_by_keywords


class GamesSearchView(FormView):
    template_name = 'game_app/game_search.html'
    form_class = GamesSearchForm

    def get_success_url(self):
        return reverse('game_app:game-filter')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            resource_type = form.cleaned_data.get('resource_type')
            fetch_games_by_keywords(keyword, resource_type)
            return self.form_valid(form)
        return self.form_invalid(form)


class GamesFilterView(FormView):
    template_name = 'game_app/game_filter.html'
    form_class = GameFilterForm

    def form_valid(self, form):
        release_year_from = form.cleaned_data.get('release_year_from')
        release_year_to = form.cleaned_data.get('release_year_to')

        # convert year from string to date
        date_from = datetime.datetime.strptime(
            release_year_from, '%Y').date() if release_year_from else None
        date_to = datetime.datetime.strptime(
            release_year_to, '%Y').date() if release_year_to else None

        if date_from and date_to:
            games = Game.objects.filter(
                original_release_date__range=(date_from, date_to))
        elif date_from:
            games = Game.objects.filter(
                original_release_date__gte=date_from)
        elif date_to:
            games = Game.objects.filter(
                original_release_date__lte=date_to)
        else:
            games = Game.objects.all()

        return render_to_response('game_app/game_list.html', {'games': games})

