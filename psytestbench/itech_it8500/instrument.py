"""
Created on Jan 11, 2025

@author: Matthew Collier
"""

from psytestbench.psytb.instrument.scpi import SCPIInstrument
import psytestbench.psytb.instrument_roles as role
from psytestbench.it8500.channel import Channel

from psytestbench.it8500.measurement import Measurement


class Instrument(SCPIInstrument):
    """
    This ELOAD has 1 channels

    Single channel is accessible with the .channeln accessor for consistency and has
    relevant methods, e.g.

       eload = psytestbench.it8500.instrument.Instrument('USB0::1155 ... ')

       eload.channel1.voltage(4.2)
       eload.channel1.on()

    Setting and querying present values is through the same methods, with
    no parameters
       v = eload.channel1.voltage()
       i = eload.channel1.current()

    If you want the actual measured values, these are access through a
    'measurement' attribute:

       measuredV = eload.measurement.channel1.voltage
       measuredI = eload.measurement.channel1.current
    """

    Role = role.ElectronicLoad

    def __init__(
        self,
        port=None,
        port_match=True,
        backend="",
        handshake=False,
        arg_separator=",",
        **resource_params,
    ):
        """

        @param port: The name of the port to connect to. [Default: None]
        @param backend: The pyvisa backend to use for communication. [Default: '']
        @param handshake: Handshake mode. [Default: False]
        @param arg_separator: Separator to use between arguments. [Default: ',']
        @param resource_params: Arguments sent to the resource upon connection.
               https://pyvisa.readthedocs.io/en/latest/api/resources.html
        @returns: An Instrument communicator.

        """
        super().__init__(
            port,
            port_match,
            backend,
            handshake,
            arg_separator,
            **resource_params,
        )
        self.min_write_delay_s = 0

        self.channel1 = Channel(1, self, self)

        self.measurement = Measurement(
            self,
            [self.channel1],
        )

        self.channels = [self.channel1]

    def select(self, channel: Channel):
        self.inst(channel.name)

    def selected(self) -> Channel:
        v = self.inst().rstrip()
        for ch in self.channels:
            if v == ch.name:
                return ch

        return None
