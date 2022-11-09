from typing import Set, Iterable
from interfaces.accountInterface import accountInterface
from interfaces.securityInterface import securityInterface
from interfaces.portfolioInterface import portfolioInterface

class portfolio(portfolioInterface):
    def __init__(self, portfolioName: str, accounts: Set[accountInterface]) -> None:
        super().__init__(portfolioName, accounts)
        self.portName = portfolioName
        self.accts = {act.getName(): act for act in accounts}

    def getAllAccounts(self) -> Iterable[accountInterface]:
        # create a list (iterable) that includes all of the accounts
        actList = list(self.accts.values())
        return actList

    def getAccounts(self, accountNamesFilter: Set[str], securitiesFilter: Set) -> Iterable[accountInterface]:
        # if there is a filter then only add those names in the filter
        # else add all of the accounts in the self.accounts
        if accountNamesFilter:
            filter = set()
            for acc in accountNamesFilter:
                if acc in self.accts: filter.add(self.accts[acc])
        else: filter = set(self.accts.values())
        output = set()
        # if there's a security filter, then only add securities in that filter
        # else don't filter any and include all
        if securitiesFilter:
            for acc in filter:
                # if the given securities are in the account then add them
                if acc.getPositions(securitiesFilter): output.add(acc)
        else: output = filter
        return output

    def addAccounts(self, accounts: Set[accountInterface]) -> None:
        for act in accounts:
            self.accts[act.getName()] = act
    
    def removeAccounts(self, accountNames: Set[str]) -> None:
        for name in accountNames:
            self.accts.pop(name, None)