#!/usr/bin/env bash

set -e

DIRS=(
    /storage/astro2/phrlbj/K2/campaign0/Detrend_DR2_v5
    /storage/astro2/phrlbj/K2/campaign1/Detrend_v5
    )

dest() {
    echo "$(readlink -f $(dirname $0)/data)"
}

unify_names() {
    sed 's/XD/X_D/'
}

link_generic() {
    read ROOT_DIR
    (cd `dest`
    ls ${ROOT_DIR}/ktwo*.fits | while read fname; do
        basename=$(basename ${fname} | unify_names)
        test -e ${basename} && echo "File ${fname} exists, skipping" || ln -sv ${fname} ${basename}
    done
    )
}

main() {
    for dir in ${DIRS[@]}; do
        echo "Linking files from ${dir}"
        echo ${dir} | link_generic
    done
}

main
