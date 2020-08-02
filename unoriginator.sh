#!/bin/bash
set -e

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

FIRST_INSTALL=""
if [[ ! -d ~/.virtualenvs/unoriginator ]]; then
  python3 -mvenv ~/.virtualenvs/unoriginator
  FIRST_INSTALL="yes"
fi

. ~/.virtualenvs/unoriginator/bin/activate

if [[ ! "$FIRST_INSTALL" == "" ]]; then
  pip3 install mutagen
fi

python3 "${SCRIPT_DIR}"/unoriginator.py "$@"

deactivate
