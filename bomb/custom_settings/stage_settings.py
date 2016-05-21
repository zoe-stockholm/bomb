AWS = True
from bomb.custom_settings.application_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bomb',
        'USER': '',
        'PASSWORD': '',
        # 'HOST': 'britnystage.c3wi05pwmygc.eu-west-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

DOMAIN = 'gazenet.britnydev.se'

ENVIRONMENT = 'stage'