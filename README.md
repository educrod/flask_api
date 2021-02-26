# README #

### What is this repository for? ###

* Repository to present a api solution.
* Version 1.0

### How do I get set up? ###
* Dependencies
    - Docker version 18.09.6-ce or above
    - docker-compose version 1.24.0 or above
    - git version 2.22.0 or above
* Clone the project
    - `git clone https://github.com/educrod/flask_api.git`
* Be sure to be inside project directory flask_api and run docker-compose
    - `docker-compose up -d --build`
* Running the tests
    - `docker-compose exec flask python -m unittest discover -v`
* Posting data to the API
    - `curl -X POST -H 'Content-Type: application/json' -i 'http://0.0.0.0/authorize' --data '{ "Transaction": { "merchant": "Americanas", "amount": 50, "time": "'"$(date "+%Y-%m-%d %H:%M:%S")"'" }}'`