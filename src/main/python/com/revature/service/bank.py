##==============================================================================
##	Python Banking Service
##==============================================================================

## imports
import sys, os

#### logging imports
import logging, logging.config, yaml
maindir = '/'.join(__file__.split('/')[:-2])
with open(maindir + '/resources/logging.yaml', 'r') as f:
	lconfig = yaml.safe_load(f.read())
	logging.config.dictConfig(lconfig)
debug_logger = logging.getLogger('defaultLogger')
error_logger = logging.getLogger('errorLogger')

import datetime
from revature.io import bank_io
from revature.error import errors


## global variables



## functions


## classes
class BankProfile():
	"""
	Bank Profile
	"""
	def __init__(self, username=None, balance=None, transactions=[]):
		"""
		Constructor with profile credentials
		"""
		self.__username = username
		self.__balance = balance
		self.__transactions = transactions
		self.__users = None
	## ~ fin __init__ ~ ##
		

	def getuser(self):
		"""
		Retrieve username
		"""
		return self.__username
	## ~ fin getuser ~ ##	


	def balance(self):
		"""
		View balance
		"""
		return self.__balance
	## ~ fin balance ~ ##	


	def withdraw(self, money):
		"""
		Withdraw money (avoids the issue of overdraft policy)
		"""
		money = min(money, self.__balance)
		self.__balance -= money
		self.__transactions.append((str(datetime.datetime.now()), -money))
		self.save_profile()
		return money
	## ~ fin withdraw ~ ##	


	def deposit(self, money):
		"""
		Deposit money
		"""
		self.__balance += money
		self.__transactions.append((str(datetime.datetime.now()), money))
		self.save_profile()
		return money
	## ~ fin deposit ~ ##	


	def transactions(self):
		"""
		Returns past transactions
		"""	
		return self.__transactions
	## ~ fin transactions ~ ##	


	def save_profile(self):
		"""
		Save profile to bank shelf
		"""
		profile = {
			'username': self.__username,
			'balance': self.__balance,
			'transactions': self.__transactions,
		}
		try:
			bank_io.save_profile(**profile)
		except errors.UserViolation as err:
			error_logger.error("bank.save_profile::" + err.message2)		
	## ~ fin save_profile ~ ##	


	def load_profile(self, username, password):
		"""
		Loads a profile
		"""
		try:
			profile = bank_io.load_profile(username,password)
			self.__username = profile['username']
			self.__balance = profile['balance']
			self.__transactions = profile['transactions']
		except errors.UserViolation as err:
			debug_logger.debug("bank.load_profile::" + err.message2)
			raise err
		except errors.PasswordViolation as err:
			debug_logger.debug("bank.load_profile::" + err.message)
			raise err
	## ~ fin load_profile ~ ##


	def load_user_list(self):
		"""
		Loads user list
		"""
		if (self.__users == None): 
			self.__users = bank_io.userlist()
		return self.__users
	## ~ fin load_user_list ~ ##		


	def register(self, username, password, balance, transactions=[]):
		"""
		Registers a profile.
		"""
		transactions.append((str(datetime.datetime.now()), balance))
		profile = {
			'username': username,
			'password': password,
			'balance': balance,
			'transactions': transactions,
		}
		try:
			bank_io.register(**profile)
		except errors.UserViolation as err:
			raise err
	## ~ fin register ~ ##
## ~ fin BankProfile ~ ##


#### test mode
def load_test_environment():
	global debug_logger
	global error_logger
	debug_logger = logging.getLogger('testLogger') 
	error_logger = logging.getLogger('testLogger')	