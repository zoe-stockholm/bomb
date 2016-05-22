AWS = True
from bomb.custom_settings.application_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bomb',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'ec2-52-51-156-213.eu-west-1.compute.amazonaws.com',
        'PORT': '5432'
    }
}
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

ENVIRONMENT = 'stage'