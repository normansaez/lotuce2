cp -v ${HOME}/lotuce2/conf/dhcpd.conf /etc/
cp -v ${HOME}/lotuce2/conf/dhclient.conf /etc/dhcp/dhclient.conf 
mkdir -p /mnt/ramcache && mount -t tmpfs -o size=4g none /mnt/ramcache/
