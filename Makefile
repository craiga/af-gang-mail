default:  ## Build and serve the web site.
	pipenv run python manage.py migrate
	make scss
	make js
	pipenv run python manage.py runserver

queue:  ## Run the task queue.
	rabbitmq-server

worker:  ## Run one instance of the queue worker.
	pipenv run watchmedo auto-restart --pattern=*.py --recursive -- celery worker --app af_gang_mail --loglevel INFO

monitor:  ## Run the web-based queue monitor.
	pipenv run watchmedo auto-restart --pattern=*.py --recursive -- celery flower --app af_gang_mail

db:  ## Create a database.
	createuser af_gang_mail --createdb
	psql --command "alter user af_gang_mail with encrypted password 'security_is_important';"
	createdb af_gang_mail --owner=af_gang_mail

db-delete:  ## Delete database.
	dropdb af_gang_mail
	dropuser af_gang_mail

setup:  ## Install required environments and packages.
	pipenv install --dev
	npm ci

dotenv:  ## Create .env file suitable for development.
	printf "DEBUG=1\nDATABASE_URL=postgres://af_gang_mail:security_is_important@localhost/af_gang_mail\n" > .env

superuser: ## Create a Django superuser. Requires DJANGO_SUPERUSER_USERNAME, _EMAIL and _PASSWORD environment variables.
	pipenv run python manage.py createsuperuser --no-input

test: ## Run tests.
	pipenv run pytest

check-django:  ## Check Django configuration. Will fail if DEBUG is set to true.
	pipenv run python manage.py makemigrations --check
	pipenv run python manage.py check --deploy --fail-level INFO

migrations:  ## Create Django migrations.
	pipenv run python manage.py makemigrations
	pipenv run black **/migrations/*.py
	pipenv run isort --apply **/migrations/*.py

migrate:  ## Run Django migrations.
	pipenv run python manage.py migrate

cypress-web:  ## Build and serve the web site for Cypress.
	PIPENV_DONT_LOAD_ENV=1 DATABASE_URL=postgres://af_gang_mail_cypress:security_is_important@localhost/af_gang_mail_cypress pipenv run python manage.py migrate
	PIPENV_DONT_LOAD_ENV=1 DEBUG=1 DATABASE_URL=postgres://af_gang_mail_cypress:security_is_important@localhost/af_gang_mail_cypress pipenv run python manage.py runserver 8001

cypress-db:  ## Create database for Cypress.
	createuser af_gang_mail_cypress --createdb
	psql --command "alter user af_gang_mail_cypress with encrypted password 'security_is_important';"
	createdb af_gang_mail_cypress --owner=af_gang_mail_cypress

cypress-db-delete:  ## Delete database for Cypress.
	dropdb af_gang_mail_cypress
	dropuser af_gang_mail_cypress

scss:  ## Build SCSS.
	npm run sass -- .

scss-continuous:  ## Build SCSS continuously.
	npm run sass -- . --watch

js:  ## Build JavaScript.
	find . \( -path "./node_modules" -o -iname "bundle.*" \) -prune -o -path "*/static/*" -a -name "*.js" -print | xargs npm run browserify -- --outfile af_gang_mail/static/bundle.js

js-continuous:  ## Build JavaScript continuously.
	find . \( -path "./node_modules" -o -iname "bundle.*" \) -prune -o -path "*/static/*" -a -name "*.js" -print | xargs npm run watchify -- --outfile af_gang_mail/static/bundle.js --verbose

lint-python:  ## Lint Python.
	pipenv run isort --check-only
	pipenv run black --check --diff .
	find . -iname "*.py" | xargs pipenv run pylint

fix-python:  ## Attempt to automatically fix Python issues reported by linter.
	pipenv run isort --apply
	pipenv run black .

lint-yaml: ## Lint YAML.
	npm run prettier -- "**/*.yaml" --check

fix-yaml: ## Attempt to fix YAML issues reported by the linter.
	npm run prettier -- "**/*.yaml" --write

lint-json: ## Lint JSON.
	npm run prettier -- "**/*.json" --check

fix-json: ## Attempt to fix JSON issues reported by the linter.
	npm run prettier -- "**/*.json" --write

lint-scss: ## Lint SCSS.
	npm run prettier -- "**/*.scss" --check

fix-scss: ## Attempt to fix SCSS issues reported by the linter.
	npm run prettier -- "**/*.scss" --write

lint-js: ## Lint JavaScript.
	npm run prettier -- "**/*.js" --check

fix-js: ## Attempt to fix JavaScript issues reported by the linter.
	npm run prettier -- "**/*.js" --write

help: ## Display this help screen.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
