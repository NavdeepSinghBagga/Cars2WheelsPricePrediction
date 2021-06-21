FROM python:3.8.3

COPY . /app

WORKDIR /app

RUN pip install -r reqq.txt

EXPOSE 5001

# run the command
CMD ["python","app.py"]