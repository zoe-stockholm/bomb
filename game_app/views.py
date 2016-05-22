from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.views import deprecate_current_app
from django.shortcuts import render_to_response, render
from django.template.response import TemplateResponse
from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.edit import FormMixin
from game_app.forms import GamesFetchForm, GameSearchForm, AdminFetchForm
from game_app.models import Game
from game_app.tasks import fetch_games_by_keywords
from django.contrib import admin
from django.contrib import messages


class GamesFetchView(FormView):
    template_name = 'game_app/game_fetch.html'
    form_class = GamesFetchForm

    def get_success_url(self):
        return reverse('game_app:home')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            resource_type = form.cleaned_data.get('resource_type')
            fetch_games_by_keywords(keyword, resource_type)
            messages.success(request, 'FETCH DONE!')
            return self.form_valid(form)
        return self.form_invalid(form)


class FilteredGameView(FormMixin, ListView):

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            self.object_list = form.filter_queryset(request, self.object_list)

        context = self.get_context_data(
            form=form, object_list=self.object_list)
        return self.render_to_response(context)

game_search = FilteredGameView.as_view(
    form_class=GameSearchForm,
    template_name='game_app/game_search.html',
    queryset=Game.objects.all(),
    paginate_by=settings.PAGINATOR_PER_PAGE
)


@deprecate_current_app
def home(
        request,
        template_name='game_app/home.html',
        extra_context=None):
    context = {
        'title': _('Home'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@admin.site.register_view('game_app/tasks/')
def tasks(request):
    return render_to_response(
         "game_app/admin/task.html", RequestContext(request, {}), )


def admin_fetch(request):
    if request.method == 'POST':
        form = AdminFetchForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('keyword')
            resource_type = request.POST.get('resource_type')

            fetch_games_by_keywords(keyword, resource_type)
            messages.success(request, 'FETCH DONE!')

            return HttpResponseRedirect('/admin/')
    else:
        form = GamesFetchForm()

    return render(request, 'game_app/admin/task.html', {'form': form})
