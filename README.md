# fileuploaderproj

Git History got deleted due to some error . I have added the files via upload

Clone the project and Install the dependencies <br />
pip install pipenv <br />
pipenv install <br />
pipenv shell <br />

**To migrate the database:** <br />
python manage.py makemigrations authentication <br />
python manage.py makemigrations fileManager <br />
python manage.py migrate <br />

**To start the server:** <br />
python manage.py runserver <br />

**Register a User** <br />
**Endpoint** - http://localhost:8000/api/users/ (POST) <br />
**Body** - { <br />
    "user":{ <br />
    "email":"test@gmail.com", <br />
    "username":"test", <br />
    "password":"test@2020" <br />
} <br />
} <br />

**Login a User** <br />
**Endpoint** - http://localhost:8000/api/users/login/ (POST) <br />
**Body** - { <br />
    "user":{ <br />
    "email":"test@gmail.com", <br />
    "password":"test@2020" <br />
} <br />
} <br />

**Response** - <br />
{ <br />
    "user": { <br />
        "email": "test@gmail.com", <br />
        "username": "test", <br />
        "token": TOKEN_VALUE <br />
    } <br />
} <br />

**Upload a File** - <br />
**Endpoint** - http://localhost:8000/file/upload/ (POST) <br />
**Headers** - 'Authorization': 'Token TOKEN_VALUE' <br />
**Body (form-data)** - <br />
**docfile** - File to upload <br />
**name**    - Chapter1 <br />
**owner**   - email_id of user <br />

**Move a File** - <br />
**Endpoint** - http://localhost:8000/file/fileops/ (POST) <br />
**Headers** - 'Authorization': 'Token TOKEN_VALUE' <br />
**Body (form-data)** - <br />
**old_path** - test.docx <br />
**new_path**    - third/ <br />

**Delete a File** - <br />
**Endpoint** - http://localhost:8000/file/upload/ (DELETE) <br />
**Headers** - 'Authorization': 'Token TOKEN_VALUE' <br />
**Body (form-data)** - <br />
**name** - test.docx <br />

**Rename a File** - <br />
**Endpoint** - http://localhost:8000/file/fileops/ (PUT) <br />
**Headers** - 'Authorization': 'Token TOKEN_VALUE' <br />
**Body (form-data)** - <br />
**old_filename** - third/test.docx <br />
**new_filename**    - Tool.docx <br />

**Copy a File** - <br />
**Endpoint** - http://localhost:8000/file/copy/ (POST) <br />
**Headers** - 'Authorization': 'Token TOKEN_VALUE' <br />
**Body (form-data)** - <br />
**filename** - Tool.docx <br />
**destination**  - third/ <br />


**In another terminal , activate the virtual env and do this to index documents in Whoosh** <br />
python manage.py rebuild_index <br />

**Search File Name in Index:** <br />
**Endpoint** - http://localhost:8000/file/filename/search/
**Query Params** - 'title':'Tool'













