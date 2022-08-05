import csv
import difflib
src = open('bertinpfull.txt','r').readlines()
#bert = open('sortedTokenStringSymonBert.txt','r').readlines()
commonfull = open('mostcommonunrestrictedlength.txt','r').readlines()
common = open('mostcommon.txt','r').readlines()
congone = open('congoneout.txt','r').readlines()
typegone = open('typegoneout.txt','r').readlines()
commonwhole = open('mostcommonwhole.txt','r').readlines()
commonwholefreq = open('mostcommonwholefreq.txt','r').readlines()
congonewhole = open('congoneoutwhole.txt','r').readlines()
typegonewhole = open('typegoneoutwhole.txt','r').readlines()
commonfullmatch = 0
for i,line in enumerate(commonfull):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    #print(lin)
    #print(srccon)
    if lin == srccon:
        commonfullmatch += 1
    #print('----------------------------------------------')
print(f'commonunrestrictedlength match:{commonfullmatch} of {len(commonfull)} = {commonfullmatch/len(commonfull)}.')

commonmatch = 0
for i,line in enumerate(common):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    #print(lin)
    #print(srccon)
    if lin == srccon:
        commonmatch += 1
    #print('----------------------------------------------')
print(f'common match:{commonmatch} of {len(common)} = {commonmatch/len(common)}.')


congonematch = 0
for i,line in enumerate(congone):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    #print(lin)
    #print(srccon)
    if lin == srccon:
        congonematch += 1
    #print('----------------------------------------------')
print(f'congone match:{congonematch} of {len(congone)} = {congonematch/len(congone)}.')


typegonematch = 0
for i,line in enumerate(typegone):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    #print(lin)
    #print(srccon)
    if lin == srccon:
        typegonematch += 1
    #print('----------------------------------------------')
print(f'typegone match:{typegonematch} of {len(typegone)} = {typegonematch/len(typegone)}.')

src = open('bertinpwhole.txt','r').readlines()
commonmatchwhole = 0
for i,line in enumerate(commonwhole):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    rel = srcline.split('<sep>')[1].strip().lower()
    #print(lin)
    #print(srccon)
    if srccon == lin:
        commonmatchwhole += 1
    #print('----------------------------------------------')
print(f'D+ bseline match:{commonmatchwhole} of {len(commonwhole)} = {commonmatchwhole/len(commonwhole)}.')

src = open('bertinpwhole.txt','r').readlines()
commonmatchwholefreq = 0
for i,line in enumerate(commonwholefreq):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    rel = srcline.split('<sep>')[1].strip().lower()
    #print(lin)
    #print(srccon)
    if srccon == lin:
        commonmatchwholefreq += 1
    #print('----------------------------------------------')
print(f'D- bseline match:{commonmatchwholefreq} of {len(commonwholefreq)} = {commonmatchwholefreq/len(commonwholefreq)}.')


congonematchwhole = 0
congonecheck = open('congonecheck.csv','w')
congonecheckwriter = csv.writer(congonecheck,delimiter = ',')
congonecheckwriter.writerow(['modelone'])
for i,line in enumerate(congonewhole):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    rel = srcline.split('<sep>')[1].strip().lower()
    #print(lin)
    #print(srccon)
    if srccon == lin:
        congonematchwhole += 1
        congonecheckwriter.writerow('1')
    else:
        congonecheckwriter.writerow('0')
    #print('----------------------------------------------')
print(f'D+ 1000 match:{congonematchwhole} of {len(congonewhole)} = {congonematchwhole/len(congonewhole)}.')

typegonematchwhole = 0
typegonecheck = open('typegonecheck.csv','w')
typegonecheckwriter = csv.writer(typegonecheck,delimiter = ',')
typegonecheckwriter.writerow(['modeltwo'])
for i,line in enumerate(typegonewhole):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    rel = srcline.split('<sep>')[1].strip().lower()
    #print(lin)
    #print(srccon)
    #print(i, lin, srccon, srcline)
    if srccon == lin:
        typegonematchwhole += 1
        typegonecheckwriter.writerow(['1'])
    else:
        typegonecheckwriter.writerow(['0'])
    #print('----------------------------------------------')
print(f'D- 1000 match:{typegonematchwhole} of {len(typegonewhole)} = {typegonematchwhole/len(typegonewhole)}.')

bert = open('sortedTokenStringSymonBert.txt')
src = open('bertinpfull.txt','r').readlines()
bertmatch = 0
for i,line in enumerate(bert):
    lin = line.strip().lower()
    srcline = src[i]
    srccon = srcline.split('<sep>')[0].strip().lower()
    rel = srcline.split('<sep>')[1].strip().lower()
    #print(lin)
    #print(srccon)
    if lin in ['"',".",","]:
        lin = 'none'
    if srccon == lin:
        bertmatch += 1
    #print('----------------------------------------------')
print(f'BERT match:{bertmatch} of {len(congonewhole)} = {bertmatch/len(congonewhole)}.')