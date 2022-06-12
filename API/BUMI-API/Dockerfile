FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py

COPY ./model.tflite /code/model.tflite

COPY ./helper.py /code/helper.py

COPY models.py /code/models.py

COPY ./data.csv /code/data.csv

COPY ./BUMI_users_data_v2.csv /code/BUMI_users_data_v2.csv

COPY ./bumi-api-4e903-firebase-adminsdk-75pgu-b7278330a6.json /code/bumi-api-4e903-firebase-adminsdk-75pgu-b7278330a6.json

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]