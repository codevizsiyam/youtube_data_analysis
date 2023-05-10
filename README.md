## Project to analyse trending youtube videos by region - Siyamala Subramanian

## Overview
In this project, we are going to collect the trending youtube videos data from youtube API and create csv datasets for each day by region automatically. It will also combine these daily files into a single cumulative dataset per region and analyze data to over the time, sentiment analysis. we will also create visualizations using either quicksight or tableau for this dataset.

## Acknowledgement
I started this project to build my own kaggle dataset similar to the existing popular kaggle dataset (https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset), hence I have kept the output csv structure similar to youtube-trending-video-dataset. This Project uses Youtube API to get this trending video data. 

## Goals
Data Extraction     - Build Python scripts to extract data from youtube API
Automate Extraction - Build Lambda function to execute the script on schedule
ETL                 - Process the data (from s3 buckets) generated from Lambda to generate a cumulative dataset
Analysis            - Perform data analysis to answer business questions provided in overview.
Visualization       - Build visualizations using both Quicksight and Tableau public to compare and contrast the process in both tools to achieve same end result.

## Detailed Steps
# Step 0: Pre-requisite
In this project we are interested in the trending videos that are hosted in youtube. Hence we need to have few pre-requisites completed to access the Youtube API. We need to create a project in google developer console and obtain API KEY. Detailed steps is available in https://developers.google.com/youtube/v3/getting-started#before-you-start

# Step 1: Setting Up the AWS Lambda function

1.  Install the Google API Client Library for Python to use the YouTube Data API.
    pip install google-api-python-client -t layer/
2.  Zip this layer folder as layer.zip
3.  Create the python script (that will become the lambda function) in your local saying using Jupyter notebook. 
    Python script for this project is available in data_extraction_script.py
4.  Use Download all and use .py to download the notebook as .py extension.
5.  Rename the .py file as "lambda_function.py"
6.  zip the file lambda_function.py.
7.  Now, Go to the Lambda service in the AWS Management Console and create a new Lambda function. 
8.  Choose “Author from scratch,” name the function, and select Python as the runtime.
9.  Use Upload From option and upload the zipped lambda_function.py 
10. Add the layer.zip file as the layer for the lambda fucntion
11. Set the environment variables to provide the s3 bucket name for ip and op files, API Key under configuration/Environment Variables

# Step 2: Test the lambda function
Since this python script does not require any other input parameters than what is configured in Step 1, you can use the Test function with {} empty JSON to run a test. You should get output response of 200 if there is no error and also the S3 Output buckets should contain the csv for given day in their own region sub folders.

# Step 3: Automation
Configure a Trigger for the function, choose the EventBridge as trigger source and create a new rule based on "Schedule Expression" and set up the cron expression to the required frequency. This will allow the lambda function to be triggered automatically at a set interval.

# Optional Step - API Gateway
You could create a REST API and add a POST method to the root resource and integrate the Lambda function. We could have a simple web app that can invoke this API to create this dataset in adhoc fashion. API Gateway will require API Key, Usage plan to be setup and it can be tested using apps like Postman by passing the x-api-key as header parameter.

# Step 4: ETL --- Will be added soon

