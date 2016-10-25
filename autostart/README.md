autostart a python script for Raspberry on bootup
====
http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/

https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units

systemd is a software suite for central management and configuration of a Linux system and aims to replace other popular tools that previously fulfilled this role.  

1 Write a python script
===

2 Create a unit file
===
with : sudo nano /lib/systemd/system/hello_world.service

[Unit]  
Description=Litener to RT5100 NIDEK  
After=multi-user.target  

[Service]  
Type=idle  
ExecStart=/usr/bin/python /home/pi/rt5100rs232/autostart/hello_world.py  
or  
ExecStart=/usr/bin/python /home/pi/rt5100rs232/autostart/hello_world.py > /home/pi/myscript.log 2>&1  
[Install]  
WantedBy=multi-user.target  

3 Change permissions 
====
sudo chmod 644 /lib/systemd/system/hello_world.service

4 Configure systemd
====
sudo systemctl daemon-reload

5 Test if it works
===
sudo systemctl start hello_world (.service facultatif)


6 Look in 
===
tail -f /var/log/syslog

You should see something like that:  
Sep 28 15:24:17 raspberrypi systemd[1]: Starting RT5100 RS232 listener...  
Sep 28 15:24:17 raspberrypi systemd[1]: Started RT5100 RS232 listener.  

ou 

sudo systemctl status hello_world.service..
which give  
● listener_rt5100.service - RT5100 RS232 listener  
   Loaded: loaded (/lib/systemd/system/listener_rt5100.service; disabled)  
   Active: active (running) since Wed 2016-09-28 15:24:17 NCT; 1min 24s ago  
 Main PID: 1076 (python)  
   CGroup: /system.slice/listener_rt5100.service  
           └─1076 /usr/bin/python listener_rt5100.py  

Sep 28 15:24:17 raspberrypi systemd[1]: Started RT5100 RS232 listener.


7 Si ca marche
===
sudo systemctl enable hello_world

8 Reboot
===
sudo reboot


Change time zone for Raspberry
====
