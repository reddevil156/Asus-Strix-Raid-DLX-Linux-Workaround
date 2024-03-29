import usb.core
import usb.util

import sys

import alsaaudio


def main():

    _dev = usb.core.find(idVendor=0x0b05, idProduct=0x180c)
    if _dev is None:
        raise ValueError("device not found")

    #usb interface blocked by usbhid / kernel driver must be blocked to get it
    usb.util.claim_interface(_dev, 4)
    #config
    _cfg = _dev[0]
    #interface
    _intf = _cfg[(4,0)]
    #endpoint
    _ep = _intf[0]

### status 0 = headphone, status 1 = loudspeaker
    _status = 1
    
    headphone = ( [0x09, 0xc5, 0x09, 0x00, 0x04, 0x03, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0a, 0x00, 0x04, 0x03, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0c, 0x00, 0x04, 0x03, 0x02, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x10, 0x00, 0x04, 0x03, 0x02, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x18, 0x00, 0x04, 0x03, 0x02, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x28, 0x00, 0x04, 0x03, 0x02, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x48, 0x00, 0x04, 0x03, 0x02, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x88, 0x00, 0x04, 0x03, 0x02, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x08, 0x00, 0x04, 0x03, 0x02, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x09, 0x00, 0x04, 0x03, 0x02, 0xff, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0b, 0x00, 0x04, 0x03, 0x02, 0xff, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0f, 0x00, 0x04, 0x03, 0x02, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x17, 0x00, 0x04, 0x03, 0x02, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x27, 0x00, 0x04, 0x03, 0x02, 0xff, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ])

    loudspeaker= ([0x09, 0xc5, 0x0f, 0x00, 0x04, 0x03, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x10, 0x00, 0x04, 0x03, 0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x12, 0x00, 0x04, 0x03, 0x08, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x16, 0x00, 0x04, 0x03, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x1e, 0x00, 0x04, 0x03, 0x08, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x2e, 0x00, 0x04, 0x03, 0x08, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x4e, 0x00, 0x04, 0x03, 0x08, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x8e, 0x00, 0x04, 0x03, 0x08, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0e, 0x00, 0x04, 0x03, 0x08, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x0f, 0x00, 0x04, 0x03, 0x08, 0xff, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x11, 0x00, 0x04, 0x03, 0x08, 0xff, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x05, 0x00, 0x04, 0x03, 0x08, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x1d, 0x00, 0x04, 0x03, 0x08, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                  [0x09, 0xc5, 0x2d, 0x00, 0x04, 0x03, 0x08, 0xff, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ])

    switch_to_speaker = [0x01, 0x03]
    switch_to_headphone = [0x02, 0x03]
    
    mixer = alsaaudio.Mixer()
    vol = mixer.getvolume()
    ledstatus = int(round(vol[0] / 8 +0.5))
    _block = False

    #loop for reading
    while True:
        try:
            #read data
            data = _dev.read(_ep.bEndpointAddress, _ep.wMaxPacketSize)
            print (data)
            #main button is pressed, sound will be switched to alternate state (headphone or loudspeaker)
            if (data[0]==5 and data[1]== 3):
                
                if (not _block):
                    _block = True
                    try:
                        if _dev.is_kernel_driver_active(0):
                            _dev.detach_kernel_driver(0)
                            usb.util.claim_interface(_dev,0)
                            _dev.detach_kernel_driver(1)
                            _dev.detach_kernel_driver(2)
                            _dev.detach_kernel_driver(3)
                            _had_driver = True
                    except:
                        continue                    
                    
                    if (_status == 0):
                        blah = _dev.ctrl_transfer(0x21, 1, 0x0800, 0x700, switch_to_speaker )
                        ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, loudspeaker[ledstatus])
                        #new status is loudspeaker
                        _status=1
                        print("switched to loudspeaker")
                    else:
                        blah = _dev.ctrl_transfer(0x21, 1, 0x0800, 0x700, switch_to_headphone)
                        ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, headphone[ledstatus])
                        #new status is headphone
                        _status = 0
                        print("switched to headphone")
                        
                    try:
                        if (_had_driver):
                            usb.util.release_interface(_dev,0)       
                            usb.util.release_interface(_dev,1)
                            usb.util.release_interface(_dev,2)
                            usb.util.release_interface(_dev,3)
                            _dev.attach_kernel_driver(0)
                    except:
                        continue
                else:
                    _block = False
                
            #volume increased        
            if (data[0] == 5 and data[1] == 5 and data [3] == 1):
                print("increase volume")
                vol = alsaaudio.Mixer().getvolume()
                print(vol)
                if (vol[0] > 97):
                    mixer.setvolume(100)
                elif (vol[0] == 0):
                    mixer.setvolume(3)
                else:
                    mixer.setvolume(int(vol[0])+3)
                
                newvol = alsaaudio.Mixer().getvolume()
                print(newvol)
                ledstatus = int(round(newvol[0] / 8 +0.5))
                
                if (_status == 0 ):
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, headphone[ledstatus])        
                else:
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, loudspeaker[ledstatus])
            
            #volume decreased
            if (data[0] == 5 and data[1] == 6 and data [3] == 1):
                print("decrease volume")
                vol = alsaaudio.Mixer().getvolume()
                print(vol)
                if (vol[0] < 3):
                    alsaaudio.Mixer().setvolume(0)
                elif (vol[0] == 100):
                    alsaaudio.Mixer().setvolume(97)
                else:
                    alsaaudio.Mixer().setvolume(int(vol[0])-3)
                
                newvol = alsaaudio.Mixer().getvolume()
                print(newvol)
                ledstatus = int(round(newvol[0] / 8 + 0.5))
                
                if (_status == 0 ):
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, headphone[ledstatus])
                else:
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, loudspeaker[ledstatus])
            
            #button for raidmode/ sonic studio is pressed
            #does not do anything, only status is repeated so usb spam is suppressed
            if (data[0] == 5 and data[1] == 2 and data [3] == 1):
                print("button pressed")
                if (_status == 0 ):
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, headphone[ledstatus])        
                else:
                    ret = _dev.ctrl_transfer(0x21, 0x09, 0x0200, 4, loudspeaker[ledstatus])
            
        except usb.core.USBError as e:
            if e.args == ('Operation timed out',):
                continue

if __name__ == '__main__':
    main()


