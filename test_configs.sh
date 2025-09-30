#!/bin/bash

source ./test_statics.sh

if [ ! -f ./xray-knife ]; then
    echo "xray-knife not found. Downloading..."
    wget https://github.com/lilendian0x00/xray-knife/releases/latest/download/Xray-knife-linux-64.zip
    unzip -o Xray-knife*.zip
    rm Xray-knife*.zip
fi


echo "combination and unique sort ..."
cat Config/all_configs.txt Config/tested_configs.txt > total.txt
sort -u total.txt > current_test_input.txt


for url in "${TEST_URLS[@]}"; do
    echo "-----------------------------------------------------"
    echo "Testing configs against: $url"
    echo "-----------------------------------------------------"
    
    if [ ! -s current_test_input.txt ]; then
        echo "No configs left to test. Stopping."
        break
    fi

    ./xray-knife http list -f current_test_input.txt --url "$url" -o passed_this_round.txt
    
    
    mv passed_this_round.txt current_test_input.txt
done


echo "-----------------------------------------------------"
if [ -s current_test_input.txt ]; then
    echo "Saving ..."
    mv current_test_input.txt Config/tested_configs.txt
else
    echo "No configs passed all tests. The results file will be empty."
    
    > Config/tested_configs.txt
    rm -f current_test_input.txt
fi


echo "Cleaning up temporary files..."
rm -f uniq.txt total.txt

echo "Testing complete."
