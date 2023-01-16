# Twitter Profiling

## Run

```bash
  # Build custom image on top of airflow
  docker build . --tag twitter_profiling:latest 
  # Init airflow
  docker compose up airflow-init   
  # Start service
  docker compose up
```

