'''
This is the main script.
'''

## imports
import sys, os
sys.path.append("/".join(sys.path[0].split('/')[:-1]))

from PyInquirer import prompt
from revature.controller import banking
# from revature.controller import router


## global variables
_question1 = {
	'type': 'list',
	'name': 'q1',
	'message': 'Welcome to Revature GCP.  What do you want to do?',
	'choices': [
		'Routing',
		'Banking',
		'exit',
	],
}


## functions
def main():
	"""
	Main console.
	"""
	while(True):
		answer = prompt(_question1)
		if (answer['q1'] == 'exit'):
			print("Goodbye...")
			exit()
		elif (answer['q1'] == 'Routing'):
			## tentative...
			print("In development...")
			exit()
		else:
			banking.console()


## main routine
if __name__ == '__main__':
	main()
