'''
Created on May 29, 2014

@author: sabir
'''

#from rscore_mongo import settings
from unidecode import unidecode
#AUTHFILE_PATH = settings.BASE_DIR + '/../venue/authorityfiles/'
import os
AUTHFILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../authorityfiles/'
import pandas as pd
dfqualis = {}


from unidecode import unidecode
import re
def normalize_title(title,lower=True):
    title = unidecode(title)
    if lower: title = title.lower()
    title = re.sub(r'\W+','-',title)
    title = title.strip('-')
    return title

def normalize_venue(venue,lower=True):
    venue = normalize_title(venue,False)
    venue = '-'+venue+'-'
    venue = re.sub(r'-[IVXLC]+-','-',venue,flags=re.I)
    if lower: venue = venue.lower()
    venue = re.sub(r'-\d+(a|o|st|nd|rd|th)-','-',venue)
    venue = re.sub(r'-(and|for|the)-','-',venue,flags=re.I)
    venue = '-'.join( filter(lambda token: len(token) > 2 , venue.split('-')) )
    venue = re.sub(r'\d+','-',venue)
    venue = re.sub(r'first|second|third|fourth|fifth|sixth|seventh|eigth|ninth|tenth\
        primeir[oa]|segund[oa]|terceir[oa]|quart[oa]|quint[oa]|sext[oa]|setim[oa]|oitav[oa]|non[oa]',
        '-',venue,flags=re.I)
    venue = re.sub(r'\W+','-',venue)
    venue = venue.strip('-')
    return venue


filename = AUTHFILE_PATH + 'qualis-computacao-conf.csv'
df = pd.read_csv(filename,sep='\t')
df['Key'] = df.Sigla.apply( lambda s : unidecode(s.strip('\xc2\xa0')).upper() )
print df.shape
print len(df.Sigla.unique())
dfqualis['dblp'] = df
dfqualis['dblp'].head(30)

filename = AUTHFILE_PATH + 'qualis-direito-manual.csv'
df = pd.read_csv(filename,sep='\t',header=None)
df.columns = 'ISSN Nome Class Area Status'.split()
#from venue.models import normalize_venue
df['Key'] = df.Nome.apply( lambda s : normalize_venue(unidecode(s.decode('utf8'))) )
print df.shape
dfqualis['direito'] = df
dfqualis['direito'].head(30)

filename = AUTHFILE_PATH + 'qualis-filosofia-manual.csv'
df = pd.read_csv(filename,sep='\t',header=None)
df.columns = 'ISSN Nome Class Area Status'.split()
#from venue.models import normalize_venue
df['Key'] = df.Nome.apply( lambda s : normalize_venue(unidecode(s.decode('utf8'))) )
print df.shape
dfqualis['filosofia'] = df
dfqualis['filosofia'].head(30)

filename = AUTHFILE_PATH + 'qualis-fisica-manual.csv'
df = pd.read_csv(filename,sep='\t',header=None)
df.columns = 'ISSN Nome Class Area Status'.split()
#from venue.models import normalize_venue
df['Key'] = df.Nome.apply( lambda s : normalize_venue(unidecode(s.decode('utf8'))) )
print df.shape
dfqualis['fisica'] = df
dfqualis['fisica'].head(30)




def get_qualis_data(areakey = 'dblp', col = 'Class', key = 'SIGIR'):
    if areakey == 'dblp':
        try: 
            df = dfqualis[areakey]
            row = df[df.Key==key.upper()]
            if len(row[col].values) != 1: return None
            value = row[col].values[0]
        except: 
            return None
        return value
    if areakey in 'direito filosofia fisica medicina'.split():
        try:
            df = dfqualis[areakey]
            row = df[df.Key==key]
            if len(row[col].values) != 1: return None
            value = row[col].values[0]
        except: 
            return None
        return value

#areakey = 'dblp'
#col = 'H-index'
#col = 'Class'
#key = 'SIGIR'
#get_qualis_data(areakey,col,key)








''' '''
filename = os.path.dirname(os.path.realpath(__file__)) + '/../metadata/dblp.csv'
dfdblp = pd.read_csv(filename,index_col='Key')
def get_cell_from_key_dblp(key='dblp:confs/sigir',cell='ShortName'):
    data = dfdblp[dfdblp.index==key]
    if data.shape[0] == 1:
        x = data.iloc[0][cell]
        if not pd.isnull(x):
            return x
    return None
def get_qualis_dblp(key):
    return get_cell_from_key_dblp(key,'Qualis')
#get_qualis_dblp('dblp:journals/siamcomp')
''' '''







