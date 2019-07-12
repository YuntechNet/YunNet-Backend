FROM python:3.7-alpine
ENV GIT_URL="https://gitlab.com/Zeinok/YunNet-Backend.git"
RUN apk update && apk upgrade && apk add --no-cache build-base git && \
git clone --depth=1 $GIT_URL /backend && \
cd /backend &&\
pip install pipenv &&\
pipenv --python 3.7 sync --dev

WORKDIR /backend
EXPOSE 8000
CMD ["pipenv", "run", "python", "backend.py"]

