'''
This is a test script.
'''

## imports
import sys, os
sys.path.append('/'.join(__file__.split('/')[:-2]))

import random, string

from revature.service import bank
from revature.io import bank_io
bank.load_test_environment()
bank_io.load_test_environment()

# from revature.controller import router


## test functions
def test_persistence():
	"""
	Registers a profile with the bank, and tests to see if transactions persist.
	"""
	username = ''.join([random.choice(string.ascii_letters + string.digits)		\
							for n in range(32)]) 
	password, balance = "fjords", 100
	bp = bank.BankProfile()
	bp.register(username, password, balance)
	bp.load_profile(username, password)
	assert (username == bp.getuser())
	assert (balance == bp.balance())
	bp.deposit(50)
	bp.load_profile(username, password)
	assert (bp.balance() == 150)
	bp.withdraw(60)
	bp.load_profile(username, password)
	assert (bp.balance() == 90)
	assert (len(bp.transactions()) == 3)
	bp.save_profile()
## ~ fin test_persistence ~ ##


def test_authorization():
	"""
	Registers a profile with the bank, and tests if user authorization works.
	All records should be in test.log.
	"""
	username = ''.join([random.choice(string.ascii_letters + string.digits)		\
							for n in range(32)]) 
	password, balance = "fjords", 100
	bp = bank.BankProfile()
	bp.register(username, password, balance)
	bp.load_profile(username, password)
	try:
		bp.register(username, password, balance)
	except:
		pass
	try:
		bp.load_profile(username, "brook")
	except:
		pass
	try:
		bp.load_profile("narrow", password)
	except:
		pass
## ~ fin test_authorization ~ ##



