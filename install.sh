#!/bin/bash
[ -z $XDG_CONFIG_HOME ] && echo 'error: $XDG_CONFIG_HOME is not set!' && exit 1
configs_dir="$XDG_CONFIG_HOME/ipvanish-cli"
logs_dir=

install -d "$configs_dir"

sudo apt-get install -y openvpn network-manager-openvpn network-manager-openvpn-gnome
mkdir -vp "$configs_dir" && cd "$configs_dir"
wget https://www.ipvanish.com/software/configs/configs.zip
unzip configs.zip

