#!/bin/bash
oldpwd=$(pwd)
sudo apt-get install -y openvpn network-manager-openvpn network-manager-openvpn-gnome
mkdir configs && cd configs
wget https://www.ipvanish.com/software/configs/configs.zip
unzip configs.zip

sudo apt-get install -y openvpn network-manager-openvpn network-manager-openvpn-gnome
