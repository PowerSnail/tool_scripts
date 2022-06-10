#!/bin/sh

trackers=$(curl -s https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt | grep -i "\n" | paste -sd "," -)

touch temp.conf
cat $HOME/.config/aria2/aria2.conf | rg -v "bt-tracker" > temp.conf
echo "bt-tracker=$trackers" >> temp.conf
cp -f temp.conf $HOME/.config/aria2/aria2.conf

