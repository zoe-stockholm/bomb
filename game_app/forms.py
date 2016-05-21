from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout, Field, Div
from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms import extras
from datetime import datetime


class GamesSearchForm(forms.Form):
    keyword = forms.CharField(label=_('Keyword'), required=True)
    resource_type = forms.CharField(label=_('Type'), required=False)

    def __init__(self, *args, **kwargs):
        super(GamesSearchForm, self).__init__(*args, **kwargs)

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
                    StrictButton(_('Ok'), type='submit', id='fetch'),
                )
            )

        self.helper.form_id = 'id-GamesSearchForm'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = reverse('game_app:game-search')


class GameFilterForm(forms.Form):
    release_year_from = forms.CharField(
        label=_('Release Year From'), required=False)
    release_year_to = forms.CharField(
        label=_('Release Year To'), required=False)

    def __init__(self, *args, **kwargs):
        super(GameFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('release_year_from',
                  type='text',
                  placeholder=_('Release Year From'),
                  name='release_year_from',
                  ),
            Field('release_year_to',
                  type='text',
                  placeholder=_('Release Year To'),
                  name='release_year_to',
                  ),
            Div(
                    StrictButton(_('See Result'), type='submit'),
                )
            )

        self.helper.form_id = 'id-GameFilterForm'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = reverse('game_app:game-filter')