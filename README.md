# Twitter Profiling

This tool has been born as a Big Data project for one of my Master in Computer Enginering subjects. The aim of the tool
is to provide a service to process data from twitter profiles, giving as a result usefull insights. As the name of the subject indicates,
this tool also aims to be a Big Data workflow tool that, apart from generating those profiles as a service, is capable of storing all this processed data 
in a database. Which, once highly populated, can give really good social insights.

As has been mentioned, this tool recieves as input parameters:

- **username**: Twitter id of the profile that we want to process through our system.
- **n_tweets**: Number of tweets that we want to process of that user
- **translation**: In case that is not a english speaker user, we can enable this to translate all tweets to english. (Disclaimer: Eventhough it translates from varelly any language to english, it has a higher computaional cost, translated in terms of time and memory)

And outputs a twitter profile with the following information:
- **Profile information**: Includes followers, following, location, profile image, banner image...
- **Topic Modeling**: A Topic modeling task is performed to diferentiate the topics that the user usually speaks of. The preprocessing is done using a pretrained Bert model to create embedings from sentences, umap to reduce the dimentionality of those embedings to make the model perform better, and scikit DBSCAN algorithm as the unsupervised ML clustering algorithm. 
- **Sentiment analysis insights**: A sentiment analysis is performed to every tweet using the HuggingFace pretrained Transformers. With this, a progression lineplot and a score value for the overall sentiment are compouted.
- **General Tweet statistics**: Statistics regarding likes, replies, retweets and views.
- **Best tweets**: Most liked, viewed, retweeted and replied tweets
- **Wordcloud**: A word cloud of the most used meaningfull words. In orther to create this wordcloud some Cleaning technics are performed such as translating, removing stopwords, pos_tagging to get just nouns and lemathizing.
- **Usage Statistics**: Statistics of the usage of the platform performed by the user.

An example output of a profile can be found in example folder.

## Apache Airflow

Apache Airflow is a really powefull open-source tool for automatizing the execution of data fluxes and managing Big Data workloads.

As the subject and the project are about Big Data, I wanted to learn about a real framework to build this data pipelines. Apache Airflow is one of the most populars and is used for really important companies all arround the glove. Moreover, was a perfect fit for my project, as I wanted to create a data pipeline that to go through the following steps:

- **Data mining**
- **Processing**
- **Storing**
- **Presenting Results**

Apache works with DAG's (Directed Acyclic Graphs), which let you define particular standalone tasks and it's dependencies. With those defined, Apache Airflow manages the dependencies between your tasks when executing.

## Tasks:

Let's talk a bit about the tasks that are beeing defined in our twitter_profiling DAG.

- **tweet_scraping**: Task to scrape data from a twitter profile. To do so, a really powerfull library called Snscrape is beeing used. Other options like Selenium have been explored, but resulted in a way more inefficient scraping and a lot more of dependency problems.
- **sentiment_analysis**: Performing a sentiment analysis to the text of every tweet scraperd in the previous task
- **topic_modeling**: Usage of Bert models for preprocessing to create embedings to translate text to vector numbers. usage of dimensionality reduction algorithms such as umap to reduce the embedings size to allow achieve a faster and better performance of the model. USage of DBSCAN algorithm as a unsupervised clustering algorithm to classify tweets in diferent topics. Keyword extraction technics to extract keywords for each of the topics.
- **plots**: With all the processing done start generating visual results for the report.
- **statistics**: Process a bit more the data to get overall statistics of the user.
- **build_profile**: Generation of the final report as an HTML.

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

To find our dag you have to find tweeter_profiling DAG in the list of the DAGs screen.

To execute the program, you just have to go to the play button in the upper right side of the screen, and click Trigger DAG w/ config.
This will lead to you to a new page where you can configure the execution parameters of the program (username, number of tweets and translation).
Finally press to Trigger button to make the program run! From here you can have different Visualizations on how your DAG is doing. (Graph visualitzation, grid visualization)
Airflow is super powerfull and plenty of insights!

Once execution is done, results can be found inside the **static/** folder. Also, you can connect to the DB with your favourite DB Client to check that the information has been saved in different tables.

## Project structure

- **./dags**: Folder containing the code and the definition od the airflow DAG.
- **./logs**: Folder that contains the logs of our executions in case something goes wrong and we have to audit some task logs.
- **./plugins**: Folder containing airflow plugins. For this projects, there are no plugins used.
- **./static**: Folder containing all the static files, including the reports generated for our program.
- **./examples**: Folder containing some example reports that the application produces.

## Technologies Used

- Apache Airflow
- Selenium
- snsscrape
- TheHuggingFace Transformers
- EasyNMT
- Opus-MT
- umap
- Bert Embedings
- Scikit TfidfVectorizer & DBSCAN
- wordcloud
- seaborn
- jinja2
- sqlalchemy
- sqlite
- Docker

## Development enviroment

Mac Pro: M1 chip 86x64

## Author

Quim10^-12