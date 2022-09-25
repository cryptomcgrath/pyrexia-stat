#!/bin/bash
pm2 --name pyrestia-stat start "npm run start" -- start
sleep 7
pm2 start ./thermostat.py 

