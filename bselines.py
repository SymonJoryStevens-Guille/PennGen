import re
from collections import defaultdict
congone = open('../gentextfiles/20211124penndepth1001/hyp.testcongone.txt','r').readlines()
congoneout = open('congoneout.txt','w')
typegone = open('../gentextfiles/20211124penndepth1001/hyp.testtypegone.txt','r').readlines()
typegoneout = open('typegoneout.txt','w')
'''Switch lines to 1000 for bertinp.'''
lines = open('../20211124corpusthreedepth1001/testgoldcongone.txt','r').readlines()
bertinpwhole = open('bertinpwhole.txt','w')
bertinpfull = open('bertinpfull.txt','w')
bertinp = open('bertinp.txt','w')
mostcommonunrestrictedlength = open('mostcommonunrestrictedlength.txt','w')
mostcommon = open('mostcommon.txt','w')
confrequency = open('../goldreconstructed.txt','r')
countdict = defaultdict(dict)
frequencydict = defaultdict(int)
for line in confrequency:
    lin = line.split('<sep>')
    con = lin[0].strip(' ').strip()
    typ = lin[1].strip(' ').strip()
    if con not in countdict[typ]:
        countdict[typ][con] = 1
    else:
        countdict[typ][con] += 1
    frequencydict[con] += 1
commondictunrestrictedlength = defaultdict()
commondict = defaultdict()
for key in countdict.keys():
    orderfull = sorted(countdict[key],key=lambda x:countdict[key][x],reverse=True)
    order = [x for x in orderfull if len(x.split(' ')) == 1]
    commondictunrestrictedlength[key] = orderfull[0]
    commondict[key] = order[0]
mostfrequent = sorted(frequencydict.keys(),key=lambda x:frequencydict[x],reverse=True)
'''Restricted to connective of length one.'''
for j,line in enumerate(lines):
    #print(line.strip())
    lin = line.split('<sep>')
    #print(lin)
    con = lin[0].strip(' ').strip()
    typ = lin[1].strip(' ').strip()
    leftone = lin[2].strip(' ').strip()
    one = lin[3].strip(' ').strip()
    rightone = lin[4].strip(' ').strip()
    lefttwo = lin[5].strip(' ').strip()
    two = lin[6].strip(' ').strip()
    righttwo = lin[7].strip(' ').strip()
    out = lin[8].strip(' ').strip()
    outindex = out
    for i in [2,3,4,5,6,7]:
        if lin[i].strip(' ') != 'none':
            sub = lin[i].lstrip(' ').rstrip(' ')
            #print(f'position {i} no strip:'+sub)
            #print(f'position {i}:'+sub)
            outindex = re.sub(re.escape(sub),len(sub)*'_',outindex,1,re.IGNORECASE)
            #print(outindex)
    #print(outindex)
    #print(con)
    if con != 'none':
        try:
            index = outindex.index(con)
        except:
            try:
                index = outindex.index(con[0].upper()+con[1:])
            except:
                try:
                    index = outindex.index(con[0].lower()+con[1:])
                except:
                    continue
        bertsub = list(out)
        bertsub[index:index+len(con)] = '[MASK]'
        bertsub = ''.join(bertsub)
        #print(bertsub)
        lin[8] = bertsub+'\n'
        bertline = lin[8]
        lin = '<sep>'.join(lin)
        lin = re.sub(' *<sep> *',' <sep> ',lin)
        if len(con.split(' ')) == 1:
            #print(len(con.split(' ')))
            #continue
            bertinpfull.write(lin)
            bertinp.write(bertline)
            mostcommonunrestrictedlength.write(commondictunrestrictedlength[typ]+'\n')
            mostcommon.write(commondict[typ]+'\n')
            congoneout.write(congone[j].lower())
            typegoneout.write(typegone[j].lower())
    print('\n')

'''Not restricted on length or explicit/implicit.'''
congonewhole = open('../gentextfiles/20211124penndepth1001/hyp.testcongone.txt','r').readlines()
congoneoutwhole = open('congoneoutwhole.txt','w')
typegonewhole = open('../gentextfiles/20211124penndepth1001/hyp.testtypegone.txt','r').readlines()
typegoneoutwhole = open('typegoneoutwhole.txt','w')
lineswhole = open('../20211124corpusthreedepth1001/testgoldcongone.txt').readlines()
bertinpwhole = open('bertinpwhole.txt','w')
mostcommonwhole = open('mostcommonwhole.txt','w')
for j,line in enumerate(lineswhole):
    lin = line.split('<sep>')
    #print(lin)
    con = lin[0].strip(' ').strip()
    typ = lin[1].strip(' ').strip()
    leftone = lin[2].strip(' ').strip()
    one = lin[3].strip(' ').strip()
    rightone = lin[4].strip(' ').strip()
    lefttwo = lin[5].strip(' ').strip()
    two = lin[6].strip(' ').strip()
    righttwo = lin[7].strip(' ').strip()
    out = lin[8].strip(' ').strip()
    outindex = out
    for i in [2,3,4,5,6,7]:
        if lin[i].strip(' ') != 'none':
            sub = lin[i].lstrip(' ').rstrip(' ')
            #print(f'position {i} no strip:'+sub)
            #print(f'position {i}:'+sub)
            outindex = re.sub(re.escape(sub),len(sub)*'_',outindex,1,re.IGNORECASE)
            #print(outindex)
    mostcommonwhole.write(commondictunrestrictedlength[typ]+'\n')
    congoneoutwhole.write(congonewhole[j].lower())
    typegoneoutwhole.write(typegonewhole[j].lower())
    bertinpwhole.write(line)
    print('\n')

'''masked for implicit.'''
lineswhole = open('../20211124corpusthreedepth1000/testgoldcongone.txt').readlines()
implicitexplicitmasked = open('implicitexplicitmasked.txt','w')
for j,line in enumerate(lineswhole):
    lin = line.split('<sep>')
    #print(lin)
    con = lin[0].strip(' ').strip()
    typ = lin[1].strip(' ').strip()
    leftone = lin[2].strip(' ').strip()
    one = lin[3].strip(' ').strip()
    rightone = lin[4].strip(' ').strip()
    lefttwo = lin[5].strip(' ').strip()
    two = lin[6].strip(' ').strip()
    righttwo = lin[7].strip(' ').strip()
    out = lin[8].strip(' ').strip()
    outindex = out
    if con != 'none':
        for i in [2, 3, 4, 5, 6, 7]:
            if lin[i].strip(' ') != 'none':
                sub = lin[i].lstrip(' ').rstrip(' ')
                # print(f'position {i} no strip:'+sub)
                # print(f'position {i}:'+sub)
                outindex = re.sub(re.escape(sub), len(sub) * '_', outindex, 1, re.IGNORECASE)
                # print(outindex)
        try:
            index = outindex.index(con)
        except:
            try:
                index = outindex.index(con[0].upper() + con[1:])
            except:
                try:
                    index = outindex.index(con[0].lower() + con[1:])
                except:
                    index = outindex.index(con[0])
                    print(con)
                    print(outindex)
                    #continue
        bertsub = list(out)
        bertsub[index:index + len(con)] = '[MASK]'
        bertsub = ''.join(bertsub)
    else:
        if lefttwo != 'none':
            try:
                index = outindex.index(lefttwo)
            except:
                try:
                    index = outindex.index(lefttwo[0].upper() + lefttwo[1:])
                except:
                    try:
                        index = outindex.index(lefttwo[0].lower() + lefttwo[1:])
                    except:
                        print(lefttwo)
                        print(outindex)
                        print(lin)
                        exit()
                        #continue
        else:
            try:
                index = outindex.index(two)
            except:
                try:
                    index = outindex.index(two[0].upper() + two[1:])
                except:
                    try:
                        index = outindex.index(two[0].lower() + two[1:])
                    except:
                        print(two)
                        print(outindex)
                        print(line)
                        exit()
                        #continue
        bertsub = list(out)
        bertsub[index] = f'[MASK] {bertsub[index]}'
        bertsub = ''.join(bertsub)
    lin[8] = bertsub + '\n'
    bertline = lin[8]
    lin = '<sep>'.join(lin)
    lin = re.sub(' *<sep> *', ' <sep> ', lin)
    implicitexplicitmasked.write(bertline)
    print('\n')

'''Frequency determined mostcommonwhole.'''
lineswhole = open('../20211124corpusthreedepth1001/testgoldcongone.txt').readlines()
mostcommonwholefreq = open('mostcommonwholefreq.txt','w')
for j,line in enumerate(lineswhole):
    mostcommonwholefreq.write(mostfrequent[0]+'\n')
    print('\n')


