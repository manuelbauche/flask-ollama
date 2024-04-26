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

- Rename the `.env.sample` file into `.env`
    - Enter your variable names 
- Set a `JWT_Secret`, this is a (min) 32 byte-length string of characters, similar to a password. 
    - You can use this snippet to generate a cryptographically secure secret: 
    ```python
    python -c "import secrets; secret = secrets.token_bytes(32); print(secret.hex())"
    ```

## Configure Application
- Open `factory.py` and review app configuration
### OPTIONAL configure database server
`factory.py` is configured to create a local sqlite database which will be created in the folder `instance` within the application. 
- If desired to setup a cloud-based database server:
    - Uncomment `#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'`
    - Comment `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'`
    - Review .env file configuration to ensure the environment variables for your server are correct

## Run
- Ensure ollama is running on the background. 
- Run python application using `python app.py` or using `FLASK_APP run`.

# API Endpoints
- `/auth/register [POST]`: Register a new user. Accepts a JSON object with username and password fields.
    ```yaml
    {
    'newUsername': string,
    'newPassword': string
    }
    ```
- `/auth/login [POST]`: Log in a user. Accepts a JSON object with username and password fields. Returns a JWT token.
    ```yaml
    {
    'username': string,
    'password': string
    }
    ```
## Protected endpoints (JWT Required)
Requires a JWT token in the `Authorization` header.

- `/api/chat [GET, POST]`: Send a chat message. Accepts a JSON object with a message field.
    ```yaml
    {
    'message': string,
    }
    ```
- `/api/messages [GET]` Returns all messages of a user. 
- `/api/clear [DELETE]` Clears all messages associated to authenticated user in chat module.

### Testing endpoints only
Ideally this endpoints would be reserved for an admin panel _to be implemented_

- `/api/users [GET]` Returns a dictionary of all users and their information. 
- `/api/allmessages [GET]` Returns a dictionary of all messages and their information. 

# Testing
Run `pytest`

## Frontend testing
There is a simplistic UI to test the user-oriented endpoints. 
- Go to `http://localhost:5000/` 
- Register your username if you haven't already
- Log in using your valid username and password
- If valid credentials, you will be redirected. You need a token to access the other endpoints. 
- Make sure ollama is running, see point above in **Modules and Frameworks Installs**
    - Run ollama using `ollama run llama2`
- Interact with the conversation module, the responses will be streamed in realtime and may take a couple seconds to complete
- If previous conversations exist, these will be display upon load of the module. 

## Postman testing

# Improvements and Future Considerations
- Make more use of decorators to simply endpoint complexity and logic
- Implement retriavable message history, keep deleted conversations up to 30 days. 
- Use sentiment analysis to tailor Ollama responses
- Context management 
- Personalized experience using user data
