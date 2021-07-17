# Steps Github organization repositories checker
This project provides:<br>
A set of CRUD APIs for the mandatory steps required in the CircleCI pipelines of an organization. <br>
A REST API which returns all the repositories from an organization and their statuses (compliant/non-compliant),
and a list of jobs with their corresponding missing steps. <br>
A python scheduler which run and report regularly, the same as the REST API.

## Support
This repository was only tested on Ubuntu 18.04. 
However, with minor changes it could also run in Windows and other Linux OS.

## Installation
After cloning the repository. From the root folder, you can run either.
`make build` or `docker-compose up`. <br>
This step is necessary for testing and usage.

## Testing
Run `make test`. Or run `docker exec -it organization-repositories-checker_web_1 pytest`.

## Usage
To start using the Step API or organizations checker API, look at the API Documentation. <br>
Prior to starting using the organization checker you need to add a `develop.env` file with your Github credentials 
(at the root folder of this project ).
For example:<br>
```
GITHUB_TOKEN="<WRITE_YOUR_TOKEN_HERE>"
GITHUB_ORGANIZATION="<WRITE_YOUR_ORGANIZATION_NAME_HERE>"
```
Of course, your credentials should never be commited. If this project were to be deployed,
the developer is free to use their own way of securely generate their own .env files
at the different stages. For that purpose, the developer must change the .env file
pointed inside the `configs.py` at root level. <br>
<br>
Once the project is configured, run `make schedule` for activating the organization
repository checker scheduler. Currently, it is set to run every day at 9:00 AM. To change this setup,
it is necessary to go to `scheduler/scripts.py` and know about python `aioschedule`.<br>
To run the organization checker from the API, please go to the API Documentation.



## API Documentation
To see the API documentation I recommend opening its swagger documentation in
`http://127.0.0.1:8000/docs` (Remember having initialized the backend, see Installation). <br> <br>
Below you can find curl examples of the API.<br>
<b>Create a step</b>:<br>
`curl -X POST http://127.0.0.1:8000/api/steps -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "command": "<WRITE_YOUR_STEP_HERE>" }'` <br>
<b>Output</b>:<br>
`{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}`<br>
<b>Get a step</b>:<br>
`curl -X GET http://127.0.0.1:8000/api/steps/<THE_STEP_ID> -H 'accept: application/json'`<br>
<b>Output</b>:<br>
`{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}`<br>
<b>Get all steps</b>:<br>
`curl -X GET http://127.0.0.1:8000/api/steps -H 'accept: application/json'`<br>
<b>Output</b>:<br>
`[{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}]`<br>
<b>Edit a step</b>:<br>
`curl -X PUT http://127.0.0.1:8000/api/steps?step-id=<THE_STEP_ID> -H 'accept: application/json'   -H 'Content-Type: application/json' -d '{ "command": "<NEW_STEP>" }'` <br>
<b>Delete a step</b>:<br>
`curl -X DELETE http://127.0.0.1:8000/api/steps/<THE_STEP_ID> -H 'accept: application/json'`

<b>Get the Organizazion check</b>:<br>
`curl -X GET http://127.0.0.1:8000/service/steps/organization-check?organization-name=<YOUR_ORGANIZATION_NAME>&github-token=<YOUR_ORGANIZATION_TOKEN> -H 'accept: application/json'`<br>
<b>Output</b>:<br>
```
{
   "test-repo-1":[
      "This repository has no jobs."
   ],
   "test-repo-2":{
      "jobs":{
         "build-and-test":[
            "hi",
            "<WRITE_YOUR_STEP_HERE>",
            "<WRITE_YOUR_STEP_HERE>"
         ]
      },
      "status":"not-compliant"
   }
}
``` 

This last example is an example from my own organization. The output is a JSON that reads:<br>
First level:<br>
Dict. Keys are repositories from the organization. Values are either "This repository has no jobs.", or 
another dict.
Second Level:<br>
Dict. Keys are "jobs" with values another object, or "status" with value string which can be compilant or non-compilant. <br>
Thid Level: <br>
Dict. Keys are job names (e.g. "build-and-test") and values are a list of missing steps (e.g. "hi"). If values are an empty list, then the job will appear as compilant,
and if the values are no empty, then the status of the repository is non-compilant.<br>

The results from the organization check api could be made more readible like in a csv, a table, etc. But without
the exact description of its use cases, I left it out in a minimalistic way.

## Design of the project
![alt text](https://github.com/nachogon1/organization-repositories-checker/blob/master/documents/organization_checker_diagram.png?raw=true)


## Line of thought
Overall code:

    1. I decided to do a python scheduler instead of a github action or job since I would have to create runners, and It would make the project instructions much harder.

    2. The output of the organization repository checker is in JSON format, as it was not clearly defined how the output should look like. If a csv, or any specific format were desired, It can be changed later.

    3. The code for the checkup_steps in script/tools.py is a bit dirty. I should wrap it up better and make a better error handling. This part of the code might even break with strange config yamls.


Database:

    1. I chose mongo as a DB, as it provides me more flexibility with the models.

    2. I won’t add password	or usernames to the mongodb since it is only for testing purposes. For deploy stage, I would deploy the database independently and I would configure the app throw a cloud build config file.
       
    3. In this example I will use pymongo to interact with the DB, in order to make the testing easier and reduce the amount of code. But for production I would use Async Motor.


API:

    1. For the apis, I chose FastAPI, as it is a very fast modern framework. It has a very good documentation and It helps a lot documenting the api, as it serve them in swagger automaticallly.
       
    2. For validating the data from the api, I will use pydantic and typing. They are my favourite since they support class dot notation.

    3. In PUT methods, In production I would add etag checkups to avoid strange user experiences.

    4. The organization_check service uses our db endpoint (step_crud) to access the database in order to make easier the tests. However, it should call the Steps API with an http request to be more scalable, in this way the organization_check service could be deployed as an independent microservice. (For this case, the tests would increase in difficulty, as I would have to mock it with a a fake server as it happens with the Gitcalls in the integration test).

Build

    1. I am not a “make” expert. I did what I could in the shortest period of time.
       
    2. For deploying stages. I would use some shell script in the pipeline, where I would create the different envs. So far, I called develop.env to the environment of the project.

    3. When deploying the application to test or live systems, the command uvicorn to start the app should be change for gunicorn.

Testing

    1. I have only made integration tests for the REST API and the checker service. But It would be good to add unit tests for the functions in tools.py.

Security

    1. Ideally all the APIs should be guarded with some kind of credentials system. Eihter some token, or some login system.

    2. Sensitive credentials for production or test systems must come from secured vaults (Vault, Git CI/CD, etc) and be integrated at some point in the pipeline, but the deployment is out of the scope of this project.
       
Code quality

    1. For code quality I followed the PEP-8 python style. For linting processes I used black, isort and flake8.

## Developers
Ignacio Gonzalez Betegon

