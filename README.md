# Asus Strix Raid DLX-Linux-Workaround
Asus Strix Raid DLX Soundcard reverse engineering for using the included control box under linux

## 1. Introduction

I own a Asus Soundcard named Strix Raid DLX which comes with a control box. Thix box is intended to be placed on the desk and you can plug in your headphones easily.
With a button you can switch between headphones (connected to the box) and speaker (directly connected to the soundcard). You can change also the volume with a rotation of the button.

Since the box doesn't work under linux and changing the output is not that easy I tried to reverse engineer the hole process. This was my first time to do so and there might be
some better methods for it but I was successful so I want to share my knowledge.

The soundcard uses a Asmedia USB controller chip where the soundchip and the control box are internally connected. 
On button press a microcontroller inside the box starts an interrupt on the usb bus with a special request. The controller on the soundcard analyses the request and sends a response back.

## 2. USB request to change led states on control box

The control box itself can only change the state of the leds and cannot switch the relais between headphone and speaker.

There exist 13 leds for the volume which results in 14 different states: all off (volume 0% / volume off) and 1-13 leds on for increased volume.
Also there are 2 leds which show if headphone or speaker are active. That results in 2 different states: (on / off or off / on)

To control the LEDs on the box the following USB request is used:

bmRequestType :0x21
bRequest: 0x09
wValue: 0x0200
wIndex: 0x0004
wLength: 16

The data block consists of 16 bytes and looks like this:

09 c5 27 00 04 03 02 ff 1f 00 00 00 00 00 00 00

Byte 7 changes the state for the status LED (headphone or speaker). 02 represents headphones, 08 represents speaker

Bytes 3, 8 and 9 represent the state of the volume control (how many leds are on)

- state of status led remains on headphones, volume led change from zero two 13

09 c5 09 00 04 03 02 00 00 00 00 00 00 00 00 00		- headphone led on, zero volume leds
09 c5 0a 00 04 03 02 01 00 00 00 00 00 00 00 00
09 c5 0c 00 04 03 02 03 00 00 00 00 00 00 00 00
09 c5 10 00 04 03 02 07 00 00 00 00 00 00 00 00
09 c5 18 00 04 03 02 0f 00 00 00 00 00 00 00 00
09 c5 28 00 04 03 02 1f 00 00 00 00 00 00 00 00
09 c5 48 00 04 03 02 3f 00 00 00 00 00 00 00 00
09 c5 88 00 04 03 02 7f 00 00 00 00 00 00 00 00
09 c5 08 00 04 03 02 ff 00 00 00 00 00 00 00 00
09 c5 09 00 04 03 02 ff 01 00 00 00 00 00 00 00
09 c5 0b 00 04 03 02 ff 03 00 00 00 00 00 00 00
09 c5 0f 00 04 03 02 ff 07 00 00 00 00 00 00 00
09 c5 17 00 04 03 02 ff 0f 00 00 00 00 00 00 00
09 c5 27 00 04 03 02 ff 1f 00 00 00 00 00 00 00		- headphone led on, all 13 volume leds on

- state of status led remains on speaker, volume led change from zero two 13
09 c5 0f 00 04 03 08 00 00 00 00 00 00 00 00 00		- speaker led on, zero volume leds
09 c5 10 00 04 03 08 01 00 00 00 00 00 00 00 00
09 c5 12 00 04 03 08 03 00 00 00 00 00 00 00 00
09 c5 16 00 04 03 08 07 00 00 00 00 00 00 00 00
09 c5 1e 00 04 03 08 0f 00 00 00 00 00 00 00 00
09 c5 2e 00 04 03 08 1f 00 00 00 00 00 00 00 00
09 c5 4e 00 04 03 08 3f 00 00 00 00 00 00 00 00
09 c5 8e 00 04 03 08 7f 00 00 00 00 00 00 00 00
09 c5 0e 00 04 03 08 ff 00 00 00 00 00 00 00 00
09 c5 0f 00 04 03 08 ff 01 00 00 00 00 00 00 00
09 c5 11 00 04 03 08 ff 03 00 00 00 00 00 00 00
09 c5 15 00 04 03 08 ff 07 00 00 00 00 00 00 00
09 c5 1d 00 04 03 08 ff 0f 00 00 00 00 00 00 00
09 c5 2d 00 04 03 08 ff 1f 00 00 00 00 00 00 00		- speaker led on, all 13 volume leds on

## 3. USB Reuqest to change sound output

To change the sound output the following USB request is used:

bmRequestType :0x21
bRequest: 0x01
wValue: 0x0800
wIndex: 0x0700
wLength: 2

The data block consists of 2 bytes and looks like this:

switching relais from headphone to speaker:
01 03
switching relais from speaker to headphone
02 03

## 4. Generated USB interrupts from control box

If the button is pressed or the volume is changed the box sends some data and waits for an answer. This data will be resend
until an answer with a new state is received (see part #2).

Pressing middle button for switching relais:
5 5 0 3 1 1 3 0 1 1 1 1 1 0 0 0
Rotating button increasing volume:
5 5 0 1 1 3 3 0 1 1 1 1 1 0 0 0
Rotating button decreasing volume:
5 6 0 1 1 4 3 0 1 1 1 1 1 0 0 0
button press on raid mode button:
5 2 0 1 1 0 4 0 1 1 1 1 1 0 0 0

## 5. Prerequisites

I don't have any experience in programming a kernel driver so I decided to go the easiest way for me and write a python script with
the help of the pyusb library.

Because the control box is attached to the Asmedia USB Hub and is not correctly recognized through linux the kernel module usbhid is 
automatically loaded. You have to unbind it to send commands to the control box itself or you will get a "resource busy" error code.

The script is tested with python3.7, i cannot say if it works with other versions too.
To change the volume I use the pyalsaaudio library.

```bash
pip3.7 install pyusb
pip3.7 install pyalsaaudio

```

## 6. Usage

Actual the python script must be run under root. It should be possible to get it working without root using udev rules but I don't have
the time to check this out.

Changing the output requires to send a command to a usb interface which is in use by the usb audio driver module. In my script I deattach
it from the kernel, send my message and reattach it. Don't know if there is a better way.

## 7. Todo:

My time is limited but I want to:

usage without root
systemd service for startup
RaidMode Button does nothing
Save last state of the box and read it out at startup


## 8. Contribution:

Please feel free to use all of the informations above



