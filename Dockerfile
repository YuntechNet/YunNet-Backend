FROM python:3.7
WORKDIR /backend
EXPOSE 8000
ADD https://gitlab.com/Zeinok/yunnet-backend/-/archive/dev/yunnet-backend-dev.tar.gz /tmp
RUN tar -xzf /tmp/yunnet-backend-dev.tar.gz -C /backend --strip-components=1 && ls /backend
RUN pip install pipenv && \
pipenv --python 3.7 sync --dev
CMD ["pipenv", "run", "gunicorn", "myapp:app", "--bind 0.0.0.0:8000", "--worker-class sanic.worker.GunicornWorker"]
