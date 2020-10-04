FROM python:alpine3.9
COPY . /application
WORKDIR /application
RUN pip install -r requirements.txt
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]
