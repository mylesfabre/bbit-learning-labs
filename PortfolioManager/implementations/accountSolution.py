import os
import sys
module_path = os.path.abspath('..')
if module_path not in sys.path:
    sys.path.append(module_path)

from interfaces.accountInterface import accountInterface
from interfaces.positionInterface import positionInterface
from interfaces.securityInterface import securityInterface
from typing import Any, Dict, Set, Iterable

class account(accountInterface):
    def __init__(self, positions: Set[positionInterface], accountName: str) -> None:
        super().__init__(positions, accountName)
        self.acctName = accountName
        self.posSet = {pos.getSecurity().getName(): pos for pos in positions}

    def getName(self) -> str:
        return self.acctName

    def getAllPositions(self) -> Iterable[positionInterface]:
        allPos = self.posSet.values()
        return list(allPos)

    def getPositions(self, securities: Set) -> Dict[Any, positionInterface]:
        posMap = {}
        for sec in securities:
            if isinstance(sec, securityInterface) and sec.getName() in self.posSet:
                posMap.update({sec: self.posSet[sec.getName()]})
            elif sec in self.posSet:
                posMap.update({sec: self.posSet[sec]})
        return posMap

    def addPositions(self, positions: Set[positionInterface]) -> None:
        for pos in positions:
            posName = pos.getSecurity().getName()
            if posName in self.posSet:
                self.posSet[posName].setPosition(pos.getPosition()) 
            else: self.posSet[posName] = pos
            
    def removePositions(self, securities: Set) -> None:
        for sec in securities:
            if isinstance(sec, securityInterface):
                del self.posSet[sec.getName()]
            else: del self.posSet[sec]

