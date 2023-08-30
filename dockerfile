FROM python:3.11.2

WORKDIR /app

COPY quiz_aws.py .
COPY questions.json .
COPY questions2.json .

RUN mkdir dist
COPY dist /app/dist

CMD ["python", "quiz_aws.py"]
