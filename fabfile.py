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
    build(root='/phsnag/')
    run('rsync -va build/ ~/www/')

def build(root=None):
    if root is not None:
        local('k2var-freeze --root "{root}"'.format(root=root))
    else:
        local('k2var-freeze')

@task
def package():
    with lcd('~/work/Other/K2VarCat'):
        with prefix('source ~/anaconda/bin/activate ./venv'):
            build(root='/phrlbj/k2varcat/')
        with lcd('~/work/Other/K2VarCat/build'):
            local('tar -zcvf ../build.tar.gz .')
