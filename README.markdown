# AF GANG Mail Exchange

💖 https://mail.afgang.co.uk 💖

## Getting Started

To run the site locally, run:
 * `make setup` to set up the environment;
 * `make db` to create a database;
 * `make dotenv` to write a default `.env` file; and then 
 * `make` to start the website.

Run `make help` for information on how to run tests, linting, etc.


## Running Cypress Tests Locally

Getting Cypress tests to run locally is a little bit involved.

First, make sure you stop any running web or worker processes.

Next, run the following commands:

* `make cypress-db` to create the database the site under test will use;
* `make queue` to run RabbitMQ;
* `make cypress-worker` to run a worker process;
* `make cypress-web` to run the site to test; and finally
* `make cypress` or `make cypress-interactive` to run the tests (`make cypress-interactive` will run Cypress' GUI and allow you to observe the tests running).
