# ml-engineer-challenge

# Why FastAPI

I chose FastAPI because it is the state of art for deploying ML models and provides more features than Flask.
It provide high performance APIs that scale in production environments. It is popular and has great [documentation](https://fastapi.tiangolo.com/lo/). uvicorn serves the API with its fast ASGI webserver implementation.

Top Features:

- High performance at scale
- Fast to code with simple syntax
- Automatic (interactive) documentation generation for every route and can test all endpoints from the browser (got to http://127.0.0.1:8000/redoc or http://localhost:8000/docs)
- Easy Data parsing of path parameters & validation of string and numeric query parameters
- Modern typing of variables with pydantic

FastAPI handles all HTTP request methods or operations:

- POST: Create a new resource; most common approach for sending data
- GET: Retrieve an existing resource (read-only)
- PUT: updates exsiting resource(s)
- DELETE: Delete a resource
- PATCH: Partially update an existing resource
- OPTIONS
- HEAD
- TRACE

## Questions

- How do you use query parameters?
  FastAPI automatically treats the part of the endpoint which is not a path parameter as a query string and parses it into parameters and its values.

# FastAPI Examples

Below are some examples of APIs deployed using FastAPI. All are ready to run locally but could be packaged with Docker to make the API more portable so it can securely run on any platform. We could build a Docker image with the code and dependencies so that it can run in an isolated environment.You can use docker-compose to manage multiple containers and then deploy to serverless compute on AWS.

## Example: Bitcoin Price Predictor

This API (saved in api.py) has:

- GET method for indicating that the API is running
- POST method with /predict path for recieving input and estimating the price of Bitcoin

- Can we add an endpoint just to check that the API is up?
  Yes, the root endpoint should deliver a status message when the API is up.

We could have used async functions when creating the FastAPI predict route to enable running multiple operations in parallel and without blocking each other.

We created a Docker image for deploying the model.

### Next Steps

As a next step, we could deploy the Dockerized FastAPI appication to Docker Compose or a Kubernetes Cluster and use the Minikube/Kubernetes dashboard to visualize the deployment. Monitoring of the container can be done using Prometheus, Grafana/cadvisor to manage and visualize the performance of the containers.

We could also add a train endpoint to recieve new data and automatically re-train the model. We would use async functions to avoid collisions with the predict endpoint.

## Example: Online Market Cafe CRUD App

We created a CRUD app for an online cafe that is integrated with a sqlite database via sqlalchemy. We chose to use SQLAlchemy as the interface between Python and the database instead of directly using the sqlite driver. Using the Object Relational Mapper creates opportunity to interface with other dialects such as MySQL, Postgres, etc. with ease.

See toy_item_example.py for a comprehensive example of API that creates, lists and updates items. It defines routes for the following HTTP methods:

- GET
- POST
- PUT
- DELETE

You must use orm_mode=True in the config class to indicate that it is mapped with the ORM class of SQLAlchemy.

## Example: Named Entity Recognition with Spacy API

This API will detect named entities in input text and redact the information using Spacy models.

This API will have:

- POST route on the path '/entities' that will accept a request body containing text, model_size and model_language and will return a list of extracted entities from text and anonymized_text with the entities redacted.

### Next Topics to Explore

- Asynchronous requests to a database service
- Unit test with Github Actions that is automatically triggered on commits to main branch
- Add logging of HTTP status codes

### Resources

1. [FastAPI + Docker](https://towardsdatascience.com/how-to-deploy-a-machine-learning-model-with-fastapi-docker-and-github-actions-13374cbd638a)
2. [FastAPI + Sentiment ML API](https://towardsdatascience.com/step-by-step-approach-to-build-your-machine-learning-api-using-fast-api-21bd32f2bbdb)
3. [FastAPI + Docker 2](https://engineering.rappi.com/using-fastapi-to-deploy-machine-learning-models-cd5ed7219ea)
4. [FastAPI + Kubernetes](https://www.section.io/engineering-education/how-to-create-a-machine-learning-app-using-the-fastapi-and-deploying-it-to-the-kubernetes-cluster/)
5. [Building a microservice with FastAPI](https://developer.nvidia.com/blog/building-a-machine-learning-microservice-with-fastapi/)
6. [FastAPI + SQL Databases](https://www.tutorialspoint.com/fastapi/fastapi_sql_databases.htm)
7. [FastAPI + sqlalchemy](https://codingnomads.co/blog/python-fastapi-tutorial)
8. [FastAPI + Tutorialpoint](https://www.tutorialspoint.com/fastapi/fastapi_query_parameters.htm)
