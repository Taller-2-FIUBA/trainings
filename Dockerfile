FROM python:3.11

WORKDIR /user/src/trainings

COPY . .
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

WORKDIR /user/src/trainings

ENTRYPOINT [ "uvicorn", "trainings.main:app", "--host", "0.0.0.0", "--port=8003", "--reload" ]
