# trainings

[![codecov](https://codecov.io/gh/Taller-2-FIUBA/trainings/branch/main/graph/badge.svg?token=WQwxO53hR1)](https://codecov.io/gh/Taller-2-FIUBA/trainings)

Service to interact with trainings

## Virtual environment

Set up:

```bash
sudo apt install python3.11 python3.11-venv
python3.11 -m venv .
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt -r dev-requirements.txt
```

## FastAPI

```bash
uvicorn main:app --reload
```

## Tests

```bash
tox
```

## Docker

Building docker image:

```bash
docker build . --tag fiufit/trainings:latest
```

Then run the container:

```bash
docker run --rm -p 8080:80 --name CONTAINER_NAME fiufit/trainings:latest
```

Notice `--rm` tells docker to remove the container after exists, and
`-p 8080:80` maps the port 80 in the container to the port 8080 in the host.

## Using the image in a local K8s cluster (k3d)

```bash
k3d image import fiufit/trainings:latest --cluster=taller2
```
