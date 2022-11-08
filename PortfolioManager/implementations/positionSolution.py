import os
import sys
module_path = os.path.abspath('..')
if module_path not in sys.path:
    sys.path.append(module_path)

from interfaces.positionInterface import positionInterface
from interfaces.securityInterface import securityInterface
from implementations.securitySolution import security

class position(positionInterface):
    def __init__(self, sec, initPos: int) -> None:
        super().__init__(sec, initPos)
        self.pos = initPos
        self.sec = sec
        if isinstance(sec, security): self.sec = sec
        else: self.sec = security(sec)

    def getSecurity(self) -> securityInterface:
        return self.sec

    def getPosition(self) -> int:
        return self.pos

    def setPosition(self, inputValue: int) -> None:
        if inputValue < 0:
            raise ValueError("Shorting is prohibited.")
        else:
            self.pos = inputValue

    def addPosition(self, inputValue: int) -> None:
        if (inputValue + self.pos) < 0:
            raise ValueError("Action will result in prohibited short position.")
        else:
            self.pos += inputValue
