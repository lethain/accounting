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


class ChartOfAccounts:
    def __init__(self):
        self.categories = []

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
