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
sudo systemctl enable hello_world.service

5 Reboot
===
sudo reboot

6 Look in 
===
tail -f /var/log/system.log

ou 

sudo systemctl status hello_world.service

Change time zone for Raspberry
====
