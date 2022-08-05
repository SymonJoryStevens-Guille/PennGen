import glob
import re
import os
import pathlib
from typing import *
from functools import reduce
from collections import defaultdict
from itertools import combinations
from transformers import BartTokenizer
import datetime
import csv
now = datetime.datetime.now()
currentime = now.strftime('%Y%m%d')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
Remove = ['AltLex','AltLexC','Hypophora','EntRel','NoRel']
conTypeStrings = defaultdict(list)
plicitNess = defaultdict(lambda:[0,0])

'''Get string from index plus text'''
def tostring(e,out):
    #print(e)
    if not e:
        return 'none'
    #return re.sub(' *\n',' ',''.join([out[i] for i in e])).rstrip(string.punctuation)
    return re.sub(' *\n', ' ', ''.join([out[i] for i in e]))

'''Get con string if it exists, log plicitness of contype'''
def plicitString(e:str,depth:int,out):
    e = e.split('|')
    plicitness = e[0]
    conTypeOne = '_'.join([x for x in e[8].split('.')[0:depth]])
    conTypeTwo = '_'.join([x for x in e[9].split('.')[0:depth]])
    existsCheck = not True
    if conTypeTwo != '':
        existsCheck = True
    if plicitness == 'Explicit':
        conTypeStrings[conTypeOne].append(tostring(ind(e[1]),out))
        plicitNess[conTypeOne][0] += 1
        if existsCheck:
            conTypeStrings[conTypeTwo].append(tostring(ind(e[1]),out))
            plicitNess[conTypeTwo][0] += 1
    else:
        plicitNess[conTypeOne][1] += 1
        if existsCheck:
            plicitNess[conTypeTwo][1] += 1

'''Lower string'''
def lowerstring(e:str):
    if not e:
        return 'none'
    e = re.sub(re.escape(e[0]), e[0].lower(), e, 1)
    return e

'''Build left + right context'''
def context(e:list,position:list):
    left = []
    right = []
    if not e:
        print('no context')
        return left,right
    for j,ee in enumerate(e):
        if j < len(e)-1:
            if e[j] + 1 != e[j+1]:
                #print('noncontig',e,e[j])
                left.append(e[j])
                right = e[j+1:]
                break
            else:
                if e[j] < position[0]:
                    left.append(e[j])
                else:
                    right.append(e[j])
    print(left, right)
    return left,right

'''Get index'''
def ind(e:str):
    e = e.split(';')
    e = [ee.split('..') for ee in e if ee.split('..') != ['']]
    if len(e) == 1:
        e = reduce(lambda x, y: x + y, [list(range(int(se[0]), int(se[1]))) for se in e])
        return e
    else:
        return 'discontinuous'

'''Get lines'''
def f(e:str,depth:int):
    e = e.split('|')
    conOvert = True
    if e[0] in Remove:
        return 'remove'
    if e[0] != 'Explicit':
        conOvert = not True
    if conOvert:
        conindex = ind(e[1])
    else:
        conindex = not True
    contypeone = not True
    if e[8] != '':
        contypeone = '_'.join([x for x in e[8].split('.')[0:depth]])
    contypetwo = not True
    if e[9] != '':
        contypetwo = '_'.join([x for x in e[9].split('.')[0:depth]])
    oneindex = ind(e[14])
    twoindex = ind(e[20])
    return conindex,contypeone,contypetwo,oneindex,twoindex

'''function to get lines from corp files'''
def lines(e:str):
    lin = defaultdict(list)
    for i, file in enumerate(glob.glob(e)):
        file = open(file, 'r').readlines()
        if len(file) >= 1:
            lin[i] = file
    return lin

'''function to get spec lines from corp files'''
def speclines(e:str,*spec:set):
    if spec:
        print('type of spec',type(spec))
        print('spec is',spec)
        lin = defaultdict(list)
        for i, file in enumerate(glob.glob(e)):
            #print('file is',file)
            for element in spec[0]:
               #print('element is',element)
                if element in file:
                    #print(element,file)
                    f = open(file, 'r').readlines()
                    if len(f) >= 1:
                        lin[i] = f
                    spec[0].remove(element)
                    break
        return lin
    else:
        lines(e)

'''function to get lines without type or connective'''
def typegone(e:str):
    e = re.sub('.*?<sep>.*?<sep>','',e,1)
    return e

'''function to get typed lines without connective'''
def congone(e:str):
    e = re.sub('.*?<sep>','',e,1)
    return e

'''function to get reconstructed gold connective/connective types by line'''
def gold():
    out = open('goldreconstructed.txt', 'w')
    for file in glob.glob('PDTB-3.0/data/gold/*/*'):
        discourse = open(file, 'r')
        for lin in discourse:
            lin = lin.split('|')
            if lin[7] != '':
                con = lin[7]
            else:
                con = 'none'
            if lin[8] != '':
                contypeone = '_'.join([x for x in lin[8].split('.')[0:10]])
                out.write(f'{lowerstring(con)} <sep> {contypeone}\n')
            if lin[9] != '':
                contypetwo = '_'.join([x for x in lin[9].split('.')[0:10]])
                out.write(f'{lowerstring(con)} <sep> {contypetwo}\n')
    out.close()
gold()

'''Build corpus from gold + raw'''
'''Depth is number of levels in contype.'''
'''Order is whether to include arg orders in MR. 0 is don't include arg order, 1 is include arg orders.'''
'''Lxstyle is whether output should be just the connective or the whole line. 0 is the whole line, 1 is just the connective.'''
def corpus(inp1,inp2,out,depth:int,order:int,lxstyle:int):
    ok = {1,0}
    if order not in ok or lxstyle not in ok:
        raise Exception(f'Ensure order and lxstyle are in {ok}')
    discourse = open(inp1,'r')
    text = open(inp2,'r',encoding='ISO-8859-1').read()
    lines = open(inp2,'r',encoding='ISO-8859-1').readlines()
    out = open(out,'w')
    #counter = 0
    discontinuouscount = 0
    noncontigcount = 0
    removecount = 0
    count = 0
    for line in discourse:
        #if counter < 300:
        #    counter += 1
        #if counter == 300:
        #    exit()
        if f(line,depth) == 'remove':
            removecount += 1
            continue
        conindex,contypeone,contypetwo,oneindex,twoindex = f(line,depth)
        print('New line.\n',conindex,'\n',contypeone,'\n',contypetwo,'\n',oneindex,'\n',twoindex,'\n')
        if conindex == 'discontinuous':
            discontinuouscount += 1
            continue
        if oneindex == 'discontinuous':
            discontinuouscount += 1
            continue
        if twoindex == 'discontinuous':
            discontinuouscount += 1
            continue
        print(f'{tostring(conindex,text)} <sep> {contypeone} <sep> {tostring(oneindex,text).strip()} <sep> {tostring(twoindex,text).strip()}\n')
        if contypetwo:
            print(f'{tostring(conindex,text)} <sep> {contypetwo} <sep> {tostring(oneindex,text).strip()} <sep> {tostring(twoindex,text).strip()}\n')
        oneindex.sort()
        twoindex.sort()
        plicitString(line,depth,text)
        oneindexrevised = oneindex
        twoindexrevised = twoindex
        '''Try to find context for oneindex/twoindex.'''
        for x in lines:
            if re.search(re.escape(tostring(oneindex,text)),x):
                oneindexrevised = ind(f'{text.index(x)}..{text.index(x)+len(x)}')
            if re.search(re.escape(tostring(twoindex,text)),x):
                twoindexrevised = ind(f'{text.index(x)}..{text.index(x)+len(x)}')
            if oneindexrevised != oneindex and twoindexrevised != twoindex:
                break
        '''If no context for oneindex/twoindex, context is empty.'''
        if oneindexrevised == oneindex:
            oneindexrevised = []
        if twoindexrevised == twoindex:
            twoindexrevised = []
        '''Filter oneindex/twoindex context.'''
        if oneindex[0] < twoindex[0]:
            for x in set(oneindexrevised):
                if x < twoindex[0]:
                    if x in twoindexrevised:
                        twoindexrevised.remove(x)
                elif x >= twoindex[0]:
                    oneindexrevised.remove(x)
        elif twoindex[0] < oneindex[0]:
            for x in set(twoindexrevised):
                if x < oneindex[0]:
                    if x in oneindexrevised:
                        oneindexrevised.remove(x)
                elif x >= oneindex[0]:
                    twoindexrevised.remove(x)
        if conindex:
            for x in conindex:
                if x in oneindexrevised:
                    oneindexrevised.remove(x)
                if x in twoindexrevised:
                    twoindexrevised.remove(x)
        #    outpt = list(set(oneindexrevised + twoindexrevised + conindex))
        #else:
        #    outpt = list(set(oneindexrevised + twoindexrevised))
        #outpt.sort()
        for x in oneindex:
            if x in oneindexrevised:
                oneindexrevised.remove(x)
        oneindexrevised.sort()
        for x in twoindex:
            if x in twoindexrevised:
                twoindexrevised.remove(x)
        twoindexrevised.sort()
        print('revised lines.\n')
        if oneindex[0] < twoindex[0]:
            onetwo = '12'
        elif twoindex[0] < oneindex[0]:
            onetwo = '21'
        con = tostring(conindex, text)
        one = lowerstring(tostring(oneindex, text).strip())
        two = lowerstring(tostring(twoindex, text).strip())
        left1,right1 = context(oneindexrevised,oneindex)
        leftcon1 = lowerstring(tostring(left1,text).strip())
        rightcon1 = lowerstring(tostring(right1,text).strip())
        if leftcon1 != 'none' and rightcon1 != 'none':
            noncontigcount += 1
        left2,right2 = context(twoindexrevised,twoindex)
        leftcon2 = lowerstring(tostring(left2, text).strip())
        rightcon2 = lowerstring(tostring(right2, text).strip())
        if conindex:
            outpt = list(set(left1 + oneindex + right1 + left2 + twoindex + right2 + conindex))
        else:
            outpt = list(set(left1 + oneindex + right1 + left2 + twoindex + right2))
        outpt.sort()
        if leftcon2 != 'none' and rightcon2 != 'none':
            noncontigcount += 1
        if lxstyle == 0:
            output = tostring(outpt, text).strip()
        elif lxstyle == 1:
            output = tostring(conindex,text).strip()
        if order == 0:
            outline1 = f'{lowerstring(con)} <sep> {contypeone} <sep> {leftcon1} <sep> {one} <sep> {rightcon1} <sep> {leftcon2} <sep> {two} <sep> {rightcon2} <sep> {output}\n'
        elif order == 1:
            outline1 = f'{lowerstring(con)} <sep> {contypeone} <sep> {onetwo} <sep> {leftcon1} <sep> {one} <sep> {rightcon1} <sep> {leftcon2} <sep> {two} <sep> {rightcon2} <sep> {output}\n'
        out.write(outline1)
        print(outline1)
        count += 1
        if contypetwo is not (not True):
            if order == 0:
                outline2 = f'{lowerstring(con)} <sep> {contypetwo} <sep> {leftcon1} <sep> {one} <sep> {rightcon1} <sep> {leftcon2} <sep> {two} <sep> {rightcon2} <sep> {output}\n'
            elif order == 1:
                outline2 = f'{lowerstring(con)} <sep> {contypetwo} <sep> {onetwo} <sep> {leftcon1} <sep> {one} <sep> {rightcon1} <sep> {leftcon2} <sep> {two} <sep> {rightcon2} <sep> {output}\n'
            out.write(outline2)
            print(outline2)
            count += 1
    out.close()
    return discontinuouscount,noncontigcount,removecount,count

'''function to construct the corpus of depth 10'''
def corpdepth10(order:int,lxstyle:int):
    pathlib.Path(f'{currentime}corpusthreedepth10{order}{lxstyle}/').mkdir(parents=True, exist_ok=True)
    discontinuouscount = 0
    noncontigcount = 0
    removecount = 0
    count = 0
    for file in glob.glob('PDTB-3.0/data/gold/*/*'):
        fileref = os.path.basename(file)
        textfile = re.sub('gold', 'raw', file)
        dcount,ncount,rcount,ccount = corpus(file, textfile, f'{currentime}corpusthreedepth10{order}{lxstyle}/'+fileref+f'{currentime}corpusthreedepth10{order}{lxstyle}',10,order,lxstyle)
        discontinuouscount += dcount
        noncontigcount += ncount
        removecount += rcount
        count += ccount
    print('discontinuouscount:',discontinuouscount)
    print('noncontigcount:',noncontigcount)
    print('removecount:',removecount)
    print('count:',count)
for x in set(combinations('1010',2)):
    corpdepth10(int(x[0]),int(x[1]))

'''function to build train/dev/test'''
def num(e:str,corptype:Callable[[str],str],corptypestring:str):
    dir = pathlib.Path(e.strip('wsj*')).absolute()
    trainIN = open(f'{dir}/train{corptypestring}.mr','w')
    devIN = open(f'{dir}/dev{corptypestring}.mr','w')
    testIN = open(f'{dir}/test{corptypestring}.mr','w')
    trainGOLD = open(f'{dir}/traingold{corptypestring}.txt','w')
    devGOLD = open(f'{dir}/devgold{corptypestring}.txt','w')
    testGOLD = open(f'{dir}/testgold{corptypestring}.txt','w')
    trainOUT = open(f'{dir}/train{corptypestring}.lx','w')
    devOUT = open(f'{dir}/dev{corptypestring}.lx','w')
    testOUT = open(f'{dir}/test{corptypestring}.lx','w')
    #sumOUT = open(f'{dir}/sumlines{corptypestring}.txt','w')
    lineInFile = lines(e)
    lin = dict(lineInFile)
    number = 0
    for i in lin.keys():
        number += len(lin[i])
    trainlines = []
    devlines = []
    testlines = []
    index = 0
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                trainGOLD.write(j)
                trainlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                trainIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                trainOUT.write(j[-1])
        if len(trainlines) >= int(number * .7):
            index = (list(lin).index(i)+1)
            break
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                devGOLD.write(j)
                devlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                devIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                devOUT.write(j[-1])
        if len(devlines) >= int(number * .15):
            index = (list(lin).index(i)+1)
            break
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                testGOLD.write(j)
                testlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                testIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                testOUT.write(j[-1])
    return trainlines,devlines,testlines
for x in set(combinations('1010', 2)):
    num(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',congone,'congone')
    num(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',typegone,'typegone')

'''function to build test/dev/train'''
def numreversesplit(e:str,corptype:Callable[[str],str],corptypestring:str):
    dir = pathlib.Path(e.strip('wsj*')).absolute()
    os.makedirs(f'{dir}/reversesplit',exist_ok=True)
    trainIN = open(f'{dir}/reversesplit/train{corptypestring}.mr','w')
    devIN = open(f'{dir}/reversesplit/dev{corptypestring}.mr','w')
    testIN = open(f'{dir}/reversesplit/test{corptypestring}.mr','w')
    trainGOLD = open(f'{dir}/reversesplit/traingold{corptypestring}.txt','w')
    devGOLD = open(f'{dir}/reversesplit/devgold{corptypestring}.txt','w')
    testGOLD = open(f'{dir}/reversesplit/testgold{corptypestring}.txt','w')
    trainOUT = open(f'{dir}/reversesplit/train{corptypestring}.lx','w')
    devOUT = open(f'{dir}/reversesplit/dev{corptypestring}.lx','w')
    testOUT = open(f'{dir}/reversesplit/test{corptypestring}.lx','w')
    #sumOUT = open(f'{dir}/sumlines{corptypestring}.txt','w')
    lineInFile = lines(e)
    lin = dict(lineInFile)
    number = 0
    for i in lin.keys():
        number += len(lin[i])
    trainlines = []
    devlines = []
    testlines = []
    index = 0
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                testGOLD.write(j)
                testlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                testIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                testOUT.write(j[-1])
        if len(testlines) >= int(number * .15):
            index = (list(lin).index(i)+1)
            break
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                devGOLD.write(j)
                devlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                devIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                devOUT.write(j[-1])
        if len(devlines) >= int(number * .15):
            index = (list(lin).index(i)+1)
            break
    for i in list(lin.keys())[index:]:
        for j in lin[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                trainGOLD.write(j)
                trainlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                trainIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                trainOUT.write(j[-1])
    return trainlines,devlines,testlines
for x in set(combinations('1010', 2)):
    numreversesplit(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',congone,'congone')
    numreversesplit(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',typegone,'typegone')


'''function to build test/dev/train'''
def numdemberg(e:str,corptype:Callable[[str],str],corptypestring:str):
    E = open('CODI.conn_gen.per_item.csv', 'r')
    EE = list(csv.DictReader(E, delimiter='\t'))
    EEE = set([line['wsj'] for line in EE])
    print('EEE',EEE)
    dir = pathlib.Path(e.strip('wsj*')).absolute()
    os.makedirs(f'{dir}/dembergsplit',exist_ok=True)
    trainIN = open(f'{dir}/dembergsplit/train{corptypestring}.mr','w')
    devIN = open(f'{dir}/dembergsplit/dev{corptypestring}.mr','w')
    testIN = open(f'{dir}/dembergsplit/test{corptypestring}.mr','w')
    trainGOLD = open(f'{dir}/dembergsplit/traingold{corptypestring}.txt','w')
    devGOLD = open(f'{dir}/dembergsplit/devgold{corptypestring}.txt','w')
    testGOLD = open(f'{dir}/dembergsplit/testgold{corptypestring}.txt','w')
    trainOUT = open(f'{dir}/dembergsplit/train{corptypestring}.lx','w')
    devOUT = open(f'{dir}/dembergsplit/dev{corptypestring}.lx','w')
    testOUT = open(f'{dir}/dembergsplit/test{corptypestring}.lx','w')
    #sumOUT = open(f'{dir}/sumlines{corptypestring}.txt','w')
    lineInFile1 = speclines(e,EEE)
    #print('lineInFile1',lineInFile1)
    lin1 = dict(lineInFile1)
    print('lin1',len(lin1),type(lin1))
    lineInFile2 = lines(e)
    lin2 = dict(lineInFile2)
    print('lin2',len(lin2),type(lin2))
    lin3 = {k:v for k,v in lin2.items() if v not in [z for x,z in lin1.items()]}
    print('lin3',len(lin3),type(lin3))
    number = 0
    for i in lin3.keys():
        number += len(lin3[i])
    trainlines = []
    devlines = []
    testlines = []
    index = 0
    for i in list(lin1.keys()):
        for j in lin1[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                testGOLD.write(j)
                testlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                testIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                testOUT.write(j[-1])
    for i in list(lin3.keys())[index:]:
        for j in lin3[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                devGOLD.write(j)
                devlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                devIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                devOUT.write(j[-1])
        if len(devlines) >= int(number * .25):
            index = (list(lin3).index(i)+1)
            break
    for i in list(lin3.keys())[index:]:
        for j in lin3[i]:
            if len(tokenizer(j)['input_ids']) < 1024:
                trainGOLD.write(j)
                trainlines.append(j)
                j = corptype(j)
                j = j.split('<sep>')
                trainIN.write('<sep>'.join(j[:len(j)-1])+'\n')
                trainOUT.write(j[-1])
    return trainlines,devlines,testlines

for x in set(combinations('1010', 2)):
    numdemberg(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',congone,'congone')
    numdemberg(f'{currentime}corpusthreedepth10{int(x[0])}{int(x[1])}/wsj*',typegone,'typegone')

'''build corpdepthn from corpdepth10 where split = 1 = reverse split, split = 2 = demberg split'''
def corpdepthn(i:int, order:int, lxstyle:int, *split:int):
    print(i, order, lxstyle, split)
    if split == 2:
        pathlib.Path(f'{currentime}corpusthreedepth{i}{order}{lxstyle}/dembergsplit/').mkdir(parents=True,
                                                                                             exist_ok=True)
        direct = f'{currentime}corpusthreedepth{i}{order}{lxstyle}/dembergsplit/'
        depth10lx = f'{currentime}corpusthreedepth10{order}{lxstyle}/dembergsplit/*congone.lx'
        depth10mr = f'{currentime}corpusthreedepth10{order}{lxstyle}/dembergsplit/*congone.mr'
    elif split == 1:
        pathlib.Path(f'{currentime}corpusthreedepth{i}{order}{lxstyle}/reversesplit/').mkdir(parents=True,
                                                                                             exist_ok=True)
        direct = f'{currentime}corpusthreedepth{i}{order}{lxstyle}/reversesplit/'
        depth10lx = f'{currentime}corpusthreedepth10{order}{lxstyle}/reversesplit/*congone.lx'
        depth10mr = f'{currentime}corpusthreedepth10{order}{lxstyle}/reversesplit/*congone.mr'
    else:
        pathlib.Path(f'{currentime}corpusthreedepth{i}{order}{lxstyle}/').mkdir(parents=True,
                                                                                             exist_ok=True)
        direct = f'{currentime}corpusthreedepth{i}{order}{lxstyle}/'
        depth10lx = f'{currentime}corpusthreedepth10{order}{lxstyle}/*congone.lx'
        depth10mr = f'{currentime}corpusthreedepth10{order}{lxstyle}/*congone.mr'
    print(direct)
    print(depth10lx)
    print(depth10mr)
    for file in glob.glob(depth10lx):
        out = re.sub('.*/','',file)
        #outfile = open(f'{currentime}corpusthreedepth{i}{order}{lxstyle}/{reverse}{out}','w')
        outfile = open(f'{direct}{out}','w')
        for line in open(file,'r').readlines():
            outfile.write(line)
        print(file)
        print(out)
    for file in glob.glob(depth10mr):
        out = re.sub('.*/', '', file)
        #outfile = open(f'{currentime}corpusthreedepth{i}{order}{lxstyle}/{reverse}{out}','w')
        outfile = open(f'{direct}{out}','w')
        for line in open(file, 'r').readlines():
            tokens = line.split('<sep>')
            type = tokens[0].split('_')
            type = '_'.join(type[:i])
            line = re.sub(tokens[0],f'{type} ',line)
            outfile.write(line)
for x in set(combinations('1010',2)):
    corpdepthn(1,int(x[0]),int(x[1]))
    corpdepthn(2,int(x[0]),int(x[1]))
    corpdepthn(1, int(x[0]), int(x[1]),1)
    corpdepthn(2, int(x[0]), int(x[1]),1)
    corpdepthn(1, int(x[0]), int(x[1]),2)
    corpdepthn(2, int(x[0]), int(x[1]),2)
