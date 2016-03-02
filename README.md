lotuce2
=======

Lotuce2 Darc configs
<!-- http://www.braindeadprojects.com/blog/what/startech-pex10000sfp-and-locating-modules-in-the-linux-source/ -->
Ubuntu version:
--------------
BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img

* wget https://rcn-ee.net/deb/flasher/raring/BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img.xz
* unzx BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img
* sudo dd if=BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img of=/dev/sdX bs=1M
* default username:password is [ubuntu:temppwd]

*Expanding File System Partition On A microSD*
   1. use fdisk to delete /dev/mmcblk0p2 partition
   2. create /dev/mmcblk0p2 again using all free space
   3. resize2fs /dev/mmcblk0p2


*Loading the image to eMMc*
   1. Power down the BBB.
   2. Insert the microSD card.
   3. Hold down the BOOT button (S2) the on the BBB (This is not power button, neither reset button. S2 boot button is close to SD card).
   4. Power the board up while still holding down the BOOT button.
   5. You can release the button when all 4 LEDs are lit.
   6. Go away and have a coffee. The process is finished when all 4 LEDs are solidly lit (about an hour).
   7. Power down the BBB and remove the microSD card. Next time it is
   8. powered up it will boot into Ubuntu.
*ssh_id.pub*
   1. scp .ssh/id_rsa.pub ubuntu@192.168.7.2:/home/ubuntu/ #This should be run in shuttle
   2. cat ~/id_rsa.pub >> authorized_keys  # This should be run at beagleboneblack
   3. cat ~/id_rsa.pub >> authorized_keys2 # This should be run at beagleboneblack

*Installing utils env*
   1. git clone https://github.com/normansaez/lotuce2.git
   2. cd /home/ubuntu/lotuce2/src/env
   3. sudo make install

*Patching dbt*
   1. sudo apt-get install build-essential bison flex
   2. git clone https://github.com/normansaez/dtc.git
   3. cd dtc
   4. git reset --hard f8cb5dd94903a5cfa1609695328b8f1d5557367f
   5. wget https://patchwork.kernel.org/patch/1934471/raw/ -O dynamic-symbols.patch
   6. git apply dynamic-symbols.patch
   7. make
   8. sudo cp dtc /usr/local/bin
   9. dtc -O dtb -o <overlay filename> -b 0 -@ <source filename>

*Installing pasm*
   1. git clone https://github.com/beagleboard/am335x_pru_package.git
   2. cd am335x_pru_package/ 
   3. sudo make install
   4. cd /usr/include/
   5. sudo mkdir pruss/
   6. cd pruss/
   7. sudo cp ~/am335x_pru_package/pru_sw/app_loader/include/pruss* .
