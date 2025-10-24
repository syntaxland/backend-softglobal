# DRF Live Chat
To run this app:

In the project directory, you can run:

### `py -m venv venv` or `python -m venv venv`

To create the virtual env.

### `venv\Scripts\activate.bat` 

To activate the virtual env.

### `pip install -r requirements.txt` 

To install packages in the virtual env.

### `python manage.py migrate` 
 
To create the the db.

### `daphne -b 0.0.0.0 -p 8000 be_test.asgi:application` 
 
To start the live server having installed, configured and started redis for you machine running at default port 6379 and ready to receive connection...


### Testing `with coverage` 

coverage report

coverage html

coverage run --omit='*/venv/*' manage.py test

python manage.py test
