import math
from collections import defaultdict
import datetime
import numpy
now = datetime.datetime.now()
currentime = now.strftime('%Y-%m-%d')

'''note:typegonegold == congonegold since there is only one gold for which both are tested'''
gold = open('20211124corpusthreedepth1000/testgoldtypegonetuples.txt','r').readlines()
congone = open('gentextfiles/20211124penndepth1000/submit20211124congoneCONREL.txt','r').readlines()
typegone = open('gentextfiles/20211124penndepth1000/submit20211124typegoneCONREL.txt','r').readlines()
discontinuous = lambda x: 'Comparison' in x[0] or 'Temporal_Asynchronous' in x[0] or 'Expansion_Alternative' in x[0] or 'Expansion_Exception' in x[0]
continuous = lambda x: 'Contingency_Cause' in x[0] or 'Expansion_Instantiation' in x[0] or 'Expansion_Restatement' in x[0] or 'Expansion_List' in x[0]
ambiguous = lambda x: 'Contingency_Condition' in x[0] or 'Temporal_Synchronous' in x[0] or 'Expansion_Conjunction'

'''determine conditional probability'''
def conditprob(xy:float,y:float):
    return xy/y

'''determine npmi given prob of rel, prob of con, and prob of (rel,con)'''
def npmi(x:float,y:float,bigramxy:float):
    return (math.log(x * y,2)/math.log(bigramxy,2)) - 1

'''determine markedness of the corpus ignoring con if con is implicit'''
def mrk(results:list,n=0):
    '''dict of connective:count'''
    concount = defaultdict(int)
    '''dict of relation:count'''
    relcount = defaultdict(int)
    '''dict of (relation,connective):count'''
    bicount = defaultdict(int)
    '''dict of two relation:count'''
    tworelcount = defaultdict(int)
    '''dict of (two relation,connective):count'''
    twobicount = defaultdict(int)
    '''dict of top relation:count'''
    toprelcount = defaultdict(int)
    '''dict of (top relation,connective):count'''
    topbicount = defaultdict(int)
    '''fill dicts by reading testgold line by line'''
    for line in results:
        line = line.split('<sep>')
        top = line[1].strip().split('_')[0]
        two = '_'.join(line[1].strip().split('_')[0:2])
        con = line[0].strip()
        '''ignore implicit con.'''
        if con == 'none':
            continue
        rel = line[1].strip()
        concount[con] += 1
        relcount[rel] += 1
        bicount[(rel,con)] += 1
        tworelcount[two] += 1
        twobicount[(two,con)] += 1
        toprelcount[top] += 1
        topbicount[(top,con)] += 1
    '''dict of con:prob'''
    conprob = defaultdict(float)
    '''dict of rel:prob'''
    relprob = defaultdict(float)
    '''dict of (rel,con):prob'''
    biprob = defaultdict(float)
    '''dict of two:prob'''
    tworelprob = defaultdict(float)
    '''dict of (two,con):prob'''
    twobiprob = defaultdict(float)
    '''dict of top:prob'''
    toprelprob = defaultdict(float)
    '''dict of (top,con):prob'''
    topbiprob = defaultdict(float)
    '''build connective probs'''
    for x in concount:
        conprob[x] = concount[x] / sum([concount[y] for y in concount])
    '''build relation probs'''
    for x in relcount:
        relprob[x] = relcount[x] / sum([relcount[y] for y in relcount])
    '''build (rel,con) probs'''
    for x in bicount:
        biprob[x] = bicount[x] / sum([bicount[y] for y in bicount])
    '''build two rel probs'''
    for x in tworelcount:
        tworelprob[x] = tworelcount[x] / sum([tworelcount[y] for y in tworelcount])
    '''build (tworel,con) probs'''
    for x in twobicount:
        twobiprob[x] = twobicount[x] / sum([twobicount[y] for y in twobicount])
    '''build top rel probs'''
    for x in toprelcount:
        toprelprob[x] = toprelcount[x] / sum([toprelcount[y] for y in toprelcount])
    '''build (toprel,con) probs'''
    for x in topbicount:
        topbiprob[x] = topbicount[x] / sum([topbicount[y] for y in topbicount])
    mrkdict = defaultdict(float)
    '''mrk metric for (rel,con).'''
    for key in biprob:
        x = relprob[key[0]]
        y = conprob[key[1]]
        mrkdict[key] = (biprob[key] / x) * ((npmi(x, y, biprob[key]) + 1) / 2)
    relmrkdict = {k:0 for k in [line.split('<sep>')[1].strip() for line in gold]}
    '''mrk metric for rel by sum of mrk metric (rel,con).'''
    for key in relcount:
        relmrkdict[key] = sum([mrkdict[(k[0], k[1])] for k in mrkdict if k[0] == key])
    '''mrk metric for (tworel,con).'''
    twomrkdict = defaultdict(float)
    for key in twobiprob:
        x = tworelprob[key[0]]
        y = conprob[key[1]]
        twomrkdict[key] = (twobiprob[key] / x) * ((npmi(x, y, twobiprob[key]) + 1) / 2)
    tworelmrkdict = {k:0 for k in ['_'.join(line.split('<sep>')[1].strip().split('_')[0:2]) for line in gold]}
    '''mrk metric for tworel by sum of mrk metric (tworel,con).'''
    for key in tworelcount:
        tworelmrkdict[key] =sum([twomrkdict[(k[0],k[1])] for k in twomrkdict if k[0] == key])
    '''mrk metric for (toprel,con).'''
    topmrkdict = defaultdict(float)
    for key in topbiprob:
        x = toprelprob[key[0]]
        y = conprob[key[1]]
        topmrkdict[key] = (topbiprob[key] / x) * ((npmi(x,y,topbiprob[key]) + 1) / 2)
    toprelmrkdict = {k:0 for k in ['Comparison','Contingency','Expansion','Temporal']}
    '''mrk metric for toprel by sum of mrk metric (toprel,con).'''
    for key in toprelcount:
        toprelmrkdict[key] =sum([topmrkdict[(k[0],k[1])] for k in topmrkdict if k[0] == key])
    out1 = [x for x in toprelmrkdict.items()]
    out1.sort(key=lambda x: x[0])
    scores1 = numpy.array([x[1] for x in out1])
    out2 = [x for x in tworelmrkdict.items()]
    out2.sort(key=lambda x: x[0])
    scores2 = numpy.array([x[1] for x in out1])
    out3 = [x for x in relmrkdict.items()]
    out3.sort(key=lambda x: x[0])
    scores3 = numpy.array([x[1] for x in out2])
    filtered1 = list(filter(continuous, out2))
    filtered1.sort(key=lambda x:x[0])
    scores_filtered1 = numpy.array([x[1] for x in filtered1])
    filtered2 = list(filter(discontinuous, out2))
    filtered2.sort(key=lambda x:x[0])
    scores_filtered2 = numpy.array([x[1] for x in filtered2])
    filtered3 = list(filter(ambiguous, out2))
    filtered3.sort(key=lambda x:x[0])
    scores_filtered3 = numpy.array([x[1] for x in filtered3])
    print('top level',out1)
    print(scores1)
    print('two level',out2)
    print(scores2)
    print('full depth',out3)
    print(scores3)
    print('discontinuous',filtered1)
    print(scores_filtered1)
    print('continuous',filtered2)
    print(scores_filtered2)
    print('ambiguous',filtered3)
    print(scores_filtered3)
    return [scores1, scores2, scores_filtered1, scores_filtered2, scores_filtered3][n]
print('congone')
conres = mrk(congone)
print('--------------------\n')
print('typegone')
typeres = mrk(typegone)
print('--------------------\n')
print('gold')
gold = mrk(gold)