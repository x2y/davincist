cd ~
sudo easy_install pip
sudo pip install yolk

pip install virtualenv
pip install virtualenvwrapper

echo "
PATH=\"/Library/Frameworks/Python.framework/Versions/2.7/bin:/usr/local/mysql/bin:${PATH}\"

# virtualenv
export WORKON_HOME=$HOME/.virtualenvs
source /Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh

# virtualenv aliases
# http://blog.doughellmann.com/2010/01/virtualenvwrapper-tips-and-tricks.html
alias v='workon'
alias v.deactivate='deactivate'
alias v.mk='mkvirtualenv --no-site-packages'
alias v.mk_withsitepackages='mkvirtualenv'
alias v.rm='rmvirtualenv'
alias v.switch='workon'
alias v.add2virtualenv='add2virtualenv'
alias v.cdsitepackages='cdsitepackages'
alias v.cd='cdvirtualenv'
alias v.lssitepackages='lssitepackages'

alias manage='python ../manage.py '
alias test-all='pyrg ../manage.py test '

alias s1='manage schemamigration app --auto'
alias s2='manage migrate app'

alias gs='git status'
alias ga='git add'
alias gr='git reset'
alias grm='git rm'
alias gm='git mv'
alias gl='git log'
alias gd='git diff'
alias gc='git commit'
alias gpsh='git push'
alias gpll='git pull'" >> ~/.bash_profile

. ~/.bash_profile

mkdir dev
mkdir dev/davincist
cd dev/davincist

v.mk davincist

echo "Now install Git from http://git-scm.com/downloads. Hit enter when complete..." && read

echo "Now set up SSH keys: http://guides.beanstalkapp.com/version-control/git-on-mac.html. Hit enter when complete..." && read

git clone git@github.com:x2y/davincist.git

deactivate
v davincist

sudo pip install yolk

echo "Now download & install mysql from http://dev.mysql.com/downloads/mysql/ (x86 64-bit DMG). Hit enter when complete..." && read

echo "Now install XCode CLI tools. Hit enter when complete..." && read

sudo pip install -r env_reqs

cd davincist
manage runserver







