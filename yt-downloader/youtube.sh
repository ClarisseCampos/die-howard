#!/bin/bash

echo "Download"
echo "1 - Video + audio"
echo "2 - Audio only (mp3)"

read -p "Set option: " option
read -p "Set URL: " url

case $option in
    1) 
        yt-dlp \
        -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio" \
        --merge-output-format mp4 \
        "$url"
        ;;
    2)
        yt-dlp \
        -x \
        --audio-format mp3 \
        "$url"
        ;;
    *)
        echo "Invalid"
        ;;
esac 