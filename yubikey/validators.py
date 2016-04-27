import re

def valid_public_id(public_id):
	test = re.compile(ur'^[a-z]{12}$')
	return bool(re.search(test, public_id))