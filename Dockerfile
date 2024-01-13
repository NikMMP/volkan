FROM python:3.11
ENV APP_HOME /docker_folder
WORKDIR $APP_HOME
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python","main.py"]