#!/bin/bash

# Define directory
videofolder="$HOME/yt-media/Video"
audiofolder="$HOME/yt-media/Audio"

# Create directories 
mkdir -p "$videofolder"
mkdir -p "$audiofolder"

echo "YOUTUBE DOWNLOADER"
echo -e "\n1 - Video + audio\n2 - Audio only (mp3)"
echo
read -p "Set option: " option
read -p "Set URL: " url

case $option in
    1) 
        yt-dlp \
        -P "$videofolder" \
        -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio" \
        --merge-output-format mp4 \
        "$url"
        ;;
    2)
        yt-dlp \
        -P "$audiofolder" \
        -x \
        --audio-format mp3 \
        "$url"
        ;;
    *)
        echo "Invalid"
        ;;
esac 