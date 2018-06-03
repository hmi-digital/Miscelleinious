# -*- coding: utf-8 -*-
from module import hindiNLP
def stemTokenize(text):
 t=hindiNLP.Processor(text)
 t.tokenize()
 return[t.generate_stem_words(w)for w in t.tokens]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
