from fabric.api import *

env.use_ssh_config = True

def git(cmd):
    cmd = 'git {cmd}'.format(cmd=cmd)
    return run(cmd)

@task
def deploy():
    with cd('~/work/Other/K2VarCat'):
        update_repository()
        with prefix('source ~/anaconda/bin/activate ./venv'):
            install()

@task
def update_repository():
    git('checkout -q master')
    git('fetch origin')
    git('merge --ff origin/master')

@task
def install():
    run('k2var-freeze --root "/phsnag/"')
    run('rsync -va build/ ~/www/')
