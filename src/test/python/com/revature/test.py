'''
This is the main testing script.
'''
## imports
import sys, os
os.chdir(sys.path[0] + "/../../../../main/python/com/revature")

def main():
	"""
	Calls pytest from main folder.
	"""
	os.system('pytest .')


if __name__ == '__main__':
	main()