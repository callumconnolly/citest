FROM python:latest

RUN mkdir "c:\\code"

COPY requirements.txt "c:\\code"

COPY scrape.py "c:\\code"

RUN pip install -r "c:\\code\\requirements.txt"

CMD ["python", "c:\\code\\scrape.py"]

