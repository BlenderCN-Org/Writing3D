#!/bin/bash
if [ ! -z "$BASH_SOURCE" ]
then
    SCRIPT_NAME="${BASH_SOURCE[0]}"
else
    SCRIPT_NAME="$0"
fi
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$SCRIPT_NAME" 2>/dev/null ||\
    greadlink -f "$SCRIPT_NAME" 2>/dev/null ||\
    echo "$SCRIPT_NAME")")" && pwd -P)"
cd "$SCRIPT_DIR/../../.."


if type "git" > /dev/null
then
    echo "Git found! Using Git to update..."
    cd Writing3D
    git rev-parse HEAD > ../last_good.txt
    git fetch && git reset --hard origin/master || echo "Could not fetch update..."
else
    echo "Git not found. Downloading zipped distribution..."
    echo "Making backup of current distribution..."
    zip -r last_good.zip Writing3D
    curl -Lk "https://github.com/wphicks/Writing3D/archive/master.zip" -o Writing3D.zip || (echo "Download failed."; exit 1)
    unzip Writing3D.zip
    rm -rf Writing3D
    mv Writing3D-master Writing3D
fi
