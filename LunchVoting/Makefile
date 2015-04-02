
all:
	@echo "make install"

install:
	crontab -l > crontab.bkp
	sudo cp vflv.bash /usr/local/bin/.
	echo "@reboot /usr/local/bin/vflv.bash" >> crontab.bkp
	crontab crontab.bkp	
	rm crontab.bkp

clean:
	rm -f crontab.bkp

