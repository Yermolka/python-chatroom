# Simple async client-server chat app
## Prerequisites
Python>=3.10
Clone the repository, cd into it and then
> pip install -r requirements.txt

Or you can use a virtual environment with pipenv
> pip install pipenv
>
> pipenv shell
> 
> pipenv install

## How to run
The project has simple cli tools in main.py
To run the server:
> python main.py run_server

To run the client:
> python main.py run_client -u username -p password

Available users are:
> -u admin -p admin
> 
> -u somecoolguy -p 123456
