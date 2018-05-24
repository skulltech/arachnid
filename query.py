import json
import argparse
from tabulate import tabulate



def filter(profile, keywords):
	searchables = ['username', 'full_name', 'biography']

	if any([keyword.lower() in profile[s].lower() for keyword in keywords for s in searchables]):
		return True
	return False


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, type=str, help='Input JSONL file containing scraped Instagram profiles.')
	parser.add_argument('-q', '--query', required=True, type=str, nargs='+', help='Query keywords.')
	args = parser.parse_args()

	with open(args.input) as inp:
		profiles = inp.readlines()

	filtered = []
	for profile in profiles:
		profile = json.loads(profile)
		if filter(profile, args.query):
			profile.pop('full_data', None)
			profile['biography'] = profile['biography'][:15]+'...'
			profile['full_name'] = profile['full_name'][:15]+'...'
			filtered.append(profile)
	
	print(tabulate(filtered, headers='keys'))


if __name__=='__main__':
	main()
