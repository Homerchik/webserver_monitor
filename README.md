# Overview
This project provides two services:
- metrics publisher - periodically checks webservices described in 
config and pushes messages with information about their availability
 to Kafka `metrics` theme;
- metrics consumer - subscribes to theme `metrics` in Kafka and periodically
writes metrics, recieved from Kafka, to PostgreSQL;

# Testing and Running 
To run tests, you need just to run pytest, after fetching all python dependencies
```
pytest
```

To run metrics publisher you need
```
python3 -m src.main.prod_runner --config-dir configs
```
where configs is directory with config-files for publisher

To run metrics consumer you need
```
python3 -m src.main.cons_runner --config-dir configs
```
where configs is directory with config-files for consumer


# Configuring
## Metrics publisher
```
#minimal set of kafka settings
# any other settings supported by kafka.python can be set here
kafka:
  bootstrap_servers: ["localhost:9092"] 

#specific settings for producers
kafka_prod:
```

## Metrics consumer
```
# minimal set of settings for PG
# any other settings supported by psycopg.connect can be set here
postgresql:
  host: 0.0.0.0 #hostname or IP
  port: 5432
  user: postgres # user with access  to db
  password: 1
  dbname: metricdb #dbname

#minimal set of kafka settings
# any other settings supported by kafka.python can be set here
kafka:
  bootstrap_servers: ["localhost:9092"] 

#specific settings for consumers
kafka_cons:
  auto_offset_reset: latest
```

## Logging
To configure logging just put logging.yaml file near the config.yaml and pass 
their destination during service run. Any logging options supported by
standard python logging lib is available.

## Services list
Below are settings for monitoring two services 
- localhost and page my_fancy_page on it, with regexp validation on page content
- my.webservice.com with two web-resources get_book and get_stone API w/o 
response validation
```
monitoring:
  localhost:
    my_fancy_page:
      regexp: "Main page"
  my.webservice.com:
    get_book:
      regexp: 
    get_stone:
      regexp  
```

# Message format
To kafka publisher messages pushed as
- key - hostname, with all `.` replaced with `_`
- value - dict with keys `ts`, `hostname`, `page`, `status`, `latency`, `regex_valid`

In postgres messages saved as:
- table name - hostname, where all `.` replaced with `_`
- fields `ts`, `hostname`, `page`, `status`, `latency`, `regex_valid`
