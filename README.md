# Weekly Menu Exercise

API [exercise](https://github.com/hello-abhishek/hf-take-home-programming-challenges/blob/main/SOFTWARE-ENGINEER.md) for building a weekly menu.

- Development setup: Poetry
- Running application: Poetry or Docker
- Python requirements: `3.8.4+`

> Workflow and task related docs are below as well.

## Running the application

### Setup using Docker

```shell script
docker-compose build
docker-compose up
```

Application should be available at `http://0.0.0.0:8080/api/`

### Setup using poetry

- Instructions for install poetry: https://python-poetry.org/docs/#installation
- Use python ^3.8.4
- Run the following command

```shell script
poetry install
poetry run python run.py
```

Application should be available at `http://0.0.0.0:5000/api/`

### Configuration/Evironment Variables

Editable environment variables

- DB_DRIVER - can be `mysql | postgres |sqlite`
- DB_NAME - database name
- DB_USER - database username
- DB_PASS - database password
- DB_HOST - db location/host
- DB_PORT - database port

See other configrable options `app/config.py`

### Tests

You can run tests using

```
poetry run coverage run -m pytest tests
poetry run coverage report -m
```

The tests will also run in the github workflow.

> Unfortunately, even though the testing platform is setup, I was not able to add tests.

## Workflow Explanation

Unfortunately, due to not feeling well, I was not able to finish the entire required specs.

Not included

- Authorization Token
- Testing

Some of the API models are not implemented as well but I tried to **include the important ones that I think shows the core process for the task**.

### Challenges/Questions

- I don't use peewee so I have to learn it. (I use SQLAlchemy but I tried to follow the recommended setup as much as possible) Its fun though
- When I looked at the pages for recipe and weekly menu, I am not sure on up to what extent should I copy the structure. Maybe specify it in the requirements? (Or I think its part of the challenge)

### Available APIs

I included postman collections so you can check.

- Weekly Menu
- Recipe
- Ingredients

I was not able to add Reviews and others such as Recipe Instructions.
I think these APIs are the ones that showcases the relationships and structure between models.

- Update for ingredients included in recipe and recipe included in weekly menu is the most complex IMO.
- Other models such as Reviews and Recipe Instructions follow the same `1:M` structure hence I was supposed to do this APIs last.
- I focused first on update and create API
- There are still parts that can be refactored. I am not familiar with Peewee and its session/transaction object yet so some codes are straight forward.
- The project structure is the one I created and using in my Flask-based API projects.
- We have different coding styles and I tend to lean more on using functions rather than objects in terms of API building.

### Design thinking

There are certain ideas I took into consideration when creating the API and its structure.

- Get requests happen way more often than update/create requests so there can be some flexibility for update/create in terms of resource usage
- Some APIs like updating ingredients in a recipe is ideally done in steps so it might make sense to separate the update calls (e.g. updating instructions vs updating actual recipe descriptions.)
- Use transactions and database operations as much as possible to minimize database query.

## Final Note

I was able to put a good day of work given my schedule and health condition but its still no excuse so again, I apologize if I was not able to finish it.
If you have any questions, I am more than happy to answer them.
