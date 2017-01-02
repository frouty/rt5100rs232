* Install raspbian image
sudo dd bs=4M if=raspbianxxx.img of=/dev/sdx
 
* config keyboard
Connection sur le terminal :
login: pi
password : raspbian 
attention par défaut clavier qwerty
configuration du clavier:
sudo raspi-config
internationalisaton option 
option configure_keyboard
garder Generic 105-key (intl) PC
french 
the default for the keyboar layout.

* aptitude install 
sudo aptitude install zsh git tree

* ssh key dans github
https://help.github.com/articles/checking-for-existing-ssh-keys/

* Oh-my-zsh
git clone git@github.com:frouty/oh-my-zsh.git

create a new zsh config file
cp /home/pi/.oh-my-zsh/templates/zshrc.zsh-template /home/pi/.zshrc
chsh -s /bin/zsh

se reloguer.


* installer le service
git clone git@github.com:frouty/rt5100rs232.git

le script du service est : 
TODO
lancer le service : TODO
cp le service /lib/systemd/system/myscript.service
sudo chmod 644 /lib/systemd/system/myscript.service

* verifier que la connection ssh sur le raspberry marche.

* backup de la carte SD
sudo dd bs=4M if=/dev/sdx | gzip > rasbian.img.gz
to restore
gunzip --stdout rasbian.img.gz | sudo dd bs=4M of=/dev/sdx