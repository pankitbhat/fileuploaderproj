# fileuploaderproj

Git History got deleted due to some error . I have added the files via upload

Clone the project and Install the dependencies <br />
pip install pipenv <br />
pipenv install <br />
pipenv shell <br />

To migrate the database: <br />
python manage.py makemigrations authentication <br />
python manage.py makemigrations fileManager <br />
python manage.py migrate <br />

To start the server: <br />
python manage.py runserver <br />

Register a User <br />
Endpoint - http://localhost:8000/api/users/ (POST) <br />
Body - { <br />
    "user":{ <br />
    "email":"test@gmail.com", <br />
    "username":"test", <br />
    "password":"test@2020" <br />
} <br />
} <br />




