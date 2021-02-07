sudo groupadd docker
sudo gpasswd -a auo docker
sudo service docker restart

# persist the app config
docker volume create appconfig
