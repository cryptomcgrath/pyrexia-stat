# pyrexia-stat

A smart thermostat running on Raspberry Pi, Python, and Node.js<br>
This is the core thermostat control code that runs on the Pi.<br>Once setup, can be monitored and controlled using https://github.com/cryptomcgrath/pyrexia-android<br>
<p>Hardware:</p>
<dl>
<dt>Raspberry Pi Zero 2W</dt>
<dd>Should also work with any Raspberry Pi hardware</dd>
<dt>Supports any GPIO high and/or low triggered Relay boards</dt>
<dd>To control furnace, boiler, and/or A/C
<dt>Optionally Supports Sensorpush HT.w Bluetooth temperature sensor</dt>
<dd>To read the temperature in a remote location over bluetooth</dd>
<dd>SensorPush HT.w Wireless Thermometer/Hygrometer Water-Resistant for iPhone/Android. USA Made Indoor/Outdoor Humidity/Temperature/Dewpoint/VPD Monitor/Logger. Smart Sensor with Alerts https://a.co/d/4TTQPGd</dd>
<dt>Supports DHT22 temperature sensor(s)</dt>
<dd>Using python Adafruit_DHT driver:  sudo pip3 install Adafruit_DHT</dd>
<dd>To read the temperature at the thermostat location https://a.co/d/f59G0Zk</dd>

<br>
<p>Software:</p>
  <li>Raspberry Pi OS</li>
<li>python3</li>
<li>Node.js</li>
<li>pm2</li>
<br>
  
![image](https://user-images.githubusercontent.com/5443337/192160872-86081805-009f-4953-9ad2-d1d7d47415e3.png)
