##==============================================================================
##	Python Errors
##==============================================================================

## imports
import sys, os


## global variables


## functions


## classes
class PasswordViolation(Exception):
	"""
	Password Failed to Authenticate
	"""
	def __init__(self):
		self.message = "Password failed to authenticate"


class UserViolation(Exception):
	"""
	Username does not exist in database
	"""
	def __init__(self):
		self.message = "Username Violation"
		self.message1 = "Username already exists"
		self.message2 = "Username does not exist"

