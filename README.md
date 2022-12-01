# pyrexia-stat

A smart thermostat running on Raspberry Pi, Python, and Node.js<br>
This is the core thermostat control code that runs on the Pi.<br><br>
Features:
<li>Easily runs on 12v DC using either a USB socket (https://a.co/d/b4sLds2) or a step down module (https://a.co/d/25QVf2F)</li>
<li>Open source - easy to customized and extend</li>
<li>No cloud requirements -- can be controlled and monitored on your local WIFI</li>
<li>Available Android client https://github.com/cryptomcgrath/pyrexia-android</li>
<li>Can be controlled and monitored using REST api</li>
<li>Ideal for RV's since it runs on DC</li>
<br>
<p>Hardware:</p>
<dl>
<dt>Raspberry Pi Zero 2W</dt>
<dd>Should also work with any Raspberry Pi hardware</dd>
<dt>Supports any GPIO high and/or low triggered Relay boards</dt>
<dd>To control furnace, boiler, and/or A/C
<dd>Amazon https://a.co/d/4OUekkN</dd>
<dt>Supports DHT22 temperature sensor(s)</dt>
<dd>Using python Adafruit_DHT driver:  sudo pip3 install Adafruit_DHT</dd>
<dd>Amazon https://a.co/d/f59G0Zk</dd>
<dt>Optionally Supports Sensorpush HT.w Bluetooth temperature sensor</dt>
<dd>To read the temperature in a remote location over bluetooth</dd>
<dd>SensorPush HT.w Wireless Thermometer/Hygrometer Water-Resistant for iPhone/Android. USA Made Indoor/Outdoor Humidity/Temperature/Dewpoint/VPD Monitor/Logger. Smart Sensor with Alerts </dd>
<dd>Amazon https://a.co/d/4TTQPGd</dd>


<br>
<p>Software:</p>
  <li>Raspberry Pi OS</li>
<li>python3</li>
<li>Node.js</li>
<li>pm2</li>
<br>
  
![image](https://user-images.githubusercontent.com/5443337/192160872-86081805-009f-4953-9ad2-d1d7d47415e3.png)
