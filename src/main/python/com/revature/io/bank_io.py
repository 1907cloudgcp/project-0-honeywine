##==============================================================================
##	Python Shelving I/O
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

import shelve
from Crypto.Hash import SHA256
from revature.error import errors


## global variables
bankshelve = sys.path[0] + '/db/db-bank-shelve'

## functions
def load_profile(username,password):
	"""
	Loads a bank profile.
	Checks password against SHA256 hash
	"""
	db = shelve.open(bankshelve)
	hash = SHA256.new()
	hash.update(str.encode(password))
	try: 
		if (db[username]['password'] == hash.digest()):
			debug_logger.debug("bank_io.load_profile::loading profile info for "
								+ username)
			profile = db[username]
			db.close()
			return profile
		else:
			db.close()
			debug_logger.debug("bank_io.load_profile::password failed for "
								+ username)
			raise errors.PasswordViolation
	except KeyError as err:
		error_logger.error("bank_io.load_profile::KeyError")
		raise errors.UserViolation


def save_profile(username, balance, transactions):
	"""
	Saves a bank profile.
	"""
	db = shelve.open(bankshelve, writeback=True)
	if (db.get(username) != None):
		debug_logger.debug("bank_io.save_profile::saving profile info for "
							+ username)
		db[username]['username'] = username
		db[username]['balance'] = balance
		db[username]['transactions'] = transactions
		db.close()
	else:
		error_logger.critical("bank_io.save_profile::"
								+ "attempted to saving unidentified user")
		db.close()
		raise errors.UserViolation


def userlist():
	"""
	Retrieves list of usernames.
	"""
	debug_logger.debug("bank_io.userlist::accessing userlist")
	db = shelve.open(bankshelve)
	users = [ val['username'] for val in db.values() ]
	db.close()
	return users


def register(**profile):
	"""
	Registers a profile.
	"""
	db = shelve.open(bankshelve, writeback=True)
	hash = SHA256.new()
	hash.update(str.encode(profile['password']))
	profile['password'] = hash.digest()
	if (db.get(profile['username']) == None):
		debug_logger.debug("bank_io.register::registering " + str(profile))
		db[profile['username']] = profile
		db.close()
	else:
		error_logger.warning("bank_io.register::"
								+ "attempted to register existent user")
		db.close()
		raise errors.UserViolation


#### test mode
def load_test_environment():
	global debug_logger
	global error_logger
	global bankshelve
	debug_logger = logging.getLogger('testLogger')
	error_logger = logging.getLogger('testLogger')
	bankshelve = '/'.join(__file__.split('/')[:-2]) + '/db/test/db-bank-shelve'