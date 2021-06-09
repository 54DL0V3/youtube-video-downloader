from typing import Counter
from pytube.extract import channel_name
from pytube import Channel
from threading import Thread


import json
import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time

VIDEOS_PER_LINK = 20

urllib3.disable_warnings(InsecureRequestWarning)

with open("youtube_urls.json", "r", encoding="UTF-8") as f:
    youtube_urls = json.load(f)

chromedriver = 'D:\Downloads\chromedriver_win32\chromedriver.exe'
# firefoxdriver = '/home/jiooum/Downloads/geckodriver-v0.29.1-linux64/geckodriver'



def download_youtube_videos():
    list_urls = youtube_urls["youtube_channel"]
    n_workers = 6
    list_workers = []
    while len(list_urls) > 0 or len(list_workers) > 0:
        if len(list_workers) >= n_workers or len(list_urls) == 0:
            time.sleep(1)
        else:
            print("Start new worker - totals: {}".format(len(list_workers)))
            channel_url = list_urls.pop()
            workers = Thread(target=download_worker, args=(channel_url,))
            workers.start()
            list_workers.append(workers)

        for worker in list_workers:
            if not worker.is_alive():
                list_workers.remove(worker)
    return

def download_worker(channel_url):
    channel = Channel(channel_url)
    channel_n = channel_name(channel_url).split("/")[-1]
    dir = os.path.join("storage", channel_n)
    if not os.path.exists(dir):
        os.mkdir(dir)

    couter = 0
    for video in channel.videos:
        print(f"Downloaded from {channel_n}: {couter} videos")
        if couter >= VIDEOS_PER_LINK:
            break

        try:
            video.streams.get_highest_resolution().download(output_path= dir)
        except Exception as e:
            print(channel_n + " - Failed to dowload highest resolution stream")
            print(e)
            try:
                video.streams.first().download(output_path= dir)
            except Exception as e:
                print(channel_n + " - Failed to dowload stream")
                print(e)
        couter += 1

# Main block
def main():
    t0 = time.time()
    download_youtube_videos()
    t1 = time.time()

    total_time = t1 - t0
    print(f'\n')
    print(f'Total time is {str(total_time)} seconds.')

if __name__ == '__main__':
    main()