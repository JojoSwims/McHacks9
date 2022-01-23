#!/usr/bin/env python3

from get_reactions import *
import plotly.express as px
import pandas as pd

#Note that in the future, we will have to replace dataframe.append() with panda.concatenate()
#We will plot the data from most reactions to least reactions, so we need to sort the subreddits in that way:

def mergeSort(keys):
    if len(keys)==1:
        return keys
    mid = (len(keys)-1) // 2
    lst1 = mergeSort(keys[:mid+1])
    lst2 = mergeSort(keys[mid+1:])
    result = merge(lst1, lst2)
    return result

def merge(lst1, lst2):
    lst = []
    i = 0
    j = 0
    while(i<=len(lst1)-1 and j<=len(lst2)-1):
        if data[lst1[i]][0]<data[lst2[j]][0]:
            lst.append(lst1[i])
            i+=1
        else:
            lst.append(lst2[j])
            j+=1
    if i>len(lst1)-1:
        while(j<=len(lst2)-1):
            lst.append(lst2[j])
            j+=1
    else:
        while(i<=len(lst1)-1):
            lst.append(lst1[i])
            i+=1
    return lst

data=get_reactions_dic()
subreddits=mergeSort(list(data.keys()))

"""
react_values=[]
for sub in subreddits:
    react_values.append(data[sub][0])
"""
print(subreddits)
df=pd.DataFrame()
for sub in subreddits:
    if(data[sub][1]=='N/A'):
        color='neutral'
    elif(data[sub][1]>0.5):
        color='positive'
    else:
        color='negative'
    df=df.append({
        'subreddit': sub,
        'reactions': data[sub][0],
        'reaction sentiment':color}, ignore_index=True)



print(df)
fig = px.bar(df, x="reactions", y="subreddit", color='reaction sentiment', orientation='h',
		
		color_discrete_sequence=["grey", "red", "light green"],

		height=len(subreddits)*100,
		title='Reactions and feelings to the event ')

fig.update_layout(yaxis = { "categoryorder": "max ascending"})
#fig.update_layout(xaxis={'categoryorder':'max descending'})



fig.show()
""""
fig = go.Figure(go.Bar(
            x=react_values,
            y=subreddits,
            orientation='h'))
fig.show()
"""
