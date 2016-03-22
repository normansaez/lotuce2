all: install
	@echo "Done"
install:
	@echo "Setup for lotuce2"
	cat environment >> /root/.bashrc
	cp sudoers /etc/sudoers
	cp pruenable /etc/init.d/pruenable 
	update-rc.d pruenable defaults
