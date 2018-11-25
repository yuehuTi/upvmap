# -*- coding: utf-8 -*-
import sys, csv, json
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

if __name__ == '__main__':
    visits, captures = set(), set()
    if sys.version_info[0] == 2:
        logfd = open('game_log.tsv', 'rU')
    else:
        logfd = open('game_log.tsv', encoding='utf8')
    data = logfd.read()
    data = data.replace('\0', '')

    f = StringIO(data)
    
    spamreader = csv.DictReader(f, delimiter='\t', quotechar='|')
    print('Processing....')

    try:
        for row in spamreader:
            try:            
                if row["Comments"] == 'failed':
                    continue
                if row["Tracker Trigger"] == 'captured portal':
                    captures.add((row["Event Lat"], row["Event Lng"]))

                #hack
                if row["Tracker Trigger"].startswith('hacked') and row["Tracker Trigger"].endswith('portal'):
                    visits.add((row["Event Lat"], row["Event Lng"]))
                #deloyed resnator or mod
                if row["Tracker Trigger"].endswith('deployed'):
                    visits.add((row["Event Lat"], row["Event Lng"]))
                #link
                if row["Tracker Trigger"] == 'created link':
                    visits.add((row["Event Lat"], row["Event Lng"]))
                #virus
                if row["Tracker Trigger"].startswith('used') and row["Tracker Trigger"].endswith('virus'):
                    visits.add((row["Event Lat"], row["Event Lng"]))
            except Exception as e:
                continue
    except Exception as e:
        print row

    l_captures = [list(x) for x in captures]
    l_visits = [list(x) for x in visits if x not in captures]

    logfd.close()

    with open('html/data.js', 'w') as fout:
        fout.write('result = {}'.format(json.dumps({'visits':l_visits, 'captures': l_captures})))

    print('Done!\nPlease open "html/index.html" to view your upv map')
