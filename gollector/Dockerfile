FROM python:3.6
COPY . .
RUN pip install richkit==1.1.1
RUN pip install psycopg2
RUN pip install pyyaml
CMD ["python3", "app.py"]