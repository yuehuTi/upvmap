# -*- coding: utf-8 -*-
import sys, csv, json

if __name__ == '__main__':
	visits, captures = set(), set()
	if sys.version_info[0] == 2:
		logfd = open('game_log.tsv', 'rb')
	else:
		logfd = open('game_log.tsv', encoding='utf8')
	spamreader = csv.reader(logfd, delimiter='\t', quotechar='|')
	print('Processing....')

	for row in spamreader:
		if row[3] == 'captured portal' and row[4] != 'failed':
			visits.add((row[1], row[2]))

	logfd.seek(0)
	for row in spamreader:
		if row[4] != 'failed' and ((row[3].startswith('hacked') and row[3].endswith('portal')) or row[3].endswith('deployed')):
			captures.add((row[1], row[2]))
	
	l_visits = [list(x) for x in visits]
	l_captures = [list(x) for x in captures if x not in visits]

	logfd.close()

	with open('html/data.js', 'w') as fout:
		fout.write('result = {}'.format(json.dumps({'visits':l_visits, 'captures': l_captures})))

	print('Done!\nPlease open "html/index.html" to view your upv map')
