import json
import bz2
import pickle

# load the months data as a dictionary
files = ['RC_2011-09', 'RC_2012-09', 'RC_2012-09', 'RC_2013-09', 'RC_2014-09', 'RC_2015-09', 'RC_2016-09']

for fi in files:
    data = []
    with bz2.open('{}.bz2'.format(fi), 'r') as f:
        for i, line in enumerate(f):
            print("ITER {}".format(i))
            row = json.loads(line)
            if row['subreddit'] == 'nfl':
                print("ITER {} FOUND NFL".format(i))
                data.append(row)

    with open('{}.pkl'.format(fi), 'wb') as f_dump:
        pickle.dump(data, f_dump)
