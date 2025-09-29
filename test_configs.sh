#!/bin/bash

wget https://github.com/lilendian0x00/xray-knife/releases/latest/download/Xray-knife-linux-64.zip
unzip Xray-knife*.zip

cat Config/all_configs.txt Config/tested_configs.txt > total.txt
./xray-knife http list -f total.txt --url https://aistudio.google.com/ -o Config/tested_configs.txt
