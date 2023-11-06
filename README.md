
# Background

This is the midterm project for DataTalksClub's Machine Learning Zoomcamp. The model I am training and dpeloying is the [Heart Failure prediction dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) from Kaggle. The hypothesis is that we can build a model that predicts whether or not someone has heart failure based on various clinical measurements.

As part of this project, I have a prepared a notebook to do exploratory data analysis, train several models, and select the model with the best performance. I have also created a Flask API that deploys the model as a web service.

Important files in this project:

* `notebook.ipynb`: the notebook containing the data analysis and model training
* `train.py`: the Python script to train the selected model with the tuned parameters
* `model_random_forest.bin`: the selected model with the tuned parameters, pickled using Python's `pickle` library
* `predict.py`: the Python code that bootstraps the Flask API for receiving heart failure prediction requests and performing predictions against the model
* `data/`: the directory containing the heart failure data CSV file, which I downloaded from Kaggle
* `Dockerfile`: the Dockerfile to containerize the Flask API
* `Pipfile*`: pip-related dependencies
 

# How to run the model API

## Install dependencies

Prerequesites: Python 3.10+, `pipenv`

Then install pip dependencies
```
pipenv install
```

## Run server locally

```
pipenv run gunicorn --bind 0.0.0.0:8080 predict:app
```

## Sending test data to server

Sample data

```json
{
    "age": 50,
    "sex": "M",
    "chestpaintype": "ASY",
    "restingbp": 140,
    "cholesterol": 220,
    "fastingbs": 0,
    "restingecg": "Abnormal",
    "maxhr": 200,
    "exerciseangina": "N",
    "oldpeak": 0.0,
    "st_slope": "Up"
}
```

Use a tool like postman or curl
```
curl -X 'POST' http://localhost:8080/predict -H 'Content-Type: application/json' -d '{
    "age": 50,
    "sex": "M",
    "chestpaintype": "ASY",
    "restingbp": 140,
    "cholesterol": 220,
    "fastingbs": 0,
    "restingecg": "Abnormal",
    "maxhr": 200,
    "exerciseangina": "N",
    "oldpeak": 0.0,
    "st_slope": "Up"
}'
```

## Docker

Build the Docker image:
```
docker build -t heart-disease .
```

Run the Docker container:
```
docker run -it -p 8080:8080 heart-disease:latest
```

You can issue requests directly to server running in the Docker container. See [Sending test data to server](#sending-test-data-to-server) section for an example request.

## Cloud deployment

I've deployed the model to AWS Elastic Beanstalk. You can send prediction requests to TBD.

Example:

```
```