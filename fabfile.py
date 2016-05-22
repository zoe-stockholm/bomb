from __future__ import with_statement
from fabric.api import *
from fabric.contrib import *
from fabric.contrib.console import confirm
import datetime
import time
from contextlib import contextmanager
import ast
import os

PROJECT_NAME = 'bomb'
PROJECT_PATH = '/media/files/projects/'
VERSION = ''


def stage():
    """Sets the deploy environment.
    """
    env.hosts = ['ec2-52-51-156-213.eu-west-1.compute.amazonaws.com']
    env.user = 'ubuntu'
    env.key_filename = '~/Dev/aws/pem/craft.pem'
    env.PROJECT_NAME = PROJECT_NAME
    env.environment = 'stage'


def initial_setup():
    """Initial setup of the server
    """

    sudo('apt-get -y update')

    confirm('Is this a new server?')

    reqs = [
        'nginx',
        'python',
        'python3.4',
        'python3-pip',
        'python-dev',
        'python-virtualenv',
        'virtualenvwrapper',
        'libpq-dev',
        'libxml2-dev',
        'libxslt1-dev',
        'libjpeg-dev',
        'libfreetype6-dev',
        'libffi-dev',
        'swig',
        'git',
        'nodejs-legacy',
        'npm',
        'sendmail',
        'libgeos-dev',
        'libxml2-dev',
        'libxslt1-dev',
    ]

    #install all requirements
    sudo('apt-get -y install '+' '.join(reqs))

    if files.exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')

    #create symlinks to make libjpeg be found by pillow
    sudo('ln -sfn /usr/lib/x86_64-linux-gnu/libz.so /usr/lib')
    sudo('ln -sfn /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/')
    sudo('ln -sfn /usr/lib/x86_64-linux-gnu/libfreetype6.so /usr/lib/libfreetype6.so')

    #create the vassals and log folder
    sudo('mkdir -p /etc/uwsgi/vassals')
    sudo('mkdir -p /var/log/uwsgi')
    sudo('mkdir -p /var/www')
    sudo('mkdir -p /var/run/uwsgi')

    sudo('chown www-data. /var/run/uwsgi')
    sudo('chown www-data. /var/log/uwsgi')
    sudo('chown www-data. /var/www')

    #install uwsgi system wide
    sudo('pip3 install uwsgi')
    sudo('npm install -g bower')
    # run('npm install grunt')
    sudo('npm install -g grunt-cli')

    #restart services
    sudo('service nginx restart')


def _fastrouter_setup(current_path):
    """Symlink fastrouter ini to vassals"""
    sudo(
        'ln -sfn {}/conf/fastrouter.ini {}'.format(
            current_path, '/etc/uwsgi')
    )


def deploy(version):
    """Deploy a tag from git.
    Usage: fab prod deploy:version=1.0 to deploy version 1.0"""

    if env.PROJECT_NAME:
        PROJECT_NAME = env.PROJECT_NAME

    #VERSION = version
    cur_version_path = PROJECT_PATH+PROJECT_NAME+'/'+version


    if not files.exists(PROJECT_PATH+PROJECT_NAME+'/'+version):
        sudo('mkdir -p '+PROJECT_PATH+PROJECT_NAME+'/'+version)
        sudo('chmod +w '+PROJECT_PATH+PROJECT_NAME+'/'+version)

    sudo('chown -R ubuntu. {}'.format(PROJECT_PATH+PROJECT_NAME))
    sudo('chmod +w '+PROJECT_PATH+PROJECT_NAME)
    sudo('chown -R ubuntu. {}'.format(cur_version_path))

    repoURL = local('git config --get remote.origin.url', capture=True)

    """@TODO: change to git clone"""
    #_create_deploy_key()
    #confirm('Is the key on github?')

    #push the code
    filename = PROJECT_NAME+'_'+version+'.tar'
    local('git archive --format=tar -o {path} {version}'
            .format(path='/tmp/'+filename, version=version))
    put('/tmp/'+filename, PROJECT_PATH+PROJECT_NAME)

    run('tar -C {0}/{version} -xf {0}/{file}'.format(PROJECT_PATH+PROJECT_NAME, file=filename, version=version))

    # symlink fastrouter ini to vassals
    _fastrouter_setup(cur_version_path)

    run('mkdir -p {}'.format(cur_version_path+'/logs'))

    # install all npm modules and grunt stuff

    with cd(cur_version_path):
        # create directories and symlinks for node and bower
        run('mkdir -p {}'.format('../node_modules'))
        run('mkdir -p {}'.format('../bower_components'))
        run('ln -sfn {} {}'.format(PROJECT_PATH+PROJECT_NAME+'/node_modules', cur_version_path+'/'))
        run('ln -sfn {} {}'.format(PROJECT_PATH+PROJECT_NAME+'/bower_components', cur_version_path+'/'))

        # install all the requirements
        run('npm install')
        run('bower install')
        run('grunt --force')

    if files.exists('/tmp/{}_celery.pid'.format(PROJECT_NAME)):
        with settings(warn_only=True):
            # Need to kill uwsgi so celery don't autostart
            sudo('service uwsgi stop')
            sudo('kill $(cat /tmp/{}_celery.pid)'.format(PROJECT_NAME))
    while files.exists('/tmp/{}_celery.pid'.format(PROJECT_NAME)):
        # print('killing celery')
        time.sleep(1)

    if not files.exists('~/.venv/{}'.format(PROJECT_NAME)):
        run('virtualenv -p /usr/bin/python3.4 {}'.format('~/.venv/'+PROJECT_NAME))

    # Take the media folder out of the project, and symlink it
    if not files.exists(PROJECT_PATH+PROJECT_NAME+'/media'):
        sudo('mkdir -p {}'.format(PROJECT_PATH+PROJECT_NAME+'/media'))
        sudo('chown -R www-data. {}'.format(PROJECT_PATH+PROJECT_NAME+'/media'))

    sudo('ln -sfn {} {}'.format(PROJECT_PATH+PROJECT_NAME+'/media', cur_version_path+'/'))
    sudo('chown -R www-data. {}'.format(cur_version_path+'/media'))
    sudo('chown -R www-data. {}'.format(PROJECT_PATH + PROJECT_NAME + '/media'))

    with prefix('source {}'.format('~/.venv/'+PROJECT_NAME+'/bin/activate')):
        with cd(cur_version_path):
            run('pip install -r {}'.format(cur_version_path+'/conf/requirements.txt'))
            # collect static
            run('python manage.py collectstatic --settings={}.custom_settings.{}_settings --noinput'.format(PROJECT_NAME, env.environment))

    sudo('chown -R www-data. {}'.format(cur_version_path))

    sync_database(cur_version_path)

    #setup the symlinks
    # Symlink to /var/www
    sudo('ln -sfn {} {}'.format(cur_version_path, '/var/www/'+PROJECT_NAME))

    # Symlink nginx to sites-available
    sudo('ln -sfn {} {}'.format(
        cur_version_path+'/conf/nginx.conf',
        '/etc/nginx/sites-enabled/'+PROJECT_NAME+'.conf'))

    # Symlink uwsgi to vassals
    sudo('ln -sfn {} {}'.format(
        cur_version_path+'/conf/uwsgi_{}.ini'.format(env.environment),
        '/etc/uwsgi/vassals/'+PROJECT_NAME+'.ini'))
    sudo('ln -sfn {} {}'.format(
        cur_version_path+'/conf/*.skel', '/etc/uwsgi/vassals/'))

    if not files.exists('/etc/init/uwsgi.conf'):
        #create startup script for uwsgi
        sudo('ln -sfn {} {}'.format(cur_version_path+'/conf/uwsgi.conf', '/etc/init/'))
        sudo('initctl reload-configuration')

    #reload nginx
    with settings(warn_only=True):
        sudo('touch /etc/uwsgi/vassals/{}.ini'.format(PROJECT_NAME))
        sudo('service nginx reload')
        sudo('service uwsgi start')
        # sudo('service rabbitmq-server restart')


def list_tags():
    """List tags in git.
    """
    local("git for-each-ref --sort='*authordate' --format='%(tag) %(subject)' refs/tags")


def _create_deploy_key():
    """Creates a ssh-key to be used as deploy key on repo
    """
    run('mkdir -p /home/ubuntu/.ssh')
    if(not files.exists('/home/ubuntu/.ssh/id_rsa.pub')):
        run('ssh-keygen -t rsa -P ""')
    key = run('cat /home/ubuntu/.ssh/id_rsa.pub')
    print("""
Copy key and add as a deploy key to the repository:
{key}
""".format(key=key))

# def create_database(type='pgsql'):
#     sudo('mysql -uroot -p -e "create database if not exists {}"'.format(PROJECT_NAME))


def sync_database(cur_version_path):
    with cd(cur_version_path):
        with prefix('source {}'.format('~/.venv/'+PROJECT_NAME+'/bin/activate')):
            run('python manage.py migrate --settings={}.custom_settings.{}_settings'.format(PROJECT_NAME, env.environment))


def create_superuser():
    with cd('{}'.format('/var/www/'+PROJECT_NAME)):
        with prefix('source {}'.format('~/.venv/'+PROJECT_NAME+'/bin/activate')):
            run('python manage.py createsuperuser --settings={}.custom_settings.{}_settings'.format(PROJECT_NAME, env.environment))


@contextmanager
def local_prefix(shell, prefix):
    def local_call(command, capture=False):
        return local("%(sh)s \"%(pre)s && %(cmd)s\"" %
            {"sh": shell, "pre": prefix, "cmd": command}, capture=capture)
    yield local_call


def dump(shell='/bin/bash -lic'):
    with local_prefix(shell, 'source {}'.format(os.environ.get(
            'WORKON_HOME') + '/' + PROJECT_NAME + '/bin/activate')) as local:
        from fabric.contrib import django
        settings_file = '{}.custom_settings.{}_settings'.format(PROJECT_NAME,
            env.environment)
        django.settings_module(settings_file)
        db = ast.literal_eval(
            local("python -c 'from django.conf import settings\nprint("
                  "settings.DATABASES)'", True))
        print(db['default']['PASSWORD'])
        local('pg_dump -h {host} -U {user} {db_name} > {db_name}_{'
              'date}.dump'.format(host=db['default']['HOST'],
            user=db['default']['USER'], db_name=db['default']['NAME'],
            password=db['default']['PASSWORD'],
            date=datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"), ))