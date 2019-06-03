FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENV NAME Ask
CMD ["python", "app.py"]
