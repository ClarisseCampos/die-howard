#!/bin/bash

# Verify updates
pipx upgrade yt-dlp >/dev/null 2>&1 || true

# Define directory
videofolder="/home/clarisse/yt-media/Video"
audiofolder="/home/clarisse/yt-media/Audio"

echo "YOUTUBE DOWNLOADER"

echo -e "\n1 - Video + audio\n2 - Audio only (mp3)\n3 - Change download directory"

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