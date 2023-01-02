#!/bin/bash
pm2 --name pyrestia-stat start "npm run start" -- start --restart-delay 10000
sleep 7
pm2 start ./thermostat.py --restart-delay 15000

