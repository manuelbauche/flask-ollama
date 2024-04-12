# Install Flask

First you will want to create a virtual environment. 

Windows: As per custom, it is recommended to use a virtual linux environment like WSL or a virtual machine, many of the commands that facilitate this processes are unique to Shell. 

However, the newest Microsoft PowerShell does allow for many Unix Shell-like commands.

## Create a Virtual Environment

* First install virtualenv using 'pip install virtualenv' 
* You can test it was correctly installed by using virtualenv --version
* Create a virtual environment 'virtualenv [your_environment_name] -p python3' this will create a virtual env using your current version of Python 3. This project was built using v3.12.0
* Now access your environment using 'source [env_name]/bin/activate' 
	* For Windows access the dictory where the environment was created and use '[env_name]\Scripts\activate'
* Next install Flask 'pip install flask' 
* You can check 'requirements.txt' for specific versions, many libraries are installed together with Flask
* Set the environment variable 'export FLASK_APP=app.py' for Unix-based console and 'set FLASK_APP=app.py' for Windows
* Run the application using 'flask run'