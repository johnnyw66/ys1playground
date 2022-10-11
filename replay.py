#—————YardStick_InstantReplay_SimpleVersion.py ----------#
# @Ficti0n
# http://consolecowboys.com


from rflib import *
import time
import re
import bitstring
import datetime

print("Listening for them signals in ASK")
d = RfCat()
d.setFreq(433.92e6)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(4800)
#d.setMaxPower()
d.lowball()
while True:
    #-----------Start Capture 1 Transmission ----------#
    capture = ""
    print("**sniffing**....")
    while (1):
        try:
            y, z = d.RFrecv()
            filtered=capture = y.hex()
            filtered = filtered.replace("ffffffff","")
            filtered = filtered.replace("00000000","")

            if (len(filtered) < 128):
                capture = ""
            else:
                capture = filtered
                print(f"{datetime.datetime.now()}: {capture}")
            #print("redundant", redund)
            #if (len(redund) < 32):
            #    capture = ""
            #else:
            #    print(capture)
            #if (capture[-4:] == "ffff"):
            #    capture = ""

        except KeyboardInterrupt:
            break

        except ChipconUsbTimeoutException:
            print("ChipconUsbTimeoutException")
            pass
        if capture:
            break

    print("Transmitting!",capture)
    time.sleep(5)

    #Parse Hex from the capture by reducing 0's
    binary = bin(int(capture,16))[2:]

    formatted = bitstring.BitArray(bin=(binary)).tobytes()
    try:
        while True:
            print("RFxmit",formatted)
            d.RFxmit(formatted)
            break
    except ChipconUsbTimeoutException:
        print("ChipconUsbTimeoutException on RFxmit")

    print('Transmission Complete')
