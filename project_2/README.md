#### Exploring document model database and MapReduce paradigm

The goal was to get fumiliar with MongoDB itself and its M/R capabilities. This is a small app that displays news articles and allows one to leave comments on articles. M/R is used to compute different statistics.

Technologies:

- Nginx for reverse proxying
- Javascript (ReactJS) on frontend
- Python (Flask) on backend
- MongoDB for saving news articles and comments, and M/R jobs

To run the app:

1. Run the containers using `docker-compose up --build -d`
2. App is running on **http://localhost/**
