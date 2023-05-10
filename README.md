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



