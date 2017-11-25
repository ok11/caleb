FROM python:alpine

EXPOSE 8080:8080

WORKDIR /home/ok11/workspace/caleb

RUN pip install pipenv==8.1.2 # latest pipenv has a bug

COPY ./Pipfile ./Pipfile
RUN pipenv install --dev --system --verbose

COPY app/ app/
COPY migrations/ migrations/
COPY ./caleb.py ./caleb.py

#ENV DATABASE_URL ./db/dev.db

#RUN python migrate.py db migrate
#RUN python migrate.py db upgrade

#RUN pip install -r requirements.txt

CMD [ "python", "./caleb.py", "run" ]
