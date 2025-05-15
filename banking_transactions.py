from datetime import datetime, timedelta

class Transaction:

    def __init__(self, id, user_id, amt, currency, timestamp, type):
        self.id = id
        self.user_id = user_id
        self.amt = float(amt)
        self.currency = currency
        self.timestamp = datetime.strptime(timestamp)
        self.type = type

    def get_date(self):
        return to_date(self.timestamp)
        

class Bank:

    def __init__(self):
        self.deposits = {
            "2022-10-21": [],
        }
        self.withdrawals = {}
        # self.transactions = []
        self.transactions = {"txn_id": Transaction}
        self.user_index = {"user_id": [txn_id]}

    def parse_data(self, transactions):
        for txn in transactions:
            data = txn.split(",")
            txn = Transaction(*data)
            self.transactions.append(txn)

            if txn.type == "deposit":
                self.deposits.setdefault(txn.get_date(), [])
                self.deposits[txn.get_date()].append(txn.user_id)


    def filter(self, start_date, end_date, type):
        arr = []
        if type == "deposit":
            arr.extend(self.deposits[date])
        if type == "withdrawal":
            arr.extend(self.withdrawals[date])


