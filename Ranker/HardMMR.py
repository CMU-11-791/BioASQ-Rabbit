from deiis.model import Question
from CoreMMR import CoreMMR

from nltk import sent_tokenize

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the implementation of Abstract method for BiRanker.
'''

# logging.config.fileConfig('logging.ini')


# Class that inherits the class CoreMMR which extends the abstract class BiRanker
class HardMMR(CoreMMR):
    # constructor to instantiate CoreMMR since we want to change certain class variables, which are shown as follows
    def __init__(self):
        super(HardMMR, self).__init__(route='mmr.hard', selected=1, alpha=0.5)
        self.mmrInstance = CoreMMR()
        self.mmrInstance.numSelectedSentences = 1
        self.mmrInstance.pos_dict = {}
        self.mmrInstance.alpha = 0.5
        # self.pos_dict = {}

    # abstract method that takes a question and returns a string
    def getRankedList(self, question):
        selectedSentences = []
        # snippets = question['snippets']
        self.beta = 0
        snippet = unicode(question.snippets[0].text).encode("ascii", "ignore")  # first snippet
        sentences = [i.lstrip().rstrip() for i in sent_tokenize(snippet)]

        # selecting 1 sentence from the first snippet
        selected_sents = self.mmrInstance.getRankedList(question)

        summary = selected_sents[0]
        leftover = set(sentences).difference(set(selected_sents))

        for snippet in question.snippets[1:]:
            snippet = unicode(snippet.text).encode("ascii", "ignore")
            more_sentences = [i.lstrip().rstrip() for i in sent_tokenize(snippet)]
            leftover = leftover.union(set(more_sentences))
        # selecting the remaining 9 sentences from the leftover
        self.mmrInstance.sentences = list(leftover)
        # The class variable that is set to 1 in the constructor is changed here
        self.mmrInstance.numSelectedSentences = 9
        selected_sents = self.mmrInstance.getRankedList(question)
        self.logger.info('Performed Hard Constrainted MMR')
        return selected_sents


# Unit Testing to check the working of CoreMMR class
if __name__ == '__main__':
    data = {u'body': u'What is the association of estrogen replacement therapy and intracranial meningioma risk?', u'documents': [u'http://www.ncbi.nlm.nih.gov/pubmed/25335165', u'http://www.ncbi.nlm.nih.gov/pubmed/23101448', u'http://www.ncbi.nlm.nih.gov/pubmed/22287638', u'http://www.ncbi.nlm.nih.gov/pubmed/21067422', u'http://www.ncbi.nlm.nih.gov/pubmed/20738039', u'http://www.ncbi.nlm.nih.gov/pubmed/20091865', u'http://www.ncbi.nlm.nih.gov/pubmed/20730482', u'http://www.ncbi.nlm.nih.gov/pubmed/17580362', u'http://www.ncbi.nlm.nih.gov/pubmed/16759391', u'http://www.ncbi.nlm.nih.gov/pubmed/16570277', u'http://www.ncbi.nlm.nih.gov/pubmed/15006250'], u'type': u'summary', u'id': u'56bf3a79ef6e39474100000f', u'snippets': [{u'offsetInBeginSection': 1178, u'offsetInEndSection': 1814, u'text': u'The meta-analyses yielded significantly increased risks for all CNS tumors, glioma and meningioma in users of estrogen-only [1.35 (1.22-1.49), 1.23 (1.06-1.42) and 1.31 (1.20-1.43), respectively] but not estrogen-progestin HT [1.09 (0.99-1.19), 0.92 (0.78-1.08) and 1.05 (0.95-1.16), respectively]; these differences were statistically significant (p<0.005 for each tumor type). There was no significant difference between glioma and meningioma risk in users of estrogen-only HT. The totality of the available evidence suggests an increased risk of all CNS tumors (and of glioma and meningioma separately) in users of estrogen-only HT. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/25335165', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1009, u'offsetInEndSection': 1310, u'text': u'Among premenopausal women, current use of oral contraceptives was associated with an increased risk of meningiomas (OR 1.8, 95% CI 1.1-2.9), while current use of hormone replacement therapy among postmenopausal women was not associated with a significant elevation in risk (OR 1.1, 95% CI 0.74-1.67). ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/23101448', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1610, u'offsetInEndSection': 1838, u'text': u'The relationship between current use of exogenous hormones and meningioma remains unclear, limited by the small numbers of patients currently on oral hormone medications and a lack of hormone receptor data for meningioma tumors.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/23101448', u'endSection': u'abstract'}, {u'offsetInBeginSection': 682, u'offsetInEndSection': 1052, u'text': u'Ever use of estradiol-only therapy was associated with an increased risk of meningioma (standardized incidence ratio = 1.29, 95% confidence interval: 1.15, 1.44). Among women who had been using estradiol-only therapy for at least 3 years, the incidence of meningioma was 1.40-fold higher (95% confidence interval: 1.18, 1.64; P<0.001) than in the background population. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/22287638', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1291, u'offsetInEndSection': 1375, u'text': u'Estradiol-only therapy was accompanied with a slightly increased risk of meningioma.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/22287638', u'endSection': u'abstract'}, {u'offsetInBeginSection': 245, u'offsetInEndSection': 447, u'text': u'Results from several prospective, large-scale studies indicate that postmenopausal hormone therapy may increase the risk for diagnosing meningioma by 30-80%, but there is no effect in regard to glioma. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/21067422', u'endSection': u'abstract'}, {u'offsetInBeginSection': 0, u'offsetInEndSection': 232, u'text': u'A retrospective study including more than 350,000 women, about 1400 of whom had developed meningioma, showed that the risk of meningioma was about twice as high in users of postmenopausal hormone replacement therapy as in non-users.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20738039', u'endSection': u'abstract'}, {u'offsetInBeginSection': 486, u'offsetInEndSection': 870, u'text': u'Compared with never users of HRT, the relative risks (RRs) for all incident CNS tumours, gliomas, meningiomas and acoustic neuromas in current users of HRT were 1.20 (95% CI: 1.05-1.36), 1.09 (95% CI: 0.89-1.32), 1.34 (95% CI: 1.03-1.75) and 1.58 (95% CI: 1.02-2.45), respectively, and there was no significant difference in the relative risks by tumour type (heterogeneity p = 0.2). ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20091865', u'endSection': u'abstract'}, {u'offsetInBeginSection': 0, u'offsetInEndSection': 134, u'text': u'BACKGROUND: Previous studies on association of exogenous female sex hormones and risk for meningioma have yielded conflicting results.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20730482', u'endSection': u'abstract'}, {u'offsetInBeginSection': 999, u'offsetInEndSection': 1131, u'text': u'RESULTS: Postmenopausal hormonal treatment, use of contraceptives, or fertility treatment did not influence the risk of meningioma. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20730482', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1418, u'offsetInEndSection': 1549, u'text': u'CONCLUSIONS: Overall, we found little indication that reproductive factors or use of exogenous sex hormones affect meningioma risk.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/20730482', u'endSection': u'abstract'}, {u'offsetInBeginSection': 813, u'offsetInEndSection': 954, u'text': u'Although not definitive, available data suggest an association between the use of hormone replacement therapy and increased meningioma risk. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/17580362', u'endSection': u'abstract'}, {u'offsetInBeginSection': 0, u'offsetInEndSection': 208, u'text': u'BACKGROUND: The role of exogenous hormone exposures in the development of meningioma is unclear, but these exposures have been proposed as one hypothesis to explain the over-abundance of such tumors in women.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/16759391', u'endSection': u'abstract'}, {u'offsetInBeginSection': 613, u'offsetInEndSection': 812, u'text': u'RESULTS: Although risk of meningioma appeared modestly elevated in past OC users (OR = 1.5, 95% CI 0.8 - 2.7), and in current users (OR = 2.5, 95% CI 0.5 - 12.6), the confidence intervals were wide. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/16759391', u'endSection': u'abstract'}, {u'offsetInBeginSection': 897, u'offsetInEndSection': 1073, u'text': u'Likewise, risk of meningioma was only weakly associated with past use of HRT (OR = 0.7, 95% CI 0.4 - 1.3), and not at all with current use of HRT (OR = 1.0, 95% CI 0.5 - 2.2). ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/16759391', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1318, u'offsetInEndSection': 1716, u'text': u' Overall, in post menopausal women, HRT use appeared to confer a non-significant protective effect, and was not associated with low or high PR expressing meningiomas.CONCLUSION: This study found little evidence of associations between meningioma and exogenous hormone exposures in women but did suggest that some hormonal exposures may influence tumor biology in those women who develop meningioma.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/16759391', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1276, u'offsetInEndSection': 1608, u'text': u'The increased odds ratios with African Americans was retained in post-menopausal women, while the protective odds ratios for pregnancy, smoking and oral contraceptives (OCs) became stronger in pre-menopausal women. The pattern by duration and timing of use does not suggest an etiologic role for OCs or hormone replacement therapy. ', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/16570277', u'endSection': u'abstract'}, {u'offsetInBeginSection': 1044, u'offsetInEndSection': 1221, u'text': u'The use of hormone replacement therapy in symptomatic postmenopausal women either with previously treated disease or with dormant tumors is discussed, but remains controversial.', u'beginSection': u'abstract', u'document': u'http://www.ncbi.nlm.nih.gov/pubmed/15006250', u'endSection': u'abstract'}]}
    question = Question(data)
    sci = HardMMR()
    sentences = sci.getRankedList(question)
    print 'Q. ' + question.body
    for i,s in enumerate(sentences):
        print "{}. {}".format(i,s)
