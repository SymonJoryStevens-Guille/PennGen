import re
import os
import sys
from collections import defaultdict
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
plt.figure(num=None, figsize=(1, 1), dpi=80, facecolor='w', edgecolor='k')

def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None

set_pandas_display_options()

def depth(typ,dep):
    return '_'.join(typ.split('_')[:dep]).strip()

'''mcnmr test where model1, model2 are csv files, obj is the type of error, typ is the sequence of rel to be checked for and depth of rel neither of which are required'''
def mcnmr(model1, model2, obj, **typ):
    print('\n', '-' * 100, '\n')
    n1 = model1.strip('.csv').split('/')[-1]
    n2 = model2.strip('.csv').split('/')[-1]
    m1 = pd.read_csv(model1)
    m2 = pd.read_csv(model2)
    hypt = pd.concat([m1,m2],axis=1)
    df = pd.DataFrame(hypt)
    df = df.T.drop_duplicates().T
    df.columns = ['type','goldplicit','model1','model2']
    print('df without restrictions')
    print(df)
    if 'dep' in typ.keys():
        df['type'] = df['type'].map(lambda x: depth(x,typ['dep']))
        print(f"df restricted to depth {typ['dep']}")
        print(df)
    if 'rel' in typ.keys():
        df.query(f"type == '{typ['rel']}'",inplace=True)
        print(f"df restricted to rel {typ['rel']}")
        print(df)
    if obj == 'e':
        df.query("goldplicit == 'exp'",inplace=True)
    if obj == 'i':
        df.query("goldplicit == 'imp'",inplace=True)
    print(f'df restricted to plicitness {obj}')
    print(df)
    hypterror = pd.DataFrame().reindex_like(df)
    hypterror = hypterror.drop(['type','goldplicit'],axis=1)
    for index, row in df.iterrows():
        if row['model1'] != 1:
            hypterror.at[index,'model1'] = 0
        else:
            hypterror.at[index,'model1'] = 1
        if row['model2'] != 1:
            hypterror.at[index,'model2'] = 0
        else:
            hypterror.at[index,'model2'] = 1
    yy = 0
    nn = 0
    yn = 0
    ny = 0
    for index, row in hypterror.iterrows():
        if row['model1'] == 1 and row['model2'] == 1:
            yy += 1
        elif row['model1'] == 0 and row['model2'] == 0:
            nn += 1
        elif row['model1'] == 0 and row['model2'] == 1:
            ny += 1
        elif row['model1'] == 1 and row['model2'] == 0:
            yn += 1
        else:
            print(row['model1'],row['model2'])
    rslts = [[yy, yn], [ny, nn]]
    print(yy+nn+yn+ny)
    print(pd.DataFrame(rslts, index=['m1y','m1n'], columns=['m2y', 'm2n']))
    result = mcnemar(rslts, exact=True, correction=True)
    print('statistic=%.3f, p-value=%.3f' % (result.statistic, result.pvalue))
    alpha = 0.05
    if result.pvalue > alpha:
        print('Same proportions of total number of entries with %s errors in %s and %s (fail to reject H0)' % (obj, n1, n2))
    else:
        print('Different proportions of total number of entries with %s error in %s and %s (reject H0)' % (obj, n1, n2))
    print('\n', '-' * 100, '\n')

def num(model, **typ):
    print('\n', '-' * 100, '\n')
    n = model.strip('.csv').split('/')[-1]
    m = pd.read_csv(model)
    df = pd.DataFrame(m).reindex_like(m)
    print(df)
    if 'dep' in typ.keys():
        print([depth(x,typ['dep']) for x in df.columns])
        print(f"df restricted to depth {typ['dep']}")
        df = df.groupby(by=[depth(x,typ['dep']) for x in df.columns],axis=1).sum()
        print(df)
        df = df.set_index(['type'])
        print(df)
    print(f'model {n}')
    for c in df.columns:
        matchE = df.loc['Predicted_Explicit',f'{c}']
        mismatchE = df.loc['Mispredicted_Explicit',f'{c}']  # predict = mismatch
        goldE = df.loc['Gold_Explicit',f'{c}']
        predictE = matchE + mismatchE  # totalpredict
        preE = matchE / predictE  # precision = matching predictions / total predictions
        recE = matchE / goldE  # recall = matching predictions / gold
        matchI = df.loc['Predicted_Implicit', f'{c}']
        mismatchI = df.loc['Mispredicted_Implicit', f'{c}']  # predict = mismatch
        goldI = df.loc['Gold_Implicit', f'{c}']
        predictI = matchI + mismatchI  # totalpredict
        preI = matchI / predictI  # precision = matching predictions / total predictions
        recI = matchI / goldI  # recall = matching predictions / gold
        print('----------------------------------------------------')
        print(f'{c} Explicit Precision:',preE)
        print(f'{c} Explicit Recall:',recE)
        print(f'{c} Implicit Precision:', preI)
        print(f'{c} Implicit Recall:', recI)
        print('----------------------------------------------------')
num('gentextfiles/DDDSIGPAPERpenndepth1000/congonemetrics.csv',dep=1)
num('gentextfiles/DDDSIGPAPERpenndepth1000/typegonemetrics.csv',dep=1)
exit()

'''Getting mcnmr(match).'''
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'e', dep=1, rel='Contingency')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'e', dep=1, rel='Comparison')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'e', dep=1, rel='Expansion')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'e', dep=1, rel='Temporal')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'i', dep=1, rel='Contingency')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'i', dep=1, rel='Comparison')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'i', dep=1, rel='Expansion')
mcnmr('gentextfiles/DDDSIGPAPERpenndepth1000/congoneeiErrorsPrecise.csv',
          'gentextfiles/DDDSIGPAPERpenndepth1000/typegoneeiErrorsPrecise.csv', 'i', dep=1, rel='Temporal')
