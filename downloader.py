import youtube_dl
import requests
import csv
from stem import Signal
from stem.control import Controller
import os
import sys
import json

# signal TOR for a new connection
def renew_connection(tor_password):
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate(password=tor_password)
    controller.signal(Signal.NEWNYM)

def download_video(config, videoId):
  ydl = youtube_dl.YoutubeDL({
    'outtmpl': os.path.dirname(os.path.realpath(__file__)) + '/videos/' + '%(id)s.%(ext)s',
    'proxy': 'socks5://127.0.0.1:9050',
    'verbose': config['verbose_logging'],
    'nocheckcertificate': True,
    # 'postprocessors': '-ss 649.044 -t 3.0'
  })
  with ydl:
    # handle looping over files
    result = ydl.extract_info(
      f'http://www.youtube.com/watch?v={videoId}',
      download=False
    )

def test_proxy(config):
  print('----------------------------------------------')
  print('Running Proxy Test')
  print('Your IP:')
  ip_test = requests.get('http://httpbin.org/ip').json()
  print(requests.get('http://httpbin.org/ip').json())
  renew_connection(config['tor_password'])
  print('Tor IP:')
  tor_ip_test = requests.Session().get('http://httpbin.org/ip', proxies={ 'http': 'socks5://127.0.0.1:9050' }).json()
  print(tor_ip_test)
  test_result = False
  if ip_test != tor_ip_test:
    print('Tor IP working correctly')
    test_result = True
  else:
    print('Your IP and Tor IP are the same: check you are running tor from commandline')

  return test_result

completed_downloads = []
videos_to_download = []

# read config
config_file = open('config.json', 'r')
config = json.load(config_file)

video_dataset_file = open('dataset.csv', 'r')
video_dataset = video_dataset_file.read().splitlines()
video_dataset_file.close()
print(f'{ len(video_dataset) } \tYouTube Videos in dataset')

completed_downloads_file = open('completed_downloads.csv', 'r')
completed_downloads = completed_downloads_file.read().splitlines()
completed_downloads_file.close()

print(f'{ len(completed_downloads) } \tCompleted downloads')

# Exclude completed downloads from video dataset (if user has re-run script)
videos_to_download = list(set(video_dataset) - set(completed_downloads))

print(videos_to_download)

if test_proxy(config) == False:
  sys.exit()

for video in videos_to_download:
  print('New Tor IP Adddress Allocated')
  renew_connection(config)

  try:
    # Download video
    download_video(config, video)
    # Remove video from download queue
    videos_to_download.remove(video)
    # Update completed downloads list
    completed_downloads.append(video)
    # Update completed downloads progress file
    with open('completed_downloads.csv', 'a') as f:
      f.write(video)
      f.write('\n')
      f.close()
  except:
    print(f'Error downloading file: {video}')
    with open('error_files.csv', 'a') as f:
      f.write(video)
      f.write('\n')
      f.close()

# Output stats
print('')
print('----------------------------------------------')
print(f'Videos Downloaded:         {len(completed_downloads)}')
print(f'Videos Failed to Download: {len(video_dataset) - len(completed_downloads)}')
if len(video_dataset) > 0 and len(completed_downloads):
  print(f'{(len(completed_downloads) / len(video_dataset) * 100)}% of dataset downloaded')