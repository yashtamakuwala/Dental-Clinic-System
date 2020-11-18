From alpine:latest

RUN apk add --no-cache py-pip
RUN pip3 install --upgrade pip

COPY ./timeslot /service
WORKDIR /service

RUN pip3 install -r requirements.txt

EXPOSE 5000

WORKDIR /service/timeslot
ENTRYPOINT ["python3"]
CMD ["__init__.py"]