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
        if row[4] == 'failed':
            continue

        if row[3] == 'captured portal':
            captures.add((row[1], row[2]))

        #hack
        if row[3].startswith('hacked') and row[3].endswith('portal'):
            visits.add((row[1], row[2]))
        #deloyed resnator or mod
        if row[3].endswith('deployed'):
            visits.add((row[1], row[2]))
        #link
        if row[3] == 'created link':
            visits.add((row[1], row[2]))
        #virus
        if row[3].startswith('used') and row[3].endswith('virus'):
            visits.add((row[1], row[2]))

    l_captures = [list(x) for x in captures]
    l_visits = [list(x) for x in visits if x not in captures]

    logfd.close()

    with open('html/data.js', 'w') as fout:
        fout.write('result = {}'.format(json.dumps({'visits':l_visits, 'captures': l_captures})))

    print('Done!\nPlease open "html/index.html" to view your upv map')
