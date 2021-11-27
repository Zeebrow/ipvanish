
# ipvanish config files are named like
# ipvanish-US-Atlanta-atl-b42.ovpn
# where the city name can be more than one word,
# split by a hyphen `-'

# prints full path: find "$IPVANISH_CONFIG_DIR" -maxdepth 1 -type f 
# outputs file only: ls -1 "$IPVANISH_CONFIG_DIR"

[ -n "$IPVANISH_CONFIG_DIR" ] && IPVANISH_CONFIG_DIR="$HOME/.config/ipvanish/configs/"

# complete "$ ipvanish "
function _ipv_complete_options() {
  local ipv_base_options=('connect' 'disconnect' 'list')
  [ "${#COMP_WORDS[@]}" -gt 2 ] && return
  COMPREPLY=($(compgen -W "${ipv_base_options[*]}" "${COMP_WORDS[1]}"))
}

# complete "ipvanish connect "
function _ipv_complete_connect () {
  let local _CLI_ENTRY_POSITION=2
  echo "$_CLI_ENTRY_POSITION"
  echo "$((_CLI_ENTRY_POSITION + 1))"

  return

  local ipv_conn_filter='^ipvanish'
  local connections=(`nmcli -t -f 'NAME' c s | grep "$ipv_conn_marker"`)
  [ "${#COMP_WORDS[@]}" -gt 3 ] && return

  for cfg_file in `ls -1 "$IPVANISH_CONFIG_DIR" | grep '^ipvanish-.*\.ovpn$'`; do
    cfg_files+=("$cfg_file")
  done
  COMPREPLY=($(compgen -W "${cfg_files[*]}" "${COMP_WORDS[2]}"))
}

function _ipv_deboog () {
  echo ""
  echo "COMP_CWORD : $COMP_CWORD"
  echo "COMP_WORDS : ${COMP_WORDS[*]}"
  echo "COMP_LINE : $COMP_LINE"
  echo "COMP_POINT : $COMP_POINT"
}


complete -F _ipv_complete_options ipvanish
#debug
#complete -F _ipv_deboog ipvanish
complete -F _ipv_complete_connect 'ipvanish connect'
