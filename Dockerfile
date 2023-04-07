FROM python:3.9  

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ARG fullchain

ARG privkey

COPY fullchain /code/

COPY privkey /code/

COPY ./ /code/


CMD ["python", "main.py"]