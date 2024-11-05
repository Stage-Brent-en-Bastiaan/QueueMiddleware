# Usecase2
##to run the queue middleware
###to create the virtual environment
python -m venv .venv
###to activate the virtual environment
.venv/scripts/activate.ps1
###to install the packages based on requirements.txt
pip install -r --requirements.txt

##when you add a new package 
make sure to activate the venv before you do
###to update requirements.txt
pip freeze > requirements.txt 



## Start REST API server
py manage.py runserver 0.0.0.0:8000