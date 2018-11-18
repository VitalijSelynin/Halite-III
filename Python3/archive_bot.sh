#!/usr/bin/env bash

set -e # Exit immediately if a command exits with a non-zero status.

current_date=$(date +%Y-%m-%d_%H:%M:%S)
attachment_folder="_comment_version"
foldername="$current_date$attachment_folder"
filename="MyBot.zip"

mkdir ../archive/$foldername


zipPath="../archive/$foldername/$filename"

zip -ur $zipPath ./hlt MyBot.py HaliteBot.py
zip -d $zipPath hlt/__pycache__/*