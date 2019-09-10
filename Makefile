
.PHONY: install clean

all: clean install

install: 
	bash install.sh

clean:
	sudo rm -rf /usr/local/bin/*
	sudo rm -rf /usr/local/cdcAsm
	sudo rm -rf /usr/local/miniconda3
	sudo rm "/home/cdc/Desktop/CDC Asm Client.desktop" 
	sudo rm "/home/cdc/Desktop/applet.desktop" 

