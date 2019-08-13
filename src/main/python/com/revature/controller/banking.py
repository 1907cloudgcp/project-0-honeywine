##==============================================================================
##	Python Console
##==============================================================================

## imports
import os, sys, signal

#### logging imports
import logging, logging.config, yaml
maindir = '/'.join(__file__.split('/')[:-2])
with open(maindir + '/resources/logging.yaml', 'r') as f:
	lconfig = yaml.safe_load(f.read())
	logging.config.dictConfig(lconfig)
info_logger = logging.getLogger('infoLogger')

from getch import getch
from PyInquirer import prompt
from getpass import getpass
from revature.service import bank
from revature.error import errors


## global variables

#### global interrupt variable used by signal handler
run = True

#### original sigint
original_sigint = signal.getsignal(signal.SIGINT)

#### console questions
_console = {
	'type': 'list',
	'name': 'qbank',
	'message': 'Welcome to Revature Banking.',
	'choices': [
		'Login',
		'Register',
		'exit',
	],
}
_bank_options = {
	'type': 'list',
	'name': 'bopts',
	'message': 'Hello {}.  What do you wish to do?',
	'choices': [
		'Withdraw money',
		'Deposit money',
		'View balance',
		'View past transactions',
		'Logout',
	],
}


## functions

#### console routines
def console():
	"""
	Banking prompt.
	"""
	while(True):
		answer = prompt(_console)
		if (answer['qbank'] == 'Register'):
			registration()
		elif (answer['qbank'] == 'Login'):
			login()
		elif (answer['qbank'] == 'exit'):
			print("Thank you.  We hope to see you again...")
			info_logger.info("banking console exited")	
			break
## ~ fin console ~ ##


def registration():
	"""
	Registration prompt.
	"""
	print("Provide username, password, and starting balance "					
			+ "(hit Ctrl-C to go back).")
	try:
		bp = bank.BankProfile()
		while(True):
			username = input(">> Username: ")
			if (username in bp.load_user_list()):
				print("Username is already in use.")	
				continue
			if (username == ""):
				print("Username cannot be empty.")
				continue
			break
		password = getpass(">> Password: ")
		if (password == ""):
			print("Password cannot be empty.")
			return
		if (getpass(">> Verify Password: ") != password):
			print("Passwords do not match.")
			return
		balance = get_amount(">> Starting Balance: ")
		try:
			bp.register(username, password, balance)
			print("Welcome " + username + ".  "									
					+ "Your registration is complete.  "						 
					+ "Your starting balance is $" + str(balance) + ".00.")
			info_logger.info(username + " registered.")
		except errors.UserViolation as err:
			print(err.message)
	except KeyboardInterrupt:
		print()
		return
## ~ fin registration ~ ##


def login():
	"""
	Login prompt.
	"""
	try:
		username, password = "", ""
		bp = bank.BankProfile()
		for k in range(3):
			print("Provide credentials (hit Ctrl-C to go back).")
			username = input(">> Username: ")
			password = getpass(">> Password: ")
			try:
				bp.load_profile(username, password)
				info_logger.info(username + " logged in.")
				banking_options(username, bp)
				del bp
				break	
			except errors.PasswordViolation as err:
				print(err.message)	
			except errors.UserViolation as err:
				print(err.message2)		
	except KeyboardInterrupt:
		print()
		return
## ~ fin login ~ ##


def banking_options(username, bankprofile):
	"""
	Banking Options.
	"""
	global _bank_options
	bank_options = _bank_options.copy()
	bank_options['message'] = bank_options['message'].format(username)
	while(True):
		answer = prompt(bank_options)
		if (answer['bopts'] == 'Withdraw money'):
			withdraw(bankprofile)
		if (answer['bopts'] == 'Deposit money'):
			deposit(bankprofile)
		if (answer['bopts'] == 'View balance'):
			view_balance(bankprofile)
		if (answer['bopts'] == 'View past transactions'):
			view_past_transactions(bankprofile)
		if (answer['bopts'] == 'Logout'):
			print("Thank you for banking with us.  Until next time.")
			info_logger.info(username + " logged out.")
			break
## ~ fin banking_options ~ ##


def withdraw(bankprofile):
	"""
	Withdraw money.
	"""
	try:
		amount = get_amount(">> Enter amount to withdraw: ")
		print("You withdrew $" + str(bankprofile.withdraw(amount)))	 
	except KeyboardInterrupt:
		return
## ~ fin withdraw ~ ##


def deposit(bankprofile):
	"""
	Deposit money.
	"""
	try:
		amount = get_amount(">> Enter amount to deposit: ")
		print("You deposited $" + str(bankprofile.deposit(amount)))	 
	except KeyboardInterrupt:
		return
## ~ fin deposit ~ ##


def view_balance(bankprofile):
	"""
	View balance.
	"""
	try:
		print("You have $" + str(bankprofile.balance()) + " in your account.")
	except KeyboardInterrupt:
		return
## ~ fin view_balance ~ ##


def view_past_transactions(bankprofile):
	"""
	View past transactions.
	"""
	try:
		print("Your past transactions.")
		for transtime, amount in bankprofile.transactions():
			print(str(transtime) + " :: $" + str(amount))
	except KeyboardInterrupt:
		return
## ~ fin view_past_transactions ~ ##


def get_amount(message):
	"""
	Retrieves an integer from prompt.
	"""
	print(message, end='', flush=True)
	mtail = message.split('\n')[-1]
	num = ""
	while(True):
		char = getch()
		if (char.isnumeric()):
			num += char
			print(char, end='', flush=True)
		elif (char == '\x7f'):
			num = num[:-1]
			print('\r'+ mtail + num + " ", end='', flush=True)
			print('\r'+ mtail + num, end='', flush=True)
		elif (char == '\r'):
			print()
			break
		elif (char == '\x03'):
			raise KeyboardInterrupt
	return ( abs(int(num)) if (num != "") else 0 )
## ~ fin get_amount ~ ##	


#### signal handlers
def new_interrupt(signum, frame):
	"""
	Handles SIGINT.  Meant to be used by a decorator.
	"""
	global original_sigint
	global run
	signal.signal(signal.SIGINT, original_sigint)
	run = False
	signal.signal(signal.SIGINT, new_interrupt)
## ~ fin new_interrupt ~ ##


def signal_decorator(func, *args):
	"""
	Wraps a function between signal handlers for SIGINT.
	"""
	def wrapper(func, *args):
		global original_sigint
		signal.signal(signal.SIGINT, new_interrupt)
		func(*args)
		signal.signal(signal.SIGINT, original_sigint)
	return wrapper
## ~ fin signal_decorator ~ ##
