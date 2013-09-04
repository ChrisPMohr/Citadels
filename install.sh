# Select current version of virtualenv:
VERSION=1.10.1
# Name of virtual environment:
ENV=env
# Set to whatever python interpreter you will be used to make the 
# virutal environment:
PYTHON=$(which python)
URL_BASE=https://pypi.python.org/packages/source/v/virtualenv

# --- Real work starts here ---
curl -O $URL_BASE/virtualenv-$VERSION.tar.gz
tar xzf virtualenv-$VERSION.tar.gz
# Create the virtual environment.
$PYTHON virtualenv-$VERSION/virtualenv.py $ENV
# Install the requirements
source $ENV/bin/activate
pip install -r requirements.txt
# Clean up
rm virtualenv-$VERSION.tar.gz
rm -rf virtualenv-$VERSION
