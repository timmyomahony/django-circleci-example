#!/usr/bin/python2

from fabric.api import env, run, cd, task, sudo

debug = False

"""
Fabric deploy script

This is a Fabric (python 2.7) deployment script to be used by CircleCI to
deploy this project automatically to either production or staging.
"""

if debug:
    import paramiko
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

env.venv_name = 'django-circleci-example'
env.venvs_path = '~/django-circleci-example'
env.user = 'admin'
env.gateway = 'timmyomahony.com:30000'


@task
def production():
    env.type = 'production'
    env.branch = 'master'
    env.settings_path = 'config.settings.production'
    env.path = '{0}{1}/{1}/'.format(env.venvs_path, env.venv_name)
    env.hosts = ['timmyomahony.com:30000', ]


@task
def staging():
    env.type = 'staging'
    env.branch = 'develop'
    env.settings_path = 'config.settings.production'
    env.path = '{0}{1}/{1}/'.format(env.venvs_path, env.venv_name)
    env.hosts = ['timmyomahony.com:30000', ]


@task
def venv(cmd):
    run('workon {0} && {1}'.format(env.venv_name, cmd))


@task
def restart():
    sudo('sudo supervisorctl reread')
    sudo('sudo supervisorctl update')
    sudo('sudo supervisorctl restart ci-api ')


@task
def update():
    with cd(env.path):
        run('git pull origin {0}'.format(env.branch))
        venv('pip install -r src/requirements.txt')
        venv('django-admin migrate')
        venv('django-admin collectstatic --noinput')


@task
def deploy():
    update()
    restart()
