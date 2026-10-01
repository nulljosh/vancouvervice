#!/bin/sh
# Keeps the 16 GB Mac alive while Unreal runs. Prints one line per event, so it works as a Claude Code Monitor.
#   sh unreal/guard.sh
# Under pressure (free RAM < 20% or swap > 88%) it acts: unloads Ollama models and keeps the Bonsai server down.
# It never touches other sessions' work (QEMU, Chrome, Python) or the editor itself; it says so and leaves that call to us.
i=0; last=ok
while true; do
  free=$(memory_pressure 2>/dev/null | awk '/free percentage/ {gsub("%","",$5); print $5}')
  swap=$(sysctl -n vm.swapusage | awk '{gsub("M","",$3); gsub("M","",$6); printf "%d", $6*100/$3}')
  e=$(pgrep -x UnrealEditor | head -1)
  ue=$([ -n "$e" ] && footprint "$e" 2>/dev/null | awk '/Footprint:/{for(i=1;i<NF;i++) if($i=="Footprint:"){v=$(i+1); if($(i+2)=="MB")v=v/1024; printf "%.1f",v}}' || echo off)
  therm=$(pmset -g therm 2>/dev/null | grep -i -E "level *= *[1-9]" | head -1)
  hog=$(top -l 1 -o mem -n 4 -stats command,mem 2>/dev/null | tail -3 | tr -s ' ' | paste -sd ',' -)
  line="free ${free}% swap ${swap}% unreal ${ue}GB | ${hog}"
  state=ok
  { [ "${free:-100}" -lt 20 ] || [ "${swap:-0}" -gt 88 ]; } && state=pressure
  [ -n "$therm" ] && state="thermal: $therm"
  if [ "$state" != ok ]; then
    acted=""
    for m in $(ollama ps 2>/dev/null | awk 'NR>1 {print $1}'); do ollama stop "$m" >/dev/null 2>&1 && acted="$acted ollama:$m"; done
    if pgrep -f bonsai-2 >/dev/null; then
      launchctl bootout "gui/$(id -u)/com.joshua.bonsai" 2>/dev/null; pkill -f bonsai-2 && acted="$acted bonsai"
    fi
    [ "$state" != "$last" ] || [ -n "$acted" ] && echo "ALERT $state | $line | freed:${acted:- nothing left to free safely}"
  elif [ "$last" != ok ]; then
    echo "RECOVERED | $line"
  fi
  [ $((i % 20)) -eq 0 ] && echo "health | $line"
  last=$state; i=$((i + 1)); sleep 30
done
