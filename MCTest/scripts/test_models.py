import gensim
import dill
import model


word_model = gensim.models.Word2Vec.load_word2vec_format('../../../data/glove.6B.50d.txt')
data_set = dill.load(open('../../sharedObjects/dataSet_mc500_train.p', 'r'))

# reload(model)
m = model.Word2VecSentencePair(word_model)
print m.evaluate(data_set, ['Accuracy'])