# Twitter Profiling

This tool has been born as a Big Data project for one of my Master in Computer Enginering subjects. The aim of the tool
is to provide a service to process data from twitter profiles, giving as a result usefull insights. As the name of the subject indicates,
this tool also aims to be a Big Data workflow tool that, apart from generating those profiles as a service, is capable of storing all this processed data 
in a database. Which, once highly populated, can give really good social insights.

As has been mentioned, this tool recieves as input parameters:

- username: Twitter id of the profile that we want to process through our system.
- n_tweets: Number of tweets that we want to process of that user
- translation: In case that is not a english speaker user, we can enable this to translate all tweets to english. (Disclaimer: Eventhough it translates from varelly any language to english, it has a higher computaional cost, translated in terms of time and memory)

And outputs a twitter profile with the following information:
- Profile information: Includes followers, following, location, profile image, banner image...
- Topic Modeling: A Topic modeling task is performed to diferentiate the topics that the user usually speaks of. The preprocessing is done using a pretrained Bert model to create embedings from sentences, umap to reduce the dimentionality of those embedings to make the model perform better, and scikit DBSCAN algorithm as the unsupervised ML clustering algorithm. 
- Sentiment analysis insights: A sentiment analysis is performed to every tweet using the HuggingFace pretrained Transformers. With this, a progression lineplot and a score value for the overall sentiment are compouted.
- General Tweet statistics: Statistics regarding likes, replies, retweets and views.
- Best tweets: Most liked, viewed, retweeted and replied tweets
- Wordcloud: A word cloud of the most used meaningfull words. In orther to create this wordcloud some Cleaning technics are performed such as translating, removing stopwords, pos_tagging to get just nouns and lemathizing.
- Usage Statistics: Statistics of the usage of the platform performed by the user.

An example output of a profile can be found in example folder.

## Apache Airflow

Apache Airflow is a really powefull open-source tool for automatizing the execution of data fluxes and managing Big Data workloads.

As the subject and the project are about Big Data, I wanted to learn about a real framework to build this data pipelines. Apache Airflow is one of the most populars and is used for really important companies all arround the glove. Moreover, was a perfect fit for my project, as I wanted to create a data pipeline that to go through the following steps:

- Data mining
- Processing
- Storing
- Presenting Results

Apache works with DAG's (Directed Acyclic Graphs), which let you define particular standalone tasks and it's dependencies. With this defined, Apache Airflow manages the dependencies within your tasks

## Twitter 

## Run

```bash
  # Build custom image on top of airflow
  docker build . --tag twitter_profiling:latest 
  # Init airflow
  docker compose up airflow-init   
  # Start service
  docker compose up
```

Open your favourite browser and navigate to [http://localhost:8080](http://localhost:8080). 
There you will se the log in screen of apache airflow. The credentials to log in are the following:

```
Username: airflow
Password: airflow
```

Welcome to Airflow world! Don't be shy, you can poke arround and play a bit with the UI. 

To execute the program, you just have to go to the play button in the upper right side of the screen, and click Trigger DAG w/ config.
This will lead to you to a new page where ypou can configure the execution parameters of the program (username, number of tweets and translation).
Finally press to Trigger button to make the program run! From here you can have different Visualizations on how your DAG is doing. (Graph visualitzation, grid visualization)
Airflow is super powerfull and plenty of insights!

## Author

Quim10^-12