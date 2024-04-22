# Pre-Requisites

## Install Flask

First you will want to create a virtual environment. 

Windows: As per custom, it is recommended to use a virtual linux environment like WSL or a virtual machine, many of the commands that facilitate this processes are unique to Shell. 

However, the newest Microsoft PowerShell does allow for many Unix Shell-like commands.

## Create a Virtual Environment

- Install virtualenv using 'pip install virtualenv' 
    - You can test it was correctly installed by using virtualenv --version
- Create a virtual environment `virtualenv [your_environment_name] -p python3` this will create a virtual env using your current version of Python 3. This project was built using v3.12.0
- Now access your environment using `source [env_name]/bin/activate` for Unix based terminals 
	- For Windows access the directory where the environment was created and use `[env_name]\Scripts\activate`
    - You can confirm that your venv is loaded by using `which python`. If the path is within your venv, you did it correctly.

## Modules and Frameworks installs 

- Next install all required modules using `pip install requirements.txt` 
    - Check 'requirements.txt' for specific versions, many libraries are installed together with Flask
- Set the environment variable `export FLASK_APP=app.py` for Unix-based console and `set FLASK_APP=app.py` for Windows
- Install [ollama](https://ollama.com/)
- Install and run llama2 using `ollama run llama2` this will take some minutes

# Run Application

## Set Environment Variables

- Create a `.env` file with the structure provided by .env-sample. 
    - Enter your variable names 
- Set a `JWT_Secret`, this is a (min) 32 byte-length string of characters, similar to a password. 
    - You can use this snippet to generate a cryptographically secure secret: `python -c "import secrets; secret = secrets.token_bytes(32); print(secret.hex())"`

## Run
- Ensure ollama is running on the background. 
- Run python application using `python app.py` or using `FLASK_APP run`.

# API Endpoints
- `/auth/register`: Register a new user. Accepts a JSON object with username and password fields.
    ```json
    {
    'newUsername': string,
    'newPassword': string
    }
    ```
- `/auth/login`: Log in a user. Accepts a JSON object with username and password fields. Returns a JWT token.
- `/api/chat`: Send a chat message. Accepts a JSON object with a message field. Requires a JWT token in the `Authorization` header.

# Testing
Run `pytest`
