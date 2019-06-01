import youtube_dl
import json
import requests

# access token
access_token = "" 
# get playlist data and video id
def get_data(playlistId, token):
    baseUrl  = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={playlistId}&key={token}&pageToken={pageToken}"



    pl = playlistId
    URL = baseUrl.format(playlistId= pl, pageToken = '', token= token)
    items = requests.get(url = URL).json()
    data = []
    # i = 0
    for item in items['items']:
        if item['snippet']['title']  != "Private video":
            data.append(item['contentDetails']['videoId'])


    while "nextPageToken" in items:
        URL = baseUrl.format(playlistId= pl, pageToken= items['nextPageToken'], token= token)
        items = requests.get(url = URL).json()
        for item in items['items']:
            if item['snippet']['title']  != "Private video":
                data.append(item['contentDetails']['videoId'])

    return data

import os

# Check file already downloaded or not
def file_exists(path, filename):
    try:
        for file_or_folder in os.listdir(path):
            if file_or_folder == filename:
                return True
        return False        
    except:
        return False
    
    
import sys
# Downloading the file from playlist
with open('playlist.json') as json_file:
    # Check validation
    if access_token == "":
        sys.exit("access_token required")

    jsonData = json.load(json_file)
    # print(jsonData)
    for classData in jsonData:
        print(classData)
        for course in jsonData[classData]:
            print(course)
            data = get_data(jsonData[classData][course], access_token)
            print(data)
            for p in data:
                # print(p)/
                p = p
                if file_exists('file_path/'+classData+'/'+course+'/', p+'.mp4'):
                    print(p+'.mp4 already exsit')
                    continue
                print('downloading.....'+p)
                ydl_opts = {'outtmpl': 'file_path/'+classData+'/'+course+'/'+p+'.mp4'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(['https://www.youtube.com/watch?v='+p])
            print(course, ' Done')
        print(classData, ' Done')


