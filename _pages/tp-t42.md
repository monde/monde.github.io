---
title: "ThinkPad T42"
permalink: /tp-t42/
nav_order: 6
---

**Debian Etch/Testing w/ Kernel 2.6.18**

*As of 02/25/2007*

### Index

![](/assets/images/ibm-tp-t42.png)

- [Introduction](#Introduction)
- [Hardware Configuration](#Hardware_Configuration)
- [lspci Output](#lspci_Output)
- [Kernel](#Kernel_build)
- [ipw2200 Modules](#ipw2200_Modules_build)
- [IBM Specific Kernel Modules](#IBM_Specific_Kernel_Modules)
- [Lock/Sleep/Suspend](#Lock_Sleep_Suspend)
- [Wireless](#Wireless)
- [Finger Print Reader](#Finger_Print_Reader_Biometrics "Biometrics")
- [IBM TP Buttons](#IBM_TP_Buttons)
- [USB Devices](#USB_Devices)
- [Bluetooth Settings](#Bluetooth_Settings)
- [Multimedia Playback](#Multimedia_Playback)

### Introduction

This is the Linux setup for my IBM ThinkPad T42 2373L1U that is running Debian Etch/Testing with a custom Kernel 2.6.17. I purchased this laptop in March of 2005 and I booted it to the Debian net installer CD image the first time it was powered up. This is the third ThinkPad I’ve owned, and I’ve run Linux on each. The first was a 770 with Redhat, the second was a A21M with with Redhat then Debian, and the current is this T42 with Debian and Gnome 2.14 Desktop.

I use this laptop almost daily, at home we have a WEP enabled wifi network and when I’m commuting by [ferry](./ferries/schedules/current/index.cfm) there is an open wifi network available. I use the laptop to write code, surf the web, and organize other aspects of my life. I also use a USB thumbdrive and USB SD-card reader with the laptop, and transfer files to/from it over Bluetooth with my [Nokia 6682 cellphone](./phones/6682/index.html) .

I prefer to use existing Debian packages when I’m administering Debian systems.  
h3(#Hardware\_Configuration). Hardware Configuration

This is the billing title that IBM had for this laptop:

GWH T42 FINGERPRT RDR 15 XGA 1.7 512 40 CENTRINO BG COMBO

- Pentium M 735
- 512MB RAM
- 40GB 5400rpm HDD
- 15 XGA TFT LCD
- 32MB ATI Radeon 7500
- 24×24×24x/8x CD-RW/DVD
- Intel 802.11b/g wireless(MPCI)
- Bluetooth/Modem(CDC)
- 1Gb Ethernet(LOM)
- UltraNav
- Secure Chip
- Fingerprint Reader
- 6c Li-Ion batt
- WinXP Pro

I orded the laptop with an additional battery and installed an additional 512MB of memory for 1024MB total.

### lspci Output

```
0000:00:00.0 Host bridge: Intel Corporation 82855PM Processor to I/O Controller (rev 03)
0000:00:01.0 PCI bridge: Intel Corporation 82855PM Processor to AGP Controller (rev 03)
0000:00:1d.0 USB Controller: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) USB UHCI Controller #1 (rev 01)
0000:00:1d.1 USB Controller: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) USB UHCI Controller #2 (rev 01)
0000:00:1d.2 USB Controller: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) USB UHCI Controller #3 (rev 01)
0000:00:1d.7 USB Controller: Intel Corporation 82801DB/DBM (ICH4/ICH4-M) USB2 EHCI Controller (rev 01)
0000:00:1e.0 PCI bridge: Intel Corporation 82801 Mobile PCI Bridge (rev 81)
0000:00:1f.0 ISA bridge: Intel Corporation 82801DBM (ICH4-M) LPC Interface Bridge (rev 01)
0000:00:1f.1 IDE interface: Intel Corporation 82801DBM (ICH4-M) IDE Controller (rev 01)
0000:00:1f.3 SMBus: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) SMBus Controller (rev 01)
0000:00:1f.5 Multimedia audio controller: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) AC'97 Audio Controller (rev 01)
0000:00:1f.6 Modem: Intel Corporation 82801DB/DBL/DBM (ICH4/ICH4-L/ICH4-M) AC'97 Modem Controller (rev 01)
0000:01:00.0 VGA compatible controller: ATI Technologies Inc Radeon Mobility M7 LW [Radeon Mobility 7500]
0000:02:00.0 CardBus bridge: Texas Instruments PCI4520 PC card Cardbus Controller (rev 01)
0000:02:00.1 CardBus bridge: Texas Instruments PCI4520 PC card Cardbus Controller (rev 01)
0000:02:01.0 Ethernet controller: Intel Corporation 82540EP Gigabit Ethernet Controller (Mobile) (rev 03)
0000:02:02.0 Network controller: Intel Corporation PRO/Wireless 2200BG (rev 05)
```

### Kernel

Finally! Installing the right packages in Debian now and “It Just Works” with kernel 2.6.18 … no more having to make your own kernel. You’ll need the current linux image and ipw 2200 modules, my working versions are:

- linux-image-2.6.18-3-686
- ipw2200-modules-2.6.18-3-686

The IPW module needs to load a binary driver, you can get it here:

[http://ipw2200.sourceforge.net/firmware.php](./firmware.php)

Read their directions, but I just downloaded versions 3.0 and 2.4 and extracted the contents of the tar ball to /lib/firmware

### ipw2200 Modules

See previous section.

### IBM Specific Kernel Modules

Add the following to /etc/modules :

```bash
# for ATI mobility video card
radeonfb

# nvram for tpb buttons
nvram

#speedstep-centrino for cpufreqd
speedstep-centrino

# ibm_acpi for tpb buttons
ibm_acpi

# hdaps for ibm harddrive stats
hdaps
```

### Lock/Sleep/Suspend

Just install “acpi-support” package. I haven’t tried hibernate to disk, but sleep works great.

Change /etc/acpi/events/ibm-sleepbtn to:

```
	
/etc/acpi/events/ibmsleepbtn

	
Called when the user presses the sleep button

event=ibm/hotkey 
HKEY
 00000080 00001004

#action=/etc/acpi/sleepbtn.sh

action=/etc/acpi/ibm-sleep.sh
```

And create/etc/acpi/ibm-sleep.sh

```sh
#!/bin/sh

# save system time
hwclock --systohc

# go to sleep
if [ -e /proc/acpi/sleep ]; then
    echo 3 > /proc/acpi/sleep
else
    echo -n mem > /sys/power/state
fi

# restore system time
hwclock --hctosys
```

Don’t forget:  
chmod +x /etc/acpi/ibm-sleep.sh

### Wireless

The package “network-manager” handles wireless and wired connections perfectly, “network-manager-gnome” includes an applet you can add to your tool bar.

### Finger Print Reader (Biometrics)

I don’t use it. I’ll install it when there is a supported Debian package.

### IBM TP Buttons

Install the “tpb” package.

### USB Devices

Network Manager needs udev instead of hotplug so you don’t get to automount a thumbdrive. Here’s my fstab for USB drives:

```
/dev/sda1       /media/memcard-sd       msdos   rw,user,noauto  0       0
/dev/sda1       /media/memcard-sd-msdos msdos   rw,user,noauto  0       0
/dev/sda1       /media/memcard-sd-vfat  vfat    rw,user,noauto  0       0
```

### Bluetooth Settings

Just install the “bluez-utils” package. Find out the bluetooth id of your device, and then add that to your /etc/bluetooth/rfcomm.conf . An example rfcomm.conf entry *change device to correct id* :

```
rfcomm0 {

bind yes;

        device 55:13:70:6D:0E:AB;

        channel 1;

        comment “My Phone”;

}
```

### Multimedia Playback

Assuming you are running Gnome and have the default ESD (extended sound daemon) enabled:

Make sure package “libesd-alsa0” is installed and not “libesd0”. For Flash with sound install “flashplugin-nonfree” and change Firefox/Iceweasel RC to

/etc/iceweasel/iceweaselrc

```
ICEWEASEL_DSP=“none”
```

or  
/etc/firefox/firefoxrc

```
FIREFOX_DSP=“none”
```

Also, if there is absolutely no sound be sure to run “alsaconf” and then “alsamixer” from the command line. If you fiddle with the kernel at all you often have to run alsaconf afterwards to get the sound back.

### Resources

- [IBM’s T42 2373L1U Page](./pc/support/site.wss/quickPath.do)
- [Linux on Laptops](./index.html)
- [ThinkWiki](./wiki/ThinkWiki/index.html)
- [ThinkWiki T42 2373L1U Page](./wiki/2373-L1U/index.html)
- [Wikipedia: ThinkPad](./wiki/ThinkPad/index.html)
- [//](./a></li>
  </ul>
  </div>

        	<script type=/index.html)
