# Instrument: Kiprim DC310S Bench Power Supply

This has been tested on the Kiprim DC310S, can see and control it through the examples/serial_DC310s.py script.

This PSU has 1 porgrammable channel

The channel is accessible with the .channeln accessor for consistency with multi-channel devices and has
relevant methods, e.g.

```
    psu = psytestbench.kiprim_dc310s.instrument.Instrument('COM5')

    psu.channel1.voltage(4.2)
    psu.channel1.on()
```

Setting and querying present values is through the same methods, with
no parameters

```
    v = psu.channel1.voltage()
    i = psu.channel1.current()
```

If you want the actual measured values, these are access through a
'measurement' attribute:

```
    measuredV = psu.measurement.channel1.voltage
    measuredI = psu.measurement.channel1.current
```

### instantiation

You only need the COM port identifier for the device. This can be discovered through the 'listResources' class method of any of the SCPI-based instrument classes however in my testing this shows up as "ASRL#::INSTR" which is not valid for easy-scpi. Instead pass "COM#" to the instantiation method, e.g.

```
   from psytestbench.kiprim_dc310s.instrument import Instrument as BenchSupply

   print(BenchSupply.listResources())
```

This method returns a tuple of all the discovered SCPI devices.

From there, either instantiate directly

```
	myPSU = BenchSupply('COM5')
```

using the appropriate identifier or set it up as part of a LabInstruments object, which will handle lazy initialization
and only connect to instruments as they are used for the first time. You can see `examples/mylab.py` and the `examples/console.py` which
uses the lab instrument collection, but is basically

```

# get the classes for the specific devices I actually have
from psytestbench.ds1000z.instrument import Instrument as OScope
from psytestbench.kiprim_dc310s.instrument import Instrument as BenchSupply
from psytestbench.utg9xx.instrument import Instrument as SigGen
from psytestbench.ut880x.instrument import Instrument as Multimeter

# init the lab instrument collection with a list of tuples
# (DEVICE_CLASS, ID)

Lab = LabInstruments([
        (OScope,        'USB0::6833::1230::DS1ZA181104442::0::INSTR'),
        (BenchSupply,   'COM5'),
        (SigGen,        'USB0::26198::2100::3568543393::0::INSTR'),
        (Multimeter,    'usb:10c4:ea80')
        ],
        autoconnect=True)
```

From there you can use the various instruments configured, e.g.

```
Lab.psu.channel1.on()
```

### sample usage

```
# some address, can get from
#  kiprim_dc310s.instrument.Instrument.listResources()
# while connected
devAddress = 'COM5'

# instantiate
pwrsupply =  kiprim_dc310s.instrument.Instrument(devAddress)

# change voltage on output channel 1
pwrsupply.channel1.voltage(3.25)

# change current limit on channel 1
pwrsupply.channel1.current(0.250)

# turn on
pwrsupply.channel1.on()

# measure output voltage/current
print(
	pwrsupply.measurement.channel1.voltage )
print(
	pwrsupply.measurement.channel.current)

pwrsupply.channel1.off()
```
