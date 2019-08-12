'''
This is the main script.
'''

## imports
import sys, os
sys.path.append("/".join(sys.path[0].split('/')[:-1]))
os.chdir(sys.path[0])

#### logging imports
import logging, logging.config, yaml
with open(sys.path[0] + '/resources/logging.yaml', 'r') as f:
	lconfig = yaml.safe_load(f.read())
	logging.config.dictConfig(lconfig)
info_logger = logging.getLogger('infoLogger')

from PyInquirer import prompt
from revature.controller import banking
# from revature.controller import router


## global variables
_question1 = {
	'type': 'list',
	'name': 'q1',
	'message': "Welcome to Revature GCP.  What do you want to do?",
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
	info_logger.info("main console started")
	while(True):
		answer = prompt(_question1)
		if (answer['q1'] == 'exit'):
			info_logger.info("main console exited")
			print("Goodbye...")
			exit()
		if (answer['q1'] == 'Routing'):
			## tentative...
			print("In development...")
			exit()
		if (answer['q1'] == 'Banking'):
			info_logger.info("banking console started")
			banking.console()
## ~ fin main ~ ##


## main routine
if __name__ == '__main__':
	main()
