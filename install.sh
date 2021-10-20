#!/bin/bash
set -x
PROG_NAME=ipvanish
[ -z $XDG_CONFIG_HOME ] && echo 'error: $XDG_CONFIG_HOME is not set!' && exit 1
configs_dir="${XDG_CONFIG_HOME:-$HOME/.config}/$PROG_NAME"


sudo apt-get install -y openvpn network-manager-openvpn network-manager-openvpn-gnome
#mkdir -vp "$configs_dir" && cd "$configs_dir"
install -vd "$configs_dir"
cd "$configs_dir"
wget https://www.ipvanish.com/software/configs/configs.zip
unzip configs.zip
sudo chown -R 0600 "$configs_dir"

