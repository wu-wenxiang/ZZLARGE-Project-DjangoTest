#!/usr/bin/env bash

pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}

function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate

    pip install -r requirements.txt
}

function rebuild_db {
	logging "Clean"
	rm -rf "${BASE_DIR}/mysite/db.sqlite3"
	rm -rf "${BASE_DIR}/mysite/account/migrations/0*"
	ls "${BASE_DIR}/mysite/account/migrations/"
	logging "migrate"
	python "${BASE_DIR}/mysite/manage.py" "migrate"
	logging "makemigrations" "account"
	python "${BASE_DIR}/mysite/manage.py" "makemigrations" "account"
	logging "migrate"
	python "${BASE_DIR}/mysite/manage.py" "migrate"
	logging "initdb.py"
	python "${BASE_DIR}/mysite/initdb.py"
}

function launch_webapp {
    cd ${BASE_DIR}/mysite
    python "manage.py" "runserver"
}

#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

if [ "${OPT_ENV_FORCE}x" == "-fx" ];then
    python "${BASE_DIR}/manage.py" "clean"
fi

python "${BASE_DIR}/manage.py" "prepare"
build_venv

if [ "${OPT_ENV_FORCE}x" != "-kx" ];then
    rebuild_db
fi

launch_webapp
