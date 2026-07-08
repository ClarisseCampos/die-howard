#!/bin/bash

# Definir diretorios
videofolder="$HOME/yt-media/video"
audiofolder="$HOME/yt-media/audio"

# Criar diretorios
mkdir -p "$videofolder"
mkdir -p "$audiofolder"

# Menu
echo "YOUTUBE DOWNLOADER"
echo -e "\n1 - Video + Audio\n2 - Somente audio (mp3)"
echo
read -p "Selecione a opcao: " option
read -p "URL: " url

# Controle
case $option in
    1) 
        # Audio + video (mp4)
        yt-dlp \
        -P "$videofolder" \
        -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio" \
        --merge-output-format mp4 \
        "$url"
        ;;
    2)
        # Somente audio (mp3)
        yt-dlp \
        -P "$audiofolder" \
        -x \
        --audio-format mp3 \
        "$url"
        ;;
    *)
        # opcao invalida
        echo "Invalido"
        ;;
esac