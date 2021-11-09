#!/bin/bash

url=$1

youtube-dl \
  -i \
  --download-archive downloaded.txt \
  -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' \
  --merge-output-format mp4 \
  "$url"
  
