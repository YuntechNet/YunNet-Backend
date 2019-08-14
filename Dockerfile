FROM python:3.7
WORKDIR /backend
EXPOSE 8000
COPY ./ /backend/
RUN pip install pipenv &&\
pipenv --python 3.7 sync --dev
CMD ["pipenv", "run", "python", "backend.py"]
