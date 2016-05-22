import datetime
from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout, Field, Div
from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class GamesFetchForm(forms.Form):
    keyword = forms.CharField(
        label=_('Keyword'), required=True, initial='Quiz')
    resource_type = forms.CharField(
        label=_('Type'), required=False, initial='game')

    def __init__(self, *args, **kwargs):
        super(GamesFetchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('keyword',
                  type='text',
                  placeholder=_('Keyword'),
                  name='keyword',
                  ),
            Field('resource_type',
                  type='text',
                  placeholder=_('Resource Type'),
                  name='resource_type',
                  ),
            Div(
                    StrictButton(_('Fetch'), type='submit', id='fetch'),
                )
            )

        self.helper.form_id = 'id-GamesFetchForm'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = reverse('game_app:game-fetch')


class GameSearchForm(forms.Form):
    release_year_from = forms.IntegerField(
        label=_('Release Year From'),
        required=False,
        initial=1900,
        max_value=9999,
        min_value=1800)
    release_year_to = forms.IntegerField(
        label=_('Release Year To'),
        required=False,
        initial=1999,
        max_value=9999,
        min_value=1800)
    resource_type = forms.CharField(
        label=_('Type'), required=False, initial='game')

    def filter_queryset(self, request, queryset):
        release_year_from = self.cleaned_data.get('release_year_from')
        release_year_to = self.cleaned_data.get('release_year_to')
        resource_type = self.cleaned_data.get('resource_type')

        queryset = queryset.filter(resource_type=resource_type)

        # convert year from string to date
        date_from = datetime.datetime.strptime(
            str(release_year_from),
            '%Y').date() if release_year_from else None

        date_to = datetime.datetime.strptime(
            str(release_year_to),
            '%Y').date() if release_year_to else None

        if date_from and date_to:
            games_list = queryset.filter(
                original_release_date__range=(date_from, date_to))
        elif date_from:
            games_list = queryset.filter(
                original_release_date__gte=date_from)
        elif date_to:
            games_list = queryset.filter(
                original_release_date__lte=date_to)
        else:
            games_list = queryset

        return games_list


class AdminFetchForm(forms.Form):
    keyword = forms.CharField(label=_('Keyword'), required=True)
    resource_type = forms.CharField(
        label=_('Type'), required=False, initial='game')