from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    # EWrapper function
    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 0)

    # In production application, we would wait for acknowledgement connection is complete.
    # Typically this is done by waiting for nextValidID callback.
    # app.disconnect()
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    # EClient function
    app.reqContractDetails(1, contract)

    app.run()


if __name__ == "__main__":
    main()