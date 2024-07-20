import datetime
from accounting.utils import leftpad_table

"""
Representing accounts and chart of accounts.
"""
class MismatchedAccount(Exception):
    pass


class Account:
    def __init__(self, num, name, debit_credit_rules):
        self.num = num
        self.name = name
        # True = debits add, credits sub
        # False = debits sub, credits add
        self.debit_credit_rules = debit_credit_rules


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
        
    def add_account(self, num, name, debit_credit_rules):
        acc = Account(num, name, debit_credit_rules)
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
                acc += '\t' + str(account.debit_credit_rules)
            acc += '\n'
        return acc



class Journal:
    def __init__(self, name, coa):
        self.name = name
        self.coa = coa
        self.entries = []

    def post(self, entry):
        self.entries.append(entry)
        entry.journal = self
        if len(self.entries) > 1:
            prev, last = self.entries[-2:]
            if prev.date > last.date:
                self.entries.sort(key=lambda x: x.date)

    def general_ledger_as_str(self):
        title = 'General ledger'

        changed_accounts = {}
        for entry in self.entries:
            changes = entry.debits + entry.credits
            for change in changes:
                if change.acc_num not in changed_accounts:
                    changed_accounts[change.account_num] = []
                changed_accounts[change.account_num].append(change)
                
        changed_accounts_by_num = sorted(changed_accounts.keys())
        for account_num in changed_accounts_by_num:
            account = self.coa.get_account(account_num)
            account_changes = changed_accounts_by_num[account_num]
            account_changes.sort(key=lambda x: x.date)
            print(account.name, account_changes)
            
        return ""
        
        
        

    def __repr__(self):
        rows = [
            ['Date', 'Account Titles and Explanations', 'Ref', 'Debit', 'Credit'],
        ]
        
        for entry in self.entries:
            entry_rows = []
            for debit in entry.debits:
                row = ['', self.coa.get_account(debit.acc_num).name, str(debit.acc_num), str(debit.amount), '']
                entry_rows.append(row)
            for credit in entry.credits:
                row = ['', self.coa.get_account(credit.acc_num).name, str(credit.acc_num), '', str(credit.amount)]
                entry_rows.append(row)                
            entry_rows[0][0] = str(entry.date.date())
            entry_rows.append([])
            rows += entry_rows

        return leftpad_table(f'General Journal ({self.name})', rows)


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
        self.journal = None
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
        return f'Entry({self.date.date()}: {debits}, {credits})'
