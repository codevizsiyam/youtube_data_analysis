#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import json
import time
import isodate
import os
import boto3
import urllib.parse
import awswrangler as wr
import io

# Function to read the region data from the S3 Bucket. Requires a txt file with list region be available in S3
def get_s3_data(bucket,key):
    file=[]
    s3_client=boto3.client("s3")
    file = s3_client.get_object(Bucket=bucket, Key=key)["Body"].read().decode('utf-8')
    return (line.strip() for line in file.splitlines())



def prepare_int_values(count):
    if count == None:
        return 0
    else:
        return count


#function to parse the duration fiel to seconds
def get_duration_ms(duration):
    d= isodate.parse_duration(duration)
    return(d.total_seconds())



#function to get the trending videos for given region and page
def get_videos_list (youtube, region,next_page_token):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=50,
        pageToken=next_page_token,
        regionCode=region
    )
    response = request.execute()

    return(response)


#writes the final output for a given region into S3 object using boto3
def write_op_file (op_bucket,region,data):
    s3_op_client=boto3.client("s3")
    op_dir= "op_files/" + region
    file_name= f"{op_dir}/{region}_youtube_trending_videos_{time.strftime('%Y-%m-%d')}.csv"
    with io.StringIO() as csv_buffer:
        data.to_csv(csv_buffer, encoding='utf-8')
        response = s3_op_client.put_object(Bucket=op_bucket, Key=file_name, Body=csv_buffer.getvalue() )


#process the video response and create the dataframe after cleansing the data.
def process_data (youtube, region,next_page_token):
    
#Get most popular video information for each country code 
#and loop through all pages of the response as only 50 responses are sent at a time
    video_list=[]
    while next_page_token is not None:
        video_response=get_videos_list (youtube, region,next_page_token)
        next_page_token = video_response.get("nextPageToken", None)
        print(next_page_token)

        for video in video_response['items']:
            stats_to_keep = {'snippet': ['title','publishedAt','channelId','channelTitle','categoryId', 'description', 'tags'],
                             'contentDetails': ['duration'],
                             'statistics': ['viewCount', 'likeCount', 'dislikeCount','favouriteCount','commentCount']
                                }
            video_info = {}
            video_info['video_id'] = video['id']
            video_info['trending_date'] = time.strftime("%Y-%m-%d")
    
            for keys in stats_to_keep.keys():
                for stats in stats_to_keep[keys]:
                    try:
                        if stats == 'duration':
                            video_info[stats] = get_duration_ms(video[keys][stats])
                        elif stats == 'tags':
                            video_info[stats] = "|".join(video[keys][stats])
                        else:
                            video_info[stats] = video[keys][stats]
                    except:
                            video_info[stats]=None
                
            video_info  ['likeCount']=prepare_int_values (video_info  ['likeCount'])
            video_info  ['dislikeCount']=prepare_int_values (video_info  ['dislikeCount'])
            video_info  ['viewCount']=prepare_int_values (video_info  ['viewCount'])
            video_info  ['favouriteCount']=prepare_int_values (video_info  ['favouriteCount'])
            video_info  ['commentCount']=prepare_int_values (video_info  ['commentCount'])
        
            video_info  ['comments_disabled']=False
            video_info  ['ratings_disabled']=False
        
            if video_info  ['likeCount']==0 and video_info  ['dislikeCount']==0:
                video_info['ratings_disabled']=True
            if video_info  ['commentCount']==0:
                video_info['comments_disabled']=True

            video_list.append(video_info) 
    print(len(video_list))
    return(pd.DataFrame(video_list))

# main function which gets executed and calls all above modules
def lambda_handler(event, context):
#variable assignment
    api_service_name ="youtube"
    api_version = "v3"
    next_page_token=""
    bucket=os.environ['bucket']
    region_key=os.environ['region_key']
    api_key=os.environ['api_key']

    
    region=get_s3_data(bucket,region_key)
    
    

#perform API Call to get youtube response
    try:
        youtube = build(api_service_name,api_version,developerKey=api_key)

        for r in region:
            print('processing data for region: ' + r)
            data = process_data (youtube, r,next_page_token)
            print('writing file for region: ' + r)
            write_op_file(bucket,r,data)
        return {
            'statusCode': 200,
            'body':f'successfully completed loading data to {bucket}'
        }
    except HttpError as e:
        return {
                'statusCode': e.resp_status,
                'body':f'error occured while loading data to {bucket}: {e}'
            }

