import glob, json, os

data = {'games': {}}

for json_file in glob.glob('../data/games/*.json'):
	with open(json_file, 'r') as fh:
		game_data = json.loads(fh.read())
		data['games'][os.path.basename(json_file).split('.')[0]] = game_data

for json_file in glob.glob('../data/*.json'):
	with open(json_file, 'r') as fh:
		game_data = json.loads(fh.read())
		data[os.path.basename(json_file).split('.')[0]] = game_data

with open('data.json', 'w') as out_file:
	out_file.write(json.dumps(data))
