# Steps Github organization repositories checker
This project provides:<br>
A set of CRUD APIs for the mandatory steps required in the CircleCI pipelines of an organization.
A REST API which returns which repositories from an organization complies with the mandatory steps and
list which steps from each job are missing.
A python scheduler which run and report regularly the same as the REST API.

## Support
This repository was only tested on Ubuntu 18.04. 
However, with minor changes it could also run in windows and other Linux OS.

## Installation
After cloning the repository. From the root folder, you can run either.
`make build` or `docker-compose up`.
Installing is necessary for testing and usage.

## Testing
Run `make test`.

## Usage
To start using the Step API or organizations checker API, look at the API Documentation. <b>
Prior to start using the organization checker you need to add a `develop.env` file with your Github credentials.
For example:<br>
```
GITHUB_TOKEN="<WRITE_YOUR_TOKEN_HERE>"
GITHUB_ORGANIZATION="<WRITE_YOUR_ORGANIZATION_NAME_HERE>"
```
Of course, your credentials should never be commited. If this project wanted to be deployed,
the developer is free to use their own way of securely generate their own .env files
at the different stages. For that purpose, the developer must change the .env file
indicated in `configs.py` at root level. <br>
Once the project is configured, then run `make schedule` for activating the organization
repository checker scheduler. Currently it is set to run every day at 9:00. To change this setup
it is necessary to go to `scheduler/scripts.py`  and know about python `aioschedule`.<br>
To run the organization checker from the API, please go to the API Documentation.



## API Documentation
To see the API documentation I recommend opening its swagger documentation in
`http://127.0.0.1:8000/docs`.
Below you can find curl examples of the API.<br>
Create a step:<br>
`curl -X POST http://127.0.0.1:8000/api/steps -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "command": "<WRITE_YOUR_STEP_HERE>" }'` <br>
Output:<br>
`{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}`<br>
Get a step:<br>
`curl -X GET http://127.0.0.1:8000/api/steps/<THE_STEP_ID> -H 'accept: application/json'`<br>
Output:<br>
`{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}`<br>
Get all steps:<br>
`curl -X GET http://127.0.0.1:8000/api/steps -H 'accept: application/json'`<br>
Output:<br>
`[{"command":"<WRITE_YOUR_STEP_HERE>","_id":"<THE_STEP_ID>"}]`<br>
Edit a step:<br>
`curl -X PUT http://127.0.0.1:8000/api/steps?step-id=<THE_STEP_ID> -H 'accept: application/json'   -H 'Content-Type: application/json' -d '{ "command": "<NEW_STEP>" }'`
Delete a step:<br>
curl -X DELETE http://127.0.0.1:8000/api/steps/<THE_STEP_ID> -H 'accept: application/json'

Get the Organizazion check:<br>
`curl -X GET http://127.0.0.1:8000/service/steps/organization-check?organization-name=<YOUR_ORGANIZATION_NAME>&github-token=<YOUR_ORGANIZATION_TOKEN> -H 'accept: application/json'`<br>
Output:<br>
`{"test-repo-1":["This repository has no jobs."],"test-repo-2":{"jobs":{"build-and-test":["hi","<WRITE_YOUR_STEP_HERE>","<WRITE_YOUR_STEP_HERE>"]},"status":"not-compliant"}}` <br>
This last example is an example from my own organization. The output is a JSON that reads:
First level:<br>
Dict. Keys are repositories from the organization. Values are either "This repository has no jobs.", or 
another dict.
Second Level:<br>
Dict. Keys are jobs with values another object, or status with value string which can be compilant or non-compilant. <br>
Thid Level: <br>
Dict. Keys are job names and values are missing steps. If values are an empty list then the job will appear as compilant,
and if the values are no empty, then the status of the repository is non-compilant.<br>
There is plenty of space to make better the results more readible like in a csv, a table, etc. But without
the exact description of its usecases I left it out in a minimalistic way.

## Design of the project
![alt text](https://github.com/nachogon1/organization-repositories-checker/blob/master/documents/organization_checker_diagram.png?raw=true)


## Line of thought

## Contributors
Ignacio Gonzalez Betegon

