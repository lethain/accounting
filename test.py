from accounting.accounts import Category, ChartOfAccounts, Journal, Entry, Credit, Debit

category_values = [
    ('Assets', 100, 200),
    ('Liabilities', 200, 300),
    ('Stockholder\'s Equity', 300, 400),
    ('Revenues', 400, 500),
    ('Expenses', 600, 1000),
]

account_values = [
    (101, 'Cash'),
    (112, 'Accounts Receivable'),
    (126, 'Supplies'),
    (130, 'Prepaid Insurance'),
    (157, 'Equipment'),
    (158, 'Accumulated Depreciation -- Equipment'),
    (200, 'Notes Payable'),
    (201, 'Accounts Payable'),
    (209, 'Unearned Service Revenue'),
    (212, 'Salaries and Wages Payable'),
    (230, 'Interest Payable'),
    (311, 'Common Stock'),
    (320, 'Retained Earnings'),
    (332, 'Dividends'),
    (350, 'Income Summary'),
    (400, 'Service Revenue'),
    (631, 'Supplies Expense'),
    (711, 'Depreciation Expense'),
    (722, 'Insurance Expense'),
    (726, 'Salaries and Wages Expense'),
    (729, 'Rent Expense'),
    (732, 'Utilities Expense'),
    (905, 'Interest Expense'),
]

coa = ChartOfAccounts()
coa.add_categories([Category(*x) for x in category_values])
for acc_num, acc_name in account_values:
    coa.add_account(acc_num, acc_name)

print(coa)

# create and populate journal with entries
journal = Journal('J1', coa)

# Perform first entry
entries = [
    Entry('1/10/2024', [Debit(101, 10000), Credit(311, 10000)]),
    Entry('1/10/2024', [Debit(157, 5000), Credit(200, 5000)]),
    Entry('2/10/2024', [Debit(101, 1200), Credit(209, 1200)]),
    Entry('3/10/2024', [Debit(729, 900), Credit(101, 900)]),
    Entry('4/10/2024', [Debit(130, 600), Credit(101, 600)]),
    Entry('5/10/2024', [Debit(126, 2500), Credit(201, 2500)]),
    Entry('20/10/2024', [Debit(101, 10000), Credit(400, 10000)]),
    Entry('26/10/2024', [Debit(726, 4000), Credit(101, 4000)]),
    Entry('31/10/2024', [Debit(332, 500), Credit(101, 500)]),    
]

for entry in entries:
    journal.post(entry)

print(journal)
