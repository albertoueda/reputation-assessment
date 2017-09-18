# -*- coding: utf-8 -*-

import numpy as np
import sys

###############################################################################
# Params

method   = 'index'
#method   = 'volume'
instance = 'example'

if len(sys.argv) == 3:
    method   = sys.argv[1]
    instance = sys.argv[2]
else:
    print 'usage: ca.py (index|volume|test) <dir>'

###############################################################################
# Input

import pandas as pd
dfauthors = pd.read_csv('%s/author-hindex.csv' % instance)
dfareas   = pd.read_csv('%s/paper-areas.csv' % instance, index_col=0)

pubsfile = {}
with open('%s/pubsfile' % instance) as f:
    for line in f:
        if line.strip() != '' and line[0] != '\t':
            name = line.strip()
            pubsfile[name] = []
        else:
            pubsfile[name].append(line.strip())

papers   = dfareas.index.unique()
paperids = { p:i for i,p in enumerate(papers) }

areas   = dfareas.Area.unique()
areaids = { p:i for i,p in enumerate(areas) }

from scipy.sparse import coo_matrix

row,col,data = [],[],[]
for (i,name) in enumerate(dfauthors.Author):
    for paper in pubsfile[name]:
        row.append(i)
        col.append(paperids[paper])
        # ca-volume
        if method == 'volume':
            data.append(1)
        # ca-index
        elif method == 'index':
            data.append(dfauthors.iloc[i].HIndex)
S = coo_matrix((data, (row, col)), 
    shape=(dfauthors.shape[0], len(papers))).toarray()

row,col,data = [],[],[]
for paper in papers:
    _areas = dfareas.loc[paper].Area
    if type(_areas) == str: _areas = [_areas]
    else: _areas = _areas.tolist()
    for area in _areas:
        row.append(paperids[paper])
        col.append(areaids[area])
        data.append(1)
A = coo_matrix((data, (row, col)), 
    shape=(len(papers),len(areaids)), dtype=np.float32).toarray()

Asum = A.sum(1)
for j in range(A.shape[1]):
    A[:,j] = A[:,j]/Asum

Na = np.zeros((len(areaids),))
for (i,name) in enumerate(dfauthors.Author):
    for paper in pubsfile[name]:
        _areas = dfareas.loc[paper].Area
        if type(_areas) == str: _areas = [_areas]
        else: _areas = _areas.tolist()
        for area in _areas:
            Na[ areaids[area] ] += 1

###############################################################################
# Method

Sline = S.dot(A)

# Test/Validation
if method == 'test':
    Na = np.array([3,3,3])
    Sline = np.array([[10.,5.,1.],[50.,25.,5.],[1.,1.,6.]])

from collections import Counter
   
l = np.zeros(Sline.shape)
e = np.zeros(Sline.shape)
l.fill(np.nan)
e.fill(np.nan)

for j in range(Sline.shape[1]):

    c = Sline[:,j]
    counter = Counter(c)
    
    for i,v in enumerate(c):
        if v == 0: continue
        e[i,j] = counter[v]-1
    
    dl = {}
    s = 0
    for k,v in sorted(dict(counter).items()):
        if k == 0: continue
        dl[k] = s
        s += v
        
    for i,v in enumerate(c):
        if v == 0: continue
        l[i,j] = dl[v]

Pia = (l + 0.5*e) / Na
Pia[pd.isnull(Pia)]=0
Bi = Pia.argmax(1)

fblist = []
for a in range(Pia.shape[1]):
    fblist.append( sorted(zip(Pia[:,a],Sline[:,a])) )
def fb(a,p):
    xs = fblist[a]
    for k,v in xs[::-1]:
        #print p,v,k
        if p >= k: return v

f1 = np.array([ fblist[a][-1][1] for a in Bi ])

F = np.zeros(Sline.shape)
for i in range(F.shape[0]):
    f = np.array([ fb(Bi[i],p) for p in Pia[i] ])
    #print Pia[i]
    #print f
    F[i,:] = f #/ fb(Bi[i],1.0)
F[pd.isnull(F)]=0

score = F.sum(1) / f1

print '\n'.join(map(str,score))
