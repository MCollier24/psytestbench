"""
Created on January 11, 2024

@author: Matthew Collier
"""

import time

from psytestbench.psytb.instrument_roles.role import InstrumentRole


class ElectronicLoad(InstrumentRole):
    InstrumentRoleName = "electronic load"

    @classmethod
    def name(cls):
        return ElectronicLoad.InstrumentRoleName

    @classmethod
    def ramp(
        cls,
        voltageSetter,
        startValue: float,
        endValue: float,
        step: float,
        delaySeconds: float = 0.03,
    ):

        goingUp = True
        if startValue <= endValue:
            if step <= 0:
                raise ValueError(f"Ramp ({startValue},{endValue},{step} will never end")
            goingUp = True
        elif startValue > endValue:
            if step >= 0:
                raise ValueError(f"Ramp ({startValue},{endValue},{step} will never end")
            goingUp = False

        v = startValue

        isDone = False
        while not isDone:
            voltageSetter(v)

            v += step
            if goingUp:
                if v >= endValue:
                    isDone = True
            else:
                if v <= endValue:
                    isDone = True

            time.sleep(delaySeconds)

        voltageSetter(endValue)
