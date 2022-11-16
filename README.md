# bluetooth-duplex-benchmark
Test connection latency and troughput between 2 linux devices


```
sudo apt-get install python3-pip
sudo apt-get install libbluetooth-dev
sudo hciconfig hci0 piscan
sudo hciconfig hci1 piscan
```

https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory


sudo systemctl daemon-reload
sudo systemctl restart bluetooth

for X in /sys/bus/usb/devices/*; do      echo "$X";     cat "$X/idVendor" 2>/dev/null ;     cat "$X/idProduct" 2>/dev/null;     echo; done
sudo sh -c "echo 0 > /sys/bus/usb/devices/1-7/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-7/authorized"
