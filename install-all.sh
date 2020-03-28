#!/bin/sh
sudo apt-get update
echo "\n\n--------------\n\n"
sudo apt-get upgrade
echo "\n\n--------------\n\n"
sudo apt-get install portaudio19-dev
echo "\n\n--------------\n\n"
pip3 install PyAudio
echo "\n\n--------------\n\n"
pip3 install pyrebase
echo "\n\n--------------\n\n"
pip3 install 'pubnub>=4.5.0'
echo "\n\n--------------\n\n"
echo "All libs installed! - Ready for Radio Azar"