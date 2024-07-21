from accounting.accounts import Category, ChartOfAccounts, Journal, Entry, Credit, Debit
from tests.test_ledger import make_coa

coa = make_coa()
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
print(journal.general_ledger())
