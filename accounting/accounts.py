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

class TrialBalance:
    def __init__(self, ledger):
        self.ledger = ledger
        self._built = None

    def build(self):
        if self._built:
            return self._built

        table = self.ledger.build()
        debits = []
        credits = []
        for category in table:
            account_num = category['num']
            account = self.ledger.journal.coa.get_account(account_num)
            balance = category['rows'][-1]['balance']
            as_dict = {'balance': balance, 'account_name': category['name'], 'account_num': account_num}
            if account.debit_credit_rules:
                debits.append(as_dict)
            else:
                credits.append(as_dict)

        debits_sum = sum([x['balance'] for x in debits])
        credits_sum = sum([x['balance'] for x in credits])
        equal = debits_sum == credits_sum
        built = { 'equal': equal, 'debits': debits, 'credits': credits, 'debits_sum': debits_sum, 'credits_sum': credits_sum}
        self._built = built
        return built

    def __repr__(self):
        as_dicts = self.build()

        rows = [['Account','Name', 'Debit', 'Credit']]
        accounts = []
        for row in as_dicts['credits']:
            accounts.append([str(row['account_num']), row['account_name'], '', str(row['balance'])])
        for row in as_dicts['debits']:
            accounts.append([str(row['account_num']), row['account_name'], str(row['balance']), ''])

        accounts.sort()
        rows += accounts + [['', 'Totals', str(as_dicts['debits_sum']), str(as_dicts['credits_sum'])]]
        return leftpad_table('Trial Balance', rows)


class GeneralLedger:
    def __init__(self, name, journal):
        self.name = name
        self.journal = journal
        self._built = None

    def account(self, num):
        tables = self.build()
        for table in tables:
            if table['num'] == num:
                return table

    def trial_balance(self):
        return TrialBalance(self)


    def build(self):
        # cache building GL
        if self._built:
            return self._built

        changed_accounts = {}
        for entry in self.journal.entries:
            changes = entry.debits + entry.credits
            for change in changes:
                if change.acc_num not in changed_accounts:
                    changed_accounts[change.acc_num] = []
                changed_accounts[change.acc_num].append(change)
        changed_accounts_by_num = sorted(changed_accounts.keys())

        tables = []
        for account_num in changed_accounts_by_num:
            account = self.journal.coa.get_account(account_num)
            account_changes = changed_accounts[account_num]
            account_changes.sort(key=lambda x: x.entry.date)

            debits_add_credits_sub = account.debit_credit_rules
            balance = 0
            table = []
            for change in account_changes:
                debit = None
                credit = None

                if change.is_debit and debit is None:
                    debit = 0
                elif change.is_credit and credit is None:
                    credit = 0

                if change.is_debit and debits_add_credits_sub:
                    debit = change.amount
                    balance += change.amount
                elif change.is_credit and debits_add_credits_sub:
                    credit = -change.amount
                    balance -= change.amount
                elif change.is_debit and not debits_add_credits_sub:
                    debit = -change.amount
                    balance -= change.amount
                elif change.is_credit and not debits_add_credits_sub:
                    credit = change.amount
                    balance += change.amount
                else:
                    raise Exception('should be unreachable')


                row = {'date': change.entry.date, 'ref': self.journal.name, 'debit': debit, 'credit': credit, 'balance': balance}
                table.append(row)
            tables.append({'name': account.name, 'num': account.num, 'rows': table})

        self._built = tables
        return tables

    def __repr__(self):
        tables_as_dicts = self.build()

        acc = self.name
        for table_as_dict in tables_as_dicts:
            account_name = table_as_dict['name']
            account_num = table_as_dict['num']
            title = f'\n{account_name}\t{account_num}'

            table = [['Date', 'Explanation', 'Ref', 'Debit', 'Credit', 'Balance']]
            for dict_row in table_as_dict['rows']:
                debit = dict_row['debit']
                credit = dict_row['credit']
                date = dict_row['date']
                balance = dict_row['balance']
                if debit is None:
                    debit = ''
                if credit is None:
                    credit = ''

                row = [str(date.date()), '', self.journal.name, str(debit), str(credit), str(balance)]
                table.append(row)
            acc += '\n' + leftpad_table(title, table)
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

    def general_ledger(self):
        return GeneralLedger('General ledger', self)

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
    is_debit = False

    def __init__(self, acc_num, amount, note=None):
        self.acc_num = acc_num
        self.amount = amount
        self.note = note
        self.entry = None


class Debit(Credit):
    is_credit = False
    is_debit = True

class Entry:
    def __init__(self, date, changes=None):
        self.journal = None
        self.date = datetime.datetime.strptime(date, "%d/%m/%Y")
        self.credits = []
        self.debits = []
        if changes:
            for change in changes:
                change.entry = self
                if change.is_credit:
                    self.credits.append(change)
                else:
                    self.debits.append(change)
    def __repr__(self):
        return f'Entry({self.date.date()}: {debits}, {credits})'
