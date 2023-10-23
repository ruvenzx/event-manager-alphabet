# event-manager-alphabet
AlphaBet Backend Home Excercise

## 1. Prerequisites 
### Docker installed
### Python 3.6+

## 2. Howto use
### cd to folder
### run 'docker-compose up -d --build'
### go to http://localhost:8008/docs for api docs
### debug using 'docker-compose logs -f web'


## 3. Tests
### NOTE: test do run locally and you should have postresql installed in order to run them.
### install all requirements using pip
### make sure you have a test db address in env var called: "DATABASE_URL" e.g: postgresql://user:pass@localhost:5432/db_name (in python's venv)
### cd to folder and run 'pytest'


## Architecture
![Arc](https://imageupload.io/ib/4xex1RmX0lEgcmC_1698078703.png)

### please note that api gw and sendgrid are not a part of the implementation as i would implement this thoroughly.