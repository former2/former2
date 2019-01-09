from python:3.7-slim
WORKDIR /app
RUN python -m pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy
COPY . .
ENTRYPOINT ["python", "former2.py"]