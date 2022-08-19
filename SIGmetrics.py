import math
import re
import pathlib
import string
from collections import defaultdict
from itertools import combinations
import csv
import datetime
import wordninja
now = datetime.datetime.now()
currentime = now.strftime('%Y-%m-%d')

'''Function to get the connectives of the same type, connectives of the parent type, etc.'''
def up(type:str,connectives:list):
    type = type.strip().lower()
    connectives = list(set([(c.split('<sep>')[0].strip().lower(),c.split('<sep>')[1].strip().lower()) for c in connectives]))
    connectives.sort(key=lambda x:x[1])
    minusone = set()
    minustwo = set()
    minusthree = set()
    uptypecons = set()
    consident = set()
    for c in connectives:
        uptypelist = c[1].split('_')
        subtypelist = type.split('_')
        if uptypelist == subtypelist:
            consident.add(c[0])
            continue
        length = len(subtypelist)
        if set(subtypelist[:length-1]).issubset(set(uptypelist)):
            uptypecons.add(c)
            minusone.add(c[0])
            continue
        if set(subtypelist[:length-2]).issubset(set(uptypelist)):
            uptypecons.add(c)
            minustwo.add(c[0])
            continue
        if set(subtypelist[:length-3]).issubset(set(uptypelist)):
            uptypecons.add(c)
            minusthree.add(c[0])
            continue
    return uptypecons,consident,minusone,minustwo,minusthree

'''Get connective/type info from full reconstructed corpus connective/type file.'''
connectiveslist = open('goldreconstructed.txt','r').readlines()

'''Function to build file listing connectives by type plus the connectives of the same type, connectives of the parent type, etc.'''
def concestors():
    types = set([con.split('<sep>')[1].strip() for con in connectiveslist])
    confile = open('concestors.txt','w')
    for t in types:
        uptypecons, consident, minusone, minustwo, minusthree = up(t, connectiveslist)
        t = t.split('_')
        confile.write(f'type:{"_".join(t)}\n')
        confile.write(f'sisters:{consident}\n')
        if len(t) >= 2:
            confile.write(f'cons for types from {"_".join(t[0:len(t)-1])}:{minusone}\n')
        else:
            confile.write(f'type minus 1 is the set of every type\n')
        if len(t) >= 3:
            confile.write(f'cons for types from {"_".join(t[0:len(t)-2])}:{minustwo}\n')
        else:
            confile.write(f'type minus 2 is the set of every type\n')
        if len(t) >= 4:
            confile.write(f'cons for types from {"_".join(t[0:len(t)-3])}:{minusthree}\n')
        else:
            confile.write(f'type minus 3 is the set of every type\n')
        confile.write('\n_________\n')
    confile.close()

connectives = set([con.split('<sep>')[0].strip() for con in connectiveslist])

'''Function to get match metrics plus produce metric result files.
hyp = modeloutput. inputstring = testMR. reference = goldinput. outstyle = integer determining whether output is word (=1) or sentence (=0).'''
def connectivecongruence(hyp:str,inputstring:str,reference:str,outstyle:int):
    hypstring = hyp
    refstring = reference
    if re.search('congone',hyp):
        rep = 1
    else:
        rep = 0
    if rep == 1:
        out = open(f'{pathlib.Path(hyp).parent}/congonemetrics.txt','w')
        outcsvfile = open(f'{pathlib.Path(hyp).parent}/congonemetrics.csv','w',newline='')
        csvwriter = csv.writer(outcsvfile,delimiter=',')
        log = open(f'{pathlib.Path(hyp).parent}/congonemetricslogfile.txt','w')
        eiErrors = open(f'{pathlib.Path(hyp).parent}/congoneeiErrors.csv','w')
        eiwriter = csv.writer(eiErrors, delimiter=',')
        eiwriter.writerow(['modelone'])
        eiErrorsPrecise = open(f'{pathlib.Path(hyp).parent}/congoneeiErrorsPrecise.csv', 'w')
        eiwriterPrecise = csv.writer(eiErrorsPrecise, delimiter=',')
        eiwriterPrecise.writerow(['type','goldplicit','m1match'])
        conrel = open(f'{pathlib.Path(hyp).parent}/congoneCONREL.txt','w')
    else:
        out = open(f'{pathlib.Path(hyp).parent}/typegonemetrics.txt','w')
        outcsvfile = open(f'{pathlib.Path(hyp).parent}/typegonemetrics.csv', 'w', newline='')
        csvwriter = csv.writer(outcsvfile, delimiter=',')
        log = open(f'{pathlib.Path(hyp).parent}/typegonemetricslogfile.txt','w')
        eiErrors = open(f'{pathlib.Path(hyp).parent}/typegoneeiErrors.csv', 'w')
        eiwriter = csv.writer(eiErrors, delimiter=',')
        eiwriter.writerow(['modeltwo'])
        eiErrorsPrecise = open(f'{pathlib.Path(hyp).parent}/typegoneeiErrorsPrecise.csv', 'w')
        eiwriterPrecise = csv.writer(eiErrorsPrecise, delimiter=',')
        eiwriterPrecise.writerow(['type', 'goldplicit', 'm2match'])
        conrel = open(f'{pathlib.Path(hyp).parent}/typegoneCONREL.txt','w')
    hyp = open(hyp, 'r').readlines()
    inputstr = open(inputstring, 'r').readlines()
    inputstr = [re.sub('\n', '', x).split('<sep>') for x in inputstr]
    print(inputstr[0])
    reference = open(reference, 'r').readlines()[:len(inputstr)]
    reference = [re.sub('\n', '', x).split('<sep>') for x in reference]
    print(reference[0][2:-1])
    print('goldlength:', len(reference))
    '''Ensure the inputstr indices = reference indices.'''
    if rep == 1:
        for i,line in enumerate(reference):
            if line[2:-1] != inputstr[i][1:]:
                print('reference:',i, line)
                print('reference subset:',i, line[2:-1])
                print('inputstr:',i, inputstr[i])
                print('inputstr subset',i, inputstr[i][1:])
                print('inputstr - reference:',set(line[2:-1]) - set(inputstr[i][1:]))
                print('reference - inputstr:',set(inputstr[i][1:]) - set(line[2:-1]))
                print('reference file:'+refstring)
                print('hypothesis file:'+hypstring)
                exit()
    else:
        for i,line in enumerate(reference):
            if line[2:-1] != inputstr[i]:
                print('reference:', i, line)
                print('inputstr:', i, inputstr[i])
                print('reference:', i, line)
                print('reference subset:', i, line[:-1])
                print('inputstr:', i, inputstr[i])
                print('inputstr subset', i, inputstr[i][:-1])
                print('inputstr - reference:', set(line[:-1]) - set(inputstr[i][:-1]))
                print('reference - inputstr:', set(inputstr[i][:-1]) - set(line[:-1]))
                print('reference file:' + refstring)
                print('hypothesis file:' + hypstring)
                exit()
    print('goldlength:', len(reference))
    log.write(f'goldlength:{len(reference)}\n')
    print('inputstrlength:',len(inputstr))
    log.write(f'inputstrlength:{len(inputstr)}\n')
    print('hyplength:',len(hyp))
    log.write(f'hyplength:{len(hyp)}\n')
    '''Build dicts for storing results.'''
    sumcounts = defaultdict(int)
    predictedimplicitcounts = defaultdict(list)
    predictedexplicitcounts = defaultdict(list)
    predictedexplicitcountsPrecise = defaultdict(list)
    goldexplicitcounts = defaultdict(list)
    goldimplicitcounts = defaultdict(list)
    sumofgold = 0
    correcthyp = 0
    expinsyn = defaultdict(list)
    expinone = defaultdict(list)
    expintwo = defaultdict(list)
    expinthree = defaultdict(list)
    expother = defaultdict(list)
    impinsyn = defaultdict(list)
    impinone = defaultdict(list)
    impintwo = defaultdict(list)
    impinthree = defaultdict(list)
    impother = defaultdict(list)
    counter = 0
    for line1,line2 in zip(hyp, inputstr):
        index = counter
        counter += 1
        print('\nnew item.')
        log.write('\nnew item.\n')
        print('index:',index)
        log.write(f'index:{index}\n')
        log.write(f'counter:{counter}\n')
        revline1 = line1.strip('\n').lower()
        print('hypstring:',hypstring)
        log.write(f'hypstring:{hypstring}\n')
        print('hyp:',line1.strip('\n'))
        log.write(f'hyp:{line1.strip()}\n')
        print('inputstring:',line2)
        log.write(f'inputstring:{line2}\n')
        ref = reference[index]
        print('reference:',ref)
        log.write(f'reference:{ref}\n')
        con = ref[0]
        type = ref[1]
        plicit = ''
        if con.strip().lower() == 'none':
            goldimplicitcounts[type].append(1)
            goldexplicitcounts[type].append(0)
            log.write('implicit\n')
            plicit = 'imp'
        elif con.strip().lower() != 'none':
            goldexplicitcounts[type].append(1)
            goldimplicitcounts[type].append(0)
            log.write('explicit\n')
            plicit = 'exp'
        else:
            print('unidentified connective in gold:',con.strip().lower())
            exit()
        print('con:',con.strip().lower())
        log.write(f'con:{con.strip().lower()}\n')
        print('type:',type.strip().lower())
        log.write(f'type:{type.strip().lower()}\n')
        uptypecons,consident,minusone,minustwo,minusthree = up(type,connectiveslist)
        sumofgold += 1
        sumcounts[type] += 1
        print('revline1:',revline1)
        log.write(f'revline1:{revline1}\n')
        revline1 = wordninja.split(revline1)
        print('wordninja revline1:',revline1)
        log.write(f'wordninja revline1:{revline1}\n')
        revline1 = ' '.join(revline1)
        print('revline1 join:',revline1)
        log.write(f'revline1 join:{revline1}\n')
        '''If rep = 0 delete args from input in output by word.'''
        if outstyle == 0:
            for slot in ref[2:-1]:
                slot = wordninja.split(slot.strip('\n').lower())
                print(slot)
                for word in slot:
                    revline1 = re.sub(f'(?<!\w){re.escape(word)}(?!\w)', '', revline1, 1, re.IGNORECASE)
        if outstyle == 1:
            if revline1 == 'none':
                revline1 = ''
        print('revised revline1:',revline1)
        log.write(f'revised revline1:{revline1}\n')
        explicit = [connective.strip().lower() for connective in connectives if(re.search(f'(?<!\w){connective.strip().lower()}(?!\w)',revline1))]
        print('explicit:',explicit)
        log.write(f'explicit:{explicit}\n')
        '''Get rid of subsequences in explicit.'''
        if len(explicit) > 1:
            for s,e in enumerate(explicit):
                if any([re.search(f'(?<!\w){explicit[s]}(?!\w)',explicit[i]) for i in range(0,len(explicit)) if i != s]):
                    del explicit[s]
        print('revised explicit:',explicit)
        log.write(f'revised explicit:{explicit}\n')
        revline1 = ' '.join([word for word in explicit])
        print(f'revised revised revline1 (=join of explicit):{revline1}\n')
        log.write(f'revised revised revline1:{revline1}\n')
        if explicit:
            '''get predicted con <sep> rel'''
            conrel.write(f'{explicit[0].strip()} <sep> {type.strip()}\n')
            '''connective in out.'''
            if con.strip().lower() in explicit:
                '''correctly predicts explicit (Texp).'''
                correcthyp += 1
                predictedexplicitcounts[type].append(1)
                predictedexplicitcountsPrecise[type].append(1)
                eiwriter.writerow('1')
                eiwriterPrecise.writerow([f'{type}']+[f'{plicit}']+['1'])
                log.write('correctly predicts explicit (Texp).\n')
                log.write('error type: none\n')
            else:
                '''incorrectly predicts explicit (Fexp).'''
                predictedexplicitcounts[type].append(0)
                eiwriter.writerow('0')
                eiwriterPrecise.writerow([f'{type}']+[f'{plicit}']+['0'])
                log.write('incorrectly predicts explicit (Fexp).\n')
                '''2+ (respectively 3+) corresponds to predicting mismatching explicit for implicit (respectively explicit) gold'''
                if any(x in consident for x in explicit):
                    expinsyn[type].append(1)
                    if con.strip().lower() == 'none':
                        predictedexplicitcountsPrecise[type].append(2)
                        log.write('error type: 2\n')
                    elif con.strip().lower() != 'none':
                        predictedexplicitcountsPrecise[type].append(3)
                        log.write('error type: 3\n')
                elif any(x in minusone for x in explicit):
                    expinone[type].append(1)
                    if con.strip().lower() == 'none':
                        predictedexplicitcountsPrecise[type].append(22)
                        log.write('error type: 22\n')
                    elif con.strip().lower() != 'none':
                        predictedexplicitcountsPrecise[type].append(33)
                        log.write('error type: 33\n')
                elif any(x in minustwo for x in explicit):
                    expintwo[type].append(1)
                    if con.strip().lower() == 'none':
                        predictedexplicitcountsPrecise[type].append(222)
                        log.write('error type: 222\n')
                    elif con.strip().lower() != 'none':
                        predictedexplicitcountsPrecise[type].append(333)
                        log.write('error type: 333\n')
                elif any(x in minusthree for x in explicit):
                    expinthree[type].append(1)
                    if con.strip().lower() == 'none':
                        predictedexplicitcountsPrecise[type].append(2222)
                        log.write('error type: 2222\n')
                    elif con.strip().lower() != 'none':
                        predictedexplicitcountsPrecise[type].append(3333)
                        log.write('error type: 3333\n')
                else:
                    expother[type].append(1)
                    if con.strip().lower() == 'none':
                        predictedexplicitcountsPrecise[type].append(22222)
                        log.write('error type: 22222\n')
                    elif con.strip().lower() != 'none':
                        predictedexplicitcountsPrecise[type].append(33333)
                        log.write('error type: 33333\n')
                    print('weird output:', explicit)
                    print('intended connective:', con.strip().lower())
                    exit()
        #elif con.strip().lower() == 'none'
        elif not explicit:
            '''get predicted con <sep> rel'''
            conrel.write(f'none <sep> {type.strip()}\n')
            '''no connective in out.'''
            if con.strip().lower() == 'none':
                '''correctly predicts implicit (Timp).'''
                correcthyp += 1
                predictedimplicitcounts[type].append(1)
                eiwriter.writerow('1')
                eiwriterPrecise.writerow([f'{type}']+[f'{plicit}']+['1'])
                log.write('correctly predicts implicit (Timp).\n')
                log.write('error type: none\n')
            elif con.strip().lower() != 'none':
                '''incorrectly predicts implicit (Fimp).'''
                predictedimplicitcounts[type].append(0)
                eiwriter.writerow('0')
                eiwriterPrecise.writerow([f'{type}']+[f'{plicit}']+['0'])
                log.write('incorrectly predicts implicit (Fimp).\n')
                '''-2+ corresponds to predicting mismatching implicit for explicit gold'''
                if any(x == 'none' for x in consident):
                    impinsyn[type].append(1)
                    log.write('error type: -2\n')
                elif any(x == 'none' for x in minusone):
                    impinone[type].append(1)
                    log.write('error type: -22\n')
                elif any(x == 'none' for x in minustwo):
                    impintwo[type].append(1)
                    log.write('error type: -222\n')
                elif any(x == 'none' for x in minusthree):
                    impinthree[type].append(1)
                    log.write('error type: -2222\n')
                #elif any(x == 'none' for x in connectives):
                else:
                    impother[type].append(1)
                    log.write('error type: -22222\n')
                    print('weird output:',explicit)
                    print('intended connective:',con.strip().lower())
                    exit()
        else:
            print('something in this code is buggered')
            exit()
    csvwriter.writerow(['type']+[str(x) for x in sumcounts.keys()])
    csvwriter.writerow(['sum']+[str(sumcounts[x]) for x in sumcounts])
    csvwriter.writerow(['Gold_Explicit']+[str(len([y for y in goldexplicitcounts[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Predicted_Explicit']+[str(len([y for y in predictedexplicitcounts[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Mispredicted_Explicit']+[str(len([y for y in predictedexplicitcounts[x] if y == 0])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Sister']+[str(len([y for y in expinsyn[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Sister_For_Implicit']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 2])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Sister_For_Explicit'] + [str(len([y for y in predictedexplicitcountsPrecise[x] if y == 3])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Type_Minus_One']+[str(len([y for y in expinone[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Implicit_Type_Minus_One']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 22])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Explicit_Type_Minus_One']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 33])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Type_Minus_Two']+[str(len([y for y in expintwo[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Implicit_Type_Minus_Two']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 222])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Explicit_Type_Minus_Two']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 333])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Type_Minus_Three']+[str(len([y for y in expinthree[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Implicit_Type_Minus_Three']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 2222])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Explicit_Type_Minus_Three']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 3333])) for x in sumcounts])
    csvwriter.writerow(['Explicit_Type_Other']+[str(len([y for y in expother[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Implicit_Type_Other']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 22222])) for x in sumcounts])
    csvwriter.writerow(['Explicit_For_Explicit_Type_Other']+[str(len([y for y in predictedexplicitcountsPrecise[x] if y == 33333])) for x in sumcounts])
    csvwriter.writerow(['Gold_Implicit']+[str(len([y for y in goldimplicitcounts[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Predicted_Implicit']+[str(len([y for y in predictedimplicitcounts[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Mispredicted_Implicit']+[str(len([y for y in predictedimplicitcounts[x] if y == 0])) for x in sumcounts])
    csvwriter.writerow(['Implicit_Sister']+[str(len([y for y in impinsyn[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Implicit_Type_Minus_One']+[str(len([y for y in impinone[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Implicit_Type_Minus_Two']+[str(len([y for y in impintwo[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Implicit_Type_Minus_Three']+[str(len([y for y in impinthree[x] if y == 1])) for x in sumcounts])
    csvwriter.writerow(['Implicit_In_Other'] + [str(len([y for y in impother[x] if y == 1])) for x in sumcounts])
    out.write('Model:'+hypstring+'\n')
    out.write('Sum:'+str(sumofgold)+'\n')
    out.write('Correct Hypotheses:'+str(correcthyp)+'\n')
    out.write('Gold Explicit:'+str(sum([len([y for y in goldexplicitcounts[x] if y == 1]) for x in sumcounts]))+'\n')
    out.write('Predicted Explicit:'+str(sum([len([y for y in predictedexplicitcounts[x] if y == 1]) for x in sumcounts]))+'\n')
    out.write('Mispredicted Explicit:'+str(sum([len([y for y in predictedexplicitcounts[x] if y == 0]) for x in sumcounts]))+'\n')
    out.write('Explicit Sister:' + str(sum([len([y for y in expinsyn[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Explicit Sister for Implicit:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 2]) for x in sumcounts])) + '\n')
    out.write('Explicit Sister for Explicit:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 3]) for x in sumcounts])) + '\n')
    out.write('Explicit Type Minus One:' + str(sum([len([y for y in expinone[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Explicit for Implicit Type Minus One:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 22]) for x in sumcounts])) + '\n')
    out.write('Explicit for Explicit Type Minus One:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 33]) for x in sumcounts])) + '\n')
    out.write('Explicit Type Minus Two:' + str(sum([len([y for y in expintwo[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Explicit for Implicit Type Minus Two:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 222]) for x in sumcounts])) + '\n')
    out.write('Explicit for Explicit Type Minus Two:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 333]) for x in sumcounts])) + '\n')
    out.write('Explicit Type Minus Three:' + str(sum([len([y for y in expinthree[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Explicit for Implicit Type Minus Three:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 2222]) for x in sumcounts])) + '\n')
    out.write('Explicit for Explicit Type Minus Three:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 3333]) for x in sumcounts])) + '\n')
    out.write('Explicit Other:' + str(sum([len([y for y in expother[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Explicit for Implicit Type Other:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 22222]) for x in sumcounts])) + '\n')
    out.write('Explicit for Explicit Type Other:' + str(sum([len([y for y in predictedexplicitcountsPrecise[x] if y == 33333]) for x in sumcounts])) + '\n')
    out.write('Gold Implicit:' + str(sum([len([y for y in goldimplicitcounts[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Predicted Implicit:' + str(sum([len([y for y in predictedimplicitcounts[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Mispredicted Implicit:' + str(sum([len([y for y in predictedimplicitcounts[x] if y == 0]) for x in sumcounts])) + '\n')
    out.write('Implicit Sister:' + str(sum([len([y for y in impinsyn[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Implicit Type Minus One:' + str(sum([len([y for y in impinone[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Implicit Type Minus Two:' + str(sum([len([y for y in impintwo[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Implicit Type Minus Three:' + str(sum([len([y for y in impinthree[x] if y == 1]) for x in sumcounts])) + '\n')
    out.write('Implicit Other:' + str(sum([len([y for y in impother[x] if y == 1]) for x in sumcounts])) + '\n')
    #breakpoint()
    return sumcounts,goldexplicitcounts,predictedexplicitcounts,expinsyn,expinone,expintwo,expinthree,goldimplicitcounts,predictedimplicitcounts,impinsyn,impinone,impintwo,impinthree

'''Sub your params here.'''
connectivecongruence('YOUR_MODEL_OUTPUT.txt','YOUR_TEST_MR.mr','YOUR_GOLD_TEST.txt','YOUR_OUTPUT_STYLE')
