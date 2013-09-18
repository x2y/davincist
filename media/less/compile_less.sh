#!/bin/bash
# Usage: bash compile_less.sh

ORIGINAL_PATH=$(pwd)
DAVINCIST_ROOT=$(echo "$ORIGINAL_PATH" | grep '.*?/davincist' -o -P | head -1)

cd $DAVINCIST_ROOT/media/less/

nodejs /usr/bin/grunt watch

cd $ORIGINAL_PATH