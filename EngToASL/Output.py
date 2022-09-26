import os
import subprocess
#import stanfordnlp
import stanza
from operator import itemgetter, attrgetter, methodcaller
import json
import spacy
import pafy
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc
from time import sleep
import cv2


# Create a VideoCapture object and read from input file
def playVideoHelper(cap, start_time, end_time) :
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
    # print(cap.get(cv2.CAP_PROP_POS_FRAMES))
    fps = cap.get(cv2.CAP_PROP_FPS)
    last_frame = int(fps * end_time)
    #print(last_frame, fps)
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        #print("Error opening video file")
        return

    # frame_count = 0
    # # Read until video is completed
    while(cap.isOpened()):
        
        # frame_count += 1
        # Capture frame-by-frame    
        ret, frame = cap.read()
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES) 
        #print(frame_count)
        if ret == True:
        # Display the resulting frame
            cv2.imshow('Frame', frame)
            
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            print(frame_count)
            if(frame_count==last_frame) :
                break
    
        # Break the loop
        else:
            break
    
    # # When everything done, release
    # # the video capture object
    cap.release()
    
def playVideo(properties):
    # properties : list of (url(string), start_time(int), end_time(int))
    videos = []
    for prop in properties:
        url, start_time, end_time, _ = prop
        #print(url)
        if(url!=None and start_time!=None and end_time!=None):
            video = pafy.new(url)
            best = video.getbest()
            cap = cv2.VideoCapture(best.url)
            videos.append((cap,start_time,end_time))
    for cap, start_time, end_time in videos:
        playVideoHelper(cap,start_time,end_time)
        
    cv2.destroyAllWindows()


def display(translation):
    properties = []
    for word in translation[0]:
        lemma = word['lemma'].lower()
        properties.append(getVideoDetails(lemma))
    playVideo(properties)