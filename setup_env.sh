#!/usr/bin/env bash
# -*- coding: utf-8 -*-

set -e

ANACONDA=${HOME}/anaconda
ENVDIR=${ANACONDA}/envs
ENVNAME=K2VarCat
ENVPATH="${ENVDIR}/${ENVNAME}"

CONDA_PKGS='astropy==0.4.2 ipython==2.3.1 jinja2==2.7.3 matplotlib==1.4.2 numpy==1.9.1 pandas==0.15.2 pytest==2.6.4 scipy==0.14.0 seaborn==0.5.1 sqlalchemy==0.9.8'

run() {
    echo $*
    $@
}

create_initial_environment() {
    echo "Creating conda environment"
    run conda create -n ${ENVNAME} python=3 pip ${CONDA_PKGS}
}

install_requirements() {
    echo "Installing from requirements.txt"
    run pip install --root "${ENVPATH}" -r requirements.txt
}

develop_install() {
    echo "Installing package in development mode"
    run python setup.py develop --prefix "${ENVPATH}"
}

setup_direnv() {
    echo "source activate ${ENVNAME}" > .envrc
    direnv allow
}

main() {
    test -d "${ENVDIR}/${ENVNAME}" || create_initial_environment
    source activate "${ENVNAME}"
    install_requirements
    develop_install
    setup_direnv
}

main
