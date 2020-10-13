# fileuploaderproj

Git History got deleted due to some error . I have added the files via upload

Clone the project and Install the dependencies:
pip install pipenv 
pipenv install
pipenv shell

To migrate the database:
python manage.py makemigrations authentication
python manage.py makemigrations fileManager
python manage.py migrate

To start the server :
python manage.py runserver 


