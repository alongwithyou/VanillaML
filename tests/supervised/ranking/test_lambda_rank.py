import unittest

from vanilla_ml.supervised.ranking.lambda_rank import LambdaRank
from vanilla_ml.util import data_io
from vanilla_ml.util.metrics.ranking import ndcg


class TestLambdaRank(unittest.TestCase):

    def test_toy_data(self):
        train_X, test_X, train_y, test_y = data_io.get_ranking_train_test()
        print("train_X's shape = %s, train_y's shape = %s" % (train_X.shape, train_y.shape))
        print("test_X's shape = %s, test_y's shape = %s" % (test_X.shape, test_y.shape))

        layers = [100]
        rnk = LambdaRank(layers, batch_size=100, n_epochs=10, learning_rate=0.1)
        print("rnk: %s" % rnk)

        print("Fitting ...")
        rnk.fit(train_X, train_y)

        print("Predicting ...")
        pred_proba_y = rnk.rank_score(test_X)
        pred_y = rnk.rank(test_X)
        print("y = %s" % test_y)
        print("pred_proba_y = %s" % pred_proba_y)
        print("pred_y = %s" % pred_y)

        k = 5
        ndcg_score = ndcg(test_y, pred_proba_y, k)
        print("NDCG@%d = %g" % (k, ndcg_score))

        self.assertGreaterEqual(ndcg_score, 0.93)
