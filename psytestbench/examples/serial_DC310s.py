"""
Created on Jan 11, 2025

@author: Matthew Collier
"""

from psytestbench.kiprim_dc310s.instrument import Instrument as DC310S
import time

psu = DC310S(
    port="COM5", read_termination="\r\n", write_temrination="\n", baud_rate=115200
)

psu.connect()

print(psu.channel1.output())
psu.channel1.output(True)
time.sleep(5)
print(psu.channel1.output())
psu.channel1.output(False)
time.sleep(5)
print(psu.channel1.output())

psu.disconnect()
