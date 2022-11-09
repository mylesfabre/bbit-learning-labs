from typing import Set, Iterable
from interfaces.accountInterface import accountInterface
from interfaces.securityInterface import securityInterface
from interfaces.portfolioInterface import portfolioInterface
from generators.priceDataGenerator import priceData

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

    def acctMarVal(self, accounts:Iterable[accountInterface]):
        #Aggregate positions at this level & query their security value.
        posDict = {}
        totMarVal = 0
        for acct in accounts:
            for pos in acct.getAllPositions():
                if pos.getSecurity().getName() in posDict:
                    posDict[pos.getSecurity().getName()][0] += pos.getPosition()
                else:
                    posDict[pos.getSecurity().getName()] = [pos.getPosition(), pos.getSecurity()]
        for posInfo in posDict.values():
            totMarVal += posInfo[0] * posInfo[1].getCurrentMarketValue()
        return totMarVal

    def getCurrentMarketValue(self) -> dict:
        return self.acctMarVal(self.accts.values())

    def getCurrentFilteredMarketValue(self, securities: Set, accountNames: Set[str]) -> float:
        return self.acctMarVal(self.changeAcctPos(self.getAccounts(accountNames, securities), securities))

    def changeAcctPos(self, accounts: Iterable[accountInterface], securities: Set) -> Iterable[accountInterface]:
        if securities:
            return accounts
        modAccts = set()
        for acc in accounts:
            modAccts.add(account(acc.getPositions(securities).values(), "trimmed"))    

        return modAccts
