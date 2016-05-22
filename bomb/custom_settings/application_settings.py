from bomb.settings import *

gettext = lambda s: s
_ = lambda s: s


PAGINATOR_PER_PAGE = 10

######################### GIANTBOMB SETTINGS ################################

GIANTBOMB_PUBLIC_API_BASE_URL = 'http://www.giantbomb.com/api/'
GIANTBOMB_PUBLIC_API_KEY = 'ef179cfeb70de3ceeb5b378c127e79b89dee49be'
FORMAT = 'json'

######################### DJANGO CRISPY SETTINGS ##############################

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_CLASS_CONVERTERS = {'textinput': ''}