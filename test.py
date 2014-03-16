#!/usr/bin/python

import random, string
import json

def random_str(randomlength=20):
	a = list(string.ascii_letters)
	random.shuffle(a)
	return ''.join(a[:randomlength])


with open("kuaipan_token.json") as f:
	data = f.read()
	j = json.loads(data)
	print(j)
