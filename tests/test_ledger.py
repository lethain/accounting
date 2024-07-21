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


class TestGeneralLedger(unittest.TestCase):
    def test_setup_chart_of_accounts(self):
        coa = ChartOfAccounts()
        coa.add_categories([Category(*x) for x in category_values])
        for account_value in account_values:
            coa.add_account(*account_value)

        cash_acc  = coa.get_account(101)
        self.assertEqual(cash_acc.name, 'Cash')
        self.assertEqual(cash_acc.num, 101)

        assets_category = coa.categories[0]
        self.assertEqual(assets_category.name, 'Assets')
        self.assertEqual(assets_category.start, 100)
    
