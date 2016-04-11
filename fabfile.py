import os, re
from datetime import datetime

from fabric.api import *


#server user name
env.user = 'zhengnan'

# sudo user
env.sudo_user = 'root'

# server address
env.hosts = ['192.168.56.103']

db_user = 'www-data'
db_password = 'www-data'

_TAR_FILE = 'dist-awesome.tar.gz'

def build():
    includes = ['static', 'templates', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
	cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
	cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
	cmd.extend(includes)
	local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'

def deploy():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # remove exist tar file
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # upload new tar file
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # make new dir
    with cd(_REMOTE_BASE_DIR):
	sudo('mkdir %s' % newdir)

    # unzip tar to new directory
    with cd('%s/%s' % _REMOTE_TMP_TAR):
	sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)

    # re-set the soft link
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
	sudo('ln -s %s www' % newdir)
	sudo('chown www-data:www-data www')
	sudo('chown -R www-data:www-data %s' % newdir)

    # restart python and nginx service
    with settings(warn_only=True):
	sudo('supervisorctl -c /etc/supervisor/supervisord.conf stop awesome')
	sudo('supervisorctl -c /etc/supervisor/supervisord.conf start awesome')
	sudo('/etc/init.d/nginx reload')
  
