import pandas as pd

def errorrate(file):
    m = pd.read_csv(file,index_col=0)
    sum = m.loc[['sum'],[col for col in m.columns]].sum(axis=1)
    m['summed sums'] = sum
    sumerrors = m.loc[['Mispredicted_Explicit','Explicit_Sister','Mispredicted_Implicit'],[col for col in m.columns]].sum(axis=1)
    m['summed errors'] = sumerrors
    MispredictedExp = m.at['Mispredicted_Explicit','summed errors']
    ExplicitSister = m.at['Explicit_Sister','summed errors']
    MispredictedEXP = MispredictedExp - ExplicitSister
    MispredictedIMP = m.at['Mispredicted_Implicit','summed errors']
    print('MispredictedNONSISTER:',MispredictedEXP,'/',m.at['sum','summed sums'],'=',MispredictedEXP/m.at['sum','summed sums'])
    print('MispredictedIMP:',MispredictedIMP,'/',m.at['sum','summed sums'],'=',MispredictedIMP/m.at['sum','summed sums'])
    print('-------------------------------')
    con = m.loc[['Mispredicted_Explicit','Explicit_Sister','Mispredicted_Implicit','sum'],[' Contingency_Cause_Result ',' Contingency_Cause_Reason ',' Contingency_Cause+Belief_Reason+Belief ',' Contingency_Cause+SpeechAct_Reason+SpeechAct ', ' Contingency_Cause+Belief_Result+Belief ',' Contingency_Cause+SpeechAct_Result+SpeechAct ']]
    con['Contingency_Cause'] = con.sum(axis=1)
    print('Contingency_Cause')
    print('Mispredicted_Nonsister:', con.at['Mispredicted_Explicit','Contingency_Cause'] - con.at['Explicit_Sister','Contingency_Cause'], '/',con.at['sum','Contingency_Cause'],'=',(con.at['Mispredicted_Explicit','Contingency_Cause'] - con.at['Explicit_Sister','Contingency_Cause'])/con.at['sum','Contingency_Cause'])
    print('Mispredicted_Implicit:',con.at['Mispredicted_Implicit','Contingency_Cause'],'/',con.at['sum','Contingency_Cause'],'=',con.at['Mispredicted_Implicit','Contingency_Cause'] / con.at['sum','Contingency_Cause'],'\n--------------------------')
    com = m.loc[['Mispredicted_Explicit','Explicit_Sister','Mispredicted_Implicit','sum'],[' Comparison_Contrast ',' Comparison_Concession_Arg2-as-denier ',' Comparison_Concession_Arg1-as-denier ',' Comparison_Similarity ',' Comparison_Concession+SpeechAct_Arg2-as-denier+SpeechAct ']]
    com['Comparison'] = com.sum(axis=1)
    print('Comparison')
    print('Mispredicted_Nonsister:',
          com.at['Mispredicted_Explicit', 'Comparison'] - com.at['Explicit_Sister', 'Comparison'],'/',com.at['sum','Comparison'],'=',(com.at['Mispredicted_Explicit', 'Comparison'] - com.at['Explicit_Sister','Comparison'])/com.at['sum','Comparison'])
    print('Mispredicted_Implicit:', com.at['Mispredicted_Implicit', 'Comparison'],'/',com.at['sum','Comparison'],'=',com.at['Mispredicted_Implicit', 'Comparison'] / com.at['sum','Comparison'],'\n--------------------------')
    exp = m.loc[['Mispredicted_Explicit','Explicit_Sister','Mispredicted_Implicit','sum'],[' Expansion_Instantiation_Arg2-as-instance ']]
    exp['Expansion_Instantiation'] = exp.sum(axis=1)
    print('Expansion_Instantiation')
    print('Mispredicted_Nonsister:',
          exp.at['Mispredicted_Explicit', 'Expansion_Instantiation'] - exp.at['Explicit_Sister', 'Expansion_Instantiation'],'/',exp.at['sum','Expansion_Instantiation'],'=',(exp.at['Mispredicted_Explicit', 'Expansion_Instantiation'] - exp.at['Explicit_Sister', 'Expansion_Instantiation'])/exp.at['sum','Expansion_Instantiation'])
    print('Mispredicted_Implicit:', exp.at['Mispredicted_Implicit', 'Expansion_Instantiation'],'/',exp.at['sum','Expansion_Instantiation'],'=',exp.at['Mispredicted_Implicit', 'Expansion_Instantiation']/exp.at['sum','Expansion_Instantiation'],'\n--------------------------')
    tem = m.loc[['Mispredicted_Explicit','Explicit_Sister','Mispredicted_Implicit','sum'],[' Temporal_Asynchronous_Succession ',' Temporal_Asynchronous_Precedence ']]
    tem['Temporal_Asynchronous'] = tem.sum(axis=1)
    print('Temporal_Asynchronous')
    print('Mispredicted_Nonsister:',
          tem.at['Mispredicted_Explicit', 'Temporal_Asynchronous'] - tem.at['Explicit_Sister', 'Temporal_Asynchronous'],'/',tem.at['sum','Temporal_Asynchronous'],'=',(tem.at['Mispredicted_Explicit', 'Temporal_Asynchronous'] - tem.at['Explicit_Sister', 'Temporal_Asynchronous'])/tem.at['sum','Temporal_Asynchronous'])
    print('Mispredicted_Implicit:', tem.at['Mispredicted_Implicit', 'Temporal_Asynchronous'],'/',tem.at['sum','Temporal_Asynchronous'],'=',tem.at['Mispredicted_Implicit', 'Temporal_Asynchronous']/tem.at['sum','Temporal_Asynchronous'],'\n--------------------------')
print('D-')
errorrate('../gentextfiles/20211124penndepth1000/submit20211124typegonemetrics.csv')
print('D+')
errorrate('../gentextfiles/20211124penndepth1000/submit20211124congonemetrics.csv')

