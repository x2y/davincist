ORIGINAL_PATH=$(pwd)
DAVINCIST_ROOT=$(echo "$ORIGINAL_PATH" | grep '.*?/davincist' -o -P | head -1)

cd $DAVINCIST_ROOT/media/less/

rm -rf ./bootstrap/
git clone git://github.com/twbs/bootstrap.git bootstrap
git add bootstrap/

cd $ORIGINAL_PATH