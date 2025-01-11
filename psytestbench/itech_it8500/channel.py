"""
Created on Jan 11, 2025

@author: Matthew Collier
"""

from psytestbench.psytb.instrument.scpi import SCPIInstrument
from psytestbench.psytb.property import IndexedProperty, scpi


class Channel(IndexedProperty):
    """
    An output channel from the electronic load.

    This is a collection of utility methods to provide a handy interface
    and mask the SCPI specific stuff (e.g. when it's :CHANNEL<n>:BLAh
    vs when it's :CHANnel<n>:BASE:BLAh).

    """

    def __init__(
        self,
        chanid: int,
        parentInstrument: SCPIInstrument,
        channelProp: scpi.scpi_instrument.Property,
    ):
        super().__init__(chanid, channelProp)
        self.parentInstrument = parentInstrument

    @property
    def name(self):
        return f"CH{self.id}"

    @property
    def parent(self) -> SCPIInstrument:
        return self.parentInstrument

    def current(self, setToLimit: float = None):
        """
        Set or query the current limit.
        @param setTo: optional -- actually set to this value.

        @return: if querying (no setTo) returns current limit

        @note: to _read_ the actual current value, use the
        eload.measurement attribute (channel must be on)
        """
        return self.getSetFloat(self.prop.current, setToLimit)

    def voltage(self, setToValue: float = None):
        """
        Set or query the output voltage setting.
        @param setTo: optional -- actually set to this value.

        @return: if querying (no setTo) returns voltage set

        @note: to _read_ the actual current value, use the
        eload.measurement attribute (channel must be on)
        """
        return self.getSetFloat(self.prop.voltage, setToValue)

    def on(self, setToOn: bool = True):
        if setToOn:
            cmd = f"ON"
        else:
            cmd = f"OFF"

        return self.parent.input(cmd)

    def off(self):
        return self.on(False)

    def input(self, setToOn: bool = None):
        """
        Set or query the output state setting.
        @param setTo: optional -- actually set to this value.

        @return: if querying (no setTo) returns output state
        """
        return self.activateBoolean(self.prop.input, setToOn)

    def ramp(
        self,
        startVoltage: float,
        endVoltage: float,
        stepVoltage: float,
        stepDelaySecs: float = 0.15,
        forceChannelOn: bool = True,
    ):
        """
        Ramp voltage from start to end in stepVoltage steps.
        By default will ensure the channel is output is actually ON, though
        this may be overridden by passing forceChannelOn=False.
        """

        if forceChannelOn:
            self.voltage(startVoltage)
            self.on()

        self.parent.instrumentRole().ramp(
            self.voltage, startVoltage, endVoltage, stepVoltage, stepDelaySecs
        )
