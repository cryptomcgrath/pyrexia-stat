#!/bin/bash
pm2 --name pyrexia-node-api start "npm run start" -- start --restart-delay 10000
sleep 7
pm2 --name pyrexia-stat start ./thermostat.py --restart-delay 15000

