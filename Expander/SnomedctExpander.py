from Expander import Expander
from singletonConceptId import *

from pymedtermino.snomedct import *

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code returns the sentence passed as argument with concept expansion from SNOMEDCT ontology.
'''

logging.config.fileConfig('logging.ini')


class SnomedctExpander(Expander):
    def __init__(self, host='localhost'):
        super(SnomedctExpander, self).__init__('expand.snomed', host)

    '''
    The abstract method from the base class is implemeted here to return a string of the original sentence with
    expansion from SNOMEDCT.
    This method takes a string as input and returns the expanded string as output.
    '''

    def getExpansions(self, sentence):
        self.logger.info('In getExpansions function of SnomedctExpander')
        self.cache = SingletonSNOMEDCTCache.Instance().cache
        synonyms = []
        synonyms = sentence.strip().split()
        metaConcepts = self.getMetaConcepts(sentence)

        for mconcept in metaConcepts:
            try:
                for el in self.cache[mconcept]:
                    synonyms.append(el)
                self.logger.info('Found SNOMEDCT Cached Concept: ' + str(mconcept.preferred_name))
            except:
                try:
                    # a full text search is performed on the preferred names of the biomedical concepts
                    termSyns = []
                    prefName = mconcept.preferred_name
                    conceptSyns = SNOMEDCT.search(prefName)
                    for uconcept in conceptSyns:
                        for el in uconcept.terms:  # .terms is also possible for all synonyms
                            termSyns.append(el)
                            synonyms.append(el)
                    self.cache[mconcept] = termSyns
                    self.logger.info('Performed expansions using SNOMECT')
                except Exception as e:
                    self.logger.debug('Exception in SNOMEDCT Expansion ' + str(e))
                    pass
        # class method from Expander to stop the meta map instance that is running
        # self.stopMetaMap()
        listSynonyms = list(set(synonyms))
        # Returning the expanded sentence
        ExpandedSentence = ' '.join(listSynonyms)
        return ExpandedSentence


# Since the abstract method from the base class Expander is implemented, uncommenting the following lines will allow this code to run.
# Unit Testing to check the working of SnomedctExpander class
if __name__ == '__main__':
    instance = SnomedctExpander()
    print instance.getExpansions("John has cancer")
