#!/bin/bash
# Usage: bash compile_less.sh

type lessc >/dev/null 2>&1 || {
  echo >&2 "Installing Less compiler..."
  sudo apt-get install rubygems1.8 ruby1.8-dev
  
  sudo gem install rubygems-update
  sudo gem update rubygems
  sudo gem install less
  sudo gem install therubyracer

  sudo ln -s /var/lib/gems/1.8/bin/lessc /usr/bin/
}

DAVINCIST_ROOT=$(pwd | grep '.*?/davincist' -o -P | head -1)

lessc -x \
    $DAVINCIST_ROOT/media/less/custom-bootstrap.less > \
    $DAVINCIST_ROOT/media/css/bootstrap.min.css