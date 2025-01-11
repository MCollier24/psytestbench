"""
Created on Jan 11, 2025

@author: Matthew Collier
"""

from psytestbench.psytb.instrument.instrument import InstrumentAPIPackage
from psytestbench.psytb.instrument.scpi import SCPIInstrument

from psytestbench.kiprim_dc310s.channel import Channel


class MeasuredChannel:
    def __init__(self, parentMeasurement, forChannel: Channel):
        self.measParent = parentMeasurement
        self.chan = forChannel

    @property
    def current(self):
        return self.measParent.getMeasurementOf("CURRent", self.chan)

    @property
    def voltage(self):
        return self.measParent.getMeasurementOf("VOLTage", self.chan)


class Measurement(InstrumentAPIPackage):

    def __init__(self, parentInstrument: SCPIInstrument, channelsList: list = None):
        super().__init__(parentInstrument)
        if channelsList and len(channelsList):
            count = 1
            for chan in channelsList:
                name = f"channel{count}"
                setattr(self, name, MeasuredChannel(self, chan))
                count += 1

    def getMeasurementOf(self, itemName: str, forChannel: Channel = None):

        q = f"MEASure:{itemName}?"
        val = 0
        try:
            val = float(self.instrument.query(q))
        except:
            pass

        return val

    def current(self, forChannel: Channel = None):
        return self.getMeasurementOf("CURRent", forChannel)

    def voltage(self, forChannel: Channel = None):
        return self.getMeasurementOf("VOLTage", forChannel)
