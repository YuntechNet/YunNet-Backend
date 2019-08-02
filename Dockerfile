FROM python:3.7
ENV GIT_URL="https://gitlab.com/Zeinok/YunNet-Backend.git"
RUN apt update && apt -y upgrade && apt -y install git && \
git clone --depth=1 $GIT_URL /backend && \
cd /backend &&\
pip install pipenv &&\
pipenv --python 3.7 sync --dev

WORKDIR /backend
EXPOSE 8000
CMD ["pipenv", "run", "python", "backend.py"]
