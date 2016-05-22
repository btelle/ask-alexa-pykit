'''
Script for testing out the response for any given request
'''

from __future__ import print_function
from lambda_function import lambda_handler
import json
import sys
import glob
import os
from argparse import ArgumentParser

class UnexpectedResponseException(Exception):
	pass

if __name__ == '__main__':
	for f in glob.glob('../test-data/*.json'):
		print (os.path.basename(f))
		request_obj = json.load(open(f))
		print ('Request JSON')
		print (json.dumps(request_obj, indent=2))
		response = lambda_handler(request_obj)
		print ('Response JSON')
		print (json.dumps(response, indent=2))

		if response['response']['outputSpeech']['text'] in ["I'm sorry, I don't know the answer.", "I couldn't understand your question, try again."]:
			raise UnexpectedResponseException()
		
		print("\n\n")
    