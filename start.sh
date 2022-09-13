#!/bin/bash
pm2 --name pyrestia-stat start "npm run start" -- start
nohup thermostat.py > thermostat.out

