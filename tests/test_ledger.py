import unittest
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

def make_coa():
    coa = ChartOfAccounts()
    coa.add_categories([Category(*x) for x in category_values])
    for account_value in account_values:
        coa.add_account(*account_value)
    return coa

def make_journal():
    coa = make_coa()
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

    return journal, entries
    

class TestChartOfAccounts(unittest.TestCase):
    def test_setup_chart_of_accounts(self):
        coa = make_coa()

        cash_acc  = coa.get_account(101)
        self.assertEqual(cash_acc.name, 'Cash')
        self.assertEqual(cash_acc.num, 101)

        assets_category = coa.categories[0]
        self.assertEqual(assets_category.name, 'Assets')
        self.assertEqual(assets_category.start, 100)


class TestGeneralLedger(unittest.TestCase):
    def test_general_ledger(self):
        journal, entries = make_journal()
        for entry in entries:
            journal.post(entry)

        gl = journal.general_ledger()
        cash_acc = gl.account(101)
        self.assertEqual(cash_acc['num'], 101)        
        self.assertEqual(cash_acc['name'], 'Cash')

        """
        From 2-17 in textbook:

                 Date   Explanation   Ref   Debit   Credit   Balance
           2024-10-01                  J1   10000              10000
           2024-10-02                  J1    1200              11200
           2024-10-03                  J1             -900     10300
           2024-10-04                  J1             -600      9700
           2024-10-20                  J1   10000              19700
           2024-10-26                  J1            -4000     15700
           2024-10-31                  J1             -500     15200
        """
        rows = cash_acc['rows']
        expected = [10000, 11200, 10300, 9700, 19700, 15700, 15200]
        for i, bal in enumerate(expected):
            self.assertEqual(rows[i]['balance'], bal)         
        
class TestTrialBalance(unittest.TestCase):
    def test_general_ledger(self):
        journal, entries = make_journal()
        for entry in entries:
            journal.post(entry)

        gl = journal.general_ledger()        
        tb = gl.trial_balance().build()
        
        self.assertEqual(tb['equal'], True)
        self.assertEqual(tb['credits_sum'], 28700)
        self.assertEqual(tb['debits_sum'], 28700)        

