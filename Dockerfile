FROM python:alpine3.9
COPY . /application
WORKDIR /application
RUN pip install -r requirements.txt
ENV FLASK_APP zipline
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
EXPOSE 5000
CMD ["flask", "run"]
