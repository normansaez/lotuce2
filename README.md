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
   6. Go away and have a coffee. The process is finished when all 4 LEDs are solidly lit.
   7. Power down the BBB and remove the microSD card. Next time it is
   8. powered up it will boot into Ubuntu.

