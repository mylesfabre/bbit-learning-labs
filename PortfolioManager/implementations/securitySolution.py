import os
import sys
module_path = os.path.abspath('..')
if module_path not in sys.path:
    sys.path.append(module_path)

from interfaces.securityInterface import securityInterface
from generators.priceDataGenerator import priceData

class security(securityInterface):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name

    def getName(self) -> str:
        return self.name

    def getCurrentMarketValue(self) -> float:
        return priceData().getCurrentPrice(self.name)
