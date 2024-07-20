import datetime

"""
Representing accounts and chart of accounts.
"""
class MismatchedAccount(Exception):
    pass


class Account:
    def __init__(self, num, name):
        self.num = num
        self.name = name


class Category:
    def __init__(self, name, start, end):
        "Name of category, start is inclusive, end is exclusive"
        self.name = name
        self.start = start
        self.end = end
        self.accounts = []

    def add(self, account):
        if account.num < self.start or account.num > self.end:
            raise MismatchedAccount(f('{account.num} not between {self.start} and {self.end}'))
        self.accounts.append(account)
        self.accounts.sort(key=lambda x: x.num)
        

    def __repr__(self):
        cls = self.__class__.__name__
        as_str = f'{cls}(name={self.name}, start={self.start})'
        return as_str

class MissingAccount(Exception):
    pass

    
class ChartOfAccounts:
    def __init__(self):
        self.categories = []
        self.accounts_by_num = {}

    def add_categories(self, categories):
        self.categories += categories
        self.categories.sort(key=lambda x: x.start)
        
    def add_account(self, num, name):
        acc = Account(num, name)
        category = self.matching_category(num)
        if category is None:
            nums = ", ".join([str(x.start) for x in self.categories])
            raise MismatchedAccount(f'{num} does not match with any existing account: {nums}')
        category.add(acc)
        self.accounts_by_num[num] = acc

    def get_account(self, num):
        if num in self.accounts_by_num:
            return self.accounts_by_num[num]
        raise MissingAccount(f'no account with number {num}')

    def matching_category(self, num):
        for category in self.categories:
            if num >= category.start and num < category.end:
                return category
        return None

    def __repr__(self):
        acc = 'ChartOfAccounts'
        for category in self.categories:
            acc += '\n' + category.name

            for account in category.accounts:
                acc += '\n' + str(account.num) + '\t' + account.name
            acc += '\n'
        return acc



class Ledger:
    def __init__(self, coa):
        self.coa = coa
        self.entries = []

    def post(self, entry):
        self.entries.append(entry)
        entry.ledger = self
        if len(self.entries) > 1:
            prev, last = self.entries[-2:]
            if prev.date > last.date:
                self.entries.sort(key=lambda x: x.date)

    def __repr__(self):
        acc = 'Ledger'
        for entry in self.entries:
            acc += '\n' + str(entry)
        return acc


class Credit:
    is_credit = True
    
    def __init__(self, acc_num, amount, note=None):
        self.acc_num = acc_num
        self.amount = amount
        self.note = note
        

class Debit(Credit):
    is_credit = False
    
class Entry:
    def __init__(self, date, changes=None):
        self.ledger = None
        self.date = datetime.datetime.strptime(date, "%d/%m/%Y")
        self.credits = []
        self.debits = []
        if changes:
            for change in changes:
                if change.is_credit:
                    self.credits.append(change)
                else:
                    self.debits.append(change)
    def __repr__(self):
        if self.ledger:
            credits_str = ", ".join([f'Credit({self.ledger.coa.get_account(x.acc_num).name}, {x.acc_num}: {x.amount})' for x in self.credits])
            debits_str = ", ".join([f'Debit({self.ledger.coa.get_account(x.acc_num).name}, {x.acc_num}: {x.amount})' for x in self.debits])
        else:
            credits_str = ", ".join([f'Credit({x.acc_num}: {x.amount})' for x in self.credits])
            debits_str = ", ".join([f'Debit({x.acc_num}: {x.amount})' for x in self.debits])
        return f'Entry({self.date.date()}, {credits_str}, {debits_str})'
