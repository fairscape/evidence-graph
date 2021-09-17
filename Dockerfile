FROM python:3.7

RUN apt-get install -y git

RUN pip install flask
RUN pip install pystardog
RUN pip install uwsgi
RUN pip install pyjwt
RUN pip3 install git+https://github.com/fairscape/python-auth

COPY . .

ENTRYPOINT [ "uwsgi", "--ini", "http.ini"]
