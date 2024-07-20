from accounting.accounts import Category, ChartOfAccounts, Journal, Entry, Credit, Debit


category_values = [
    ('Assets', 100, 200),
    ('Liabilities', 200, 300),
    ('Stockholder\'s Equity', 300, 400),
    ('Revenues', 400, 500),
    ('Expenses', 600, 1000),
]

DEBITS_ADD_CREDIT_SUB = True
DEBITS_SUB_CREDIT_ADD = False

account_values = [
    (101, 'Cash', DEBITS_ADD_CREDIT_SUB),
    (112, 'Accounts Receivable', DEBITS_ADD_CREDIT_SUB),
    (126, 'Supplies', DEBITS_ADD_CREDIT_SUB),
    (130, 'Prepaid Insurance', DEBITS_ADD_CREDIT_SUB),
    (157, 'Equipment', DEBITS_ADD_CREDIT_SUB),
    (158, 'Accumulated Depreciation -- Equipment', DEBITS_ADD_CREDIT_SUB),
    (200, 'Notes Payable', DEBITS_SUB_CREDIT_ADD),
    (201, 'Accounts Payable', DEBITS_SUB_CREDIT_ADD),
    (209, 'Unearned Service Revenue', DEBITS_SUB_CREDIT_ADD),
    (212, 'Salaries and Wages Payable', DEBITS_SUB_CREDIT_ADD),
    (230, 'Interest Payable', DEBITS_SUB_CREDIT_ADD),
    (311, 'Common Stock', DEBITS_SUB_CREDIT_ADD),
    (320, 'Retained Earnings', DEBITS_SUB_CREDIT_ADD),
    (332, 'Dividends', DEBITS_ADD_CREDIT_SUB),
    (350, 'Income Summary', DEBITS_SUB_CREDIT_ADD),
    (400, 'Service Revenue', DEBITS_SUB_CREDIT_ADD),
    (631, 'Supplies Expense', DEBITS_ADD_CREDIT_SUB),
    (711, 'Depreciation Expense', DEBITS_ADD_CREDIT_SUB),
    (722, 'Insurance Expense', DEBITS_ADD_CREDIT_SUB),
    (726, 'Salaries and Wages Expense', DEBITS_ADD_CREDIT_SUB),
    (729, 'Rent Expense', DEBITS_ADD_CREDIT_SUB),
    (732, 'Utilities Expense', DEBITS_ADD_CREDIT_SUB),
    (905, 'Interest Expense', DEBITS_ADD_CREDIT_SUB),
]

coa = ChartOfAccounts()
coa.add_categories([Category(*x) for x in category_values])
for account_value in account_values:
    coa.add_account(*account_value)

print(coa)

# create and populate journal with entries
journal = Journal('J1', coa)
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

# show general ledger summary of all journal entries
print(journal.general_ledger_as_str())
