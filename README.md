# Flask Forum
A simple project to start a forum in flask.

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/nikappa57/flask-forum?style=for-the-badge) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/nikappa57/flask-forum/flask?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/nikappa57/flask-forum?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/Nikappa57/flask-forum?style=for-the-badge) 
## Forum System
```
Categories 
|
└───Sections
    |
    └───threads
        │
        └───Comments
            |
            └───SubComments

```

## Features
- authentication system
- CRUD system on category, section and threads
- system of comments and answers with tags and upvotes
- management of permissions with ranks system
- category and threads position management
- other... like pinned thread and rank badges

## Installation

Clone this repo:
```console
git clone https://github.com/Nikappa57/flask-forum
```

Create the virtual environme,

For example:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

And the environment variable `FLASK_APP`.

For example:
```console
export FLASK_APP=run.py
```
or save it in a file `.flaskenv`.


Now create the `.env` file with the other environment variable.
```plaintext
SECRET_KEY=mykey
MAIL_USERNAME=mail@gmail.com
MAIL_PASSWORD=mailpassw
MAIL_DEFAULT_SENDER=mail@gmail.com
```

#### Set up
Now you just need to set the settings of your forum.

Sets the ranks and their permissions as you prefer in `Site/src/permission_default.py` and `Site/src/rank_default.py`.

Prepare the database.
```
flask db init
flask db migrate
flask db upgrade
```

Now you should be ready to start your forum.
```console
flask run
```
 
Have fun adding all the functions you want and create a good frontend (do not use mine because it sucks!).
