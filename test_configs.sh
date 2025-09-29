#!/bin/bash

wget https://github.com/lilendian0x00/xray-knife/releases/latest/download/Xray-knife-linux-64.zip
unzip Xray-knife*.zip
./xray-knife http list -f Config/all_configs.txt --url https://aistudio.google.com/ -o Config/tested_configs.txt
