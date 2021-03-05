sudo groupadd docker
sudo gpasswd -a auo docker
sudo service docker restart

# persist the app config
docker volume rm appconfig
docker volume create appconfig

# persist the image
docker volume rm image
docker volume create image

# load gism docker image
docker load < gism-v1.5.img

# make desktop icon
path=GISM.desktop
touch $path
echo [Desktop Entry] > $path
sed -i -e '$a Name=GISM' $path
sed -i -e '$a Comment=open GISM' $path
sed -i -e '$a Exec=sh '${HOME}'/gism/run_gism.sh' $path
sed -i -e '$a Icon='${HOME}'/gism/logo.png' $path
sed -i -e '$a Terminal=true' $path
sed -i -e '$a Type=Application' $path
sed -i -e '$a Name[en_US]=GISM' $path

mv -f $path $HOME/Desktop
chmod 777 $HOME/Desktop/GISM.desktop
