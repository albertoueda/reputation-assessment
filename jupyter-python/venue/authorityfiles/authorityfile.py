'''
Created on May 27, 2014

@author: sabir
'''

class AuthorityFile:

    _canonical = {}
    
    def __init__(self,filename):
        
        with open(filename) as f:
            blocks = f.read().split('\n\n')
            for block in blocks:
                lines = block.split('\n')
                firstline = lines[0].strip()
                for line in lines[1:]:
                    self._canonical[line.strip()] = firstline
                    
        #print self._canonical
    
    def canonical(self,text):
        _text = text.strip()
        #print _text
        if self._canonical.has_key(_text): return self._canonical[_text]
        return _text 

from rscore_mongo import settings
authorityfiles = {}
authorityfiles['computacao'] = AuthorityFile(settings.BASE_DIR + '/../venue/authorityfiles/computacao.txt')
authorityfiles['direito'] = AuthorityFile(settings.BASE_DIR + '/../venue/authorityfiles/direito.txt')
authorityfiles['filosofia'] = AuthorityFile(settings.BASE_DIR + '/../venue/authorityfiles/filosofia.txt')
