## Development Setup
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
```

Type `make`. Run your code in a virtualenv. Type `. venv/bin/activate` to do so.

## Running the App Locally
```
pip3 install --editable .
export FLASK_APP=subscribely
flask initdb
flask run
```
Runs on http://localhost:5000/ by default.
