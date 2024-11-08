# Usecase2
## to run the queue middleware
### when you clone the repo
#### navigate to the folder with requirements.txt
#### create the virtual environment
$python -m venv .venv
#### activate the virtual environment(only on windows)
$.venv/scripts/activate
#### install the packages based on requirements.txt
$pip install -r --requirements.txt

### when you add a new package 
#### activate the virtual environment(only on windows)
$.venv/scripts/activate
#### update requirements.txt
$pip freeze > requirements.txt 

### to run the app in debug mode
$py Usecase2.py

### to install and start the service
$py WindowsService.py install
$py WindowsService.py start

## Start REST API server
py manage.py runserver 0.0.0.0:8000