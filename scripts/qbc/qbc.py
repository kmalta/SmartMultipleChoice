import sys
sys.path.append('../')
sys.path.append('./')
import answerer
from answerer import AnswerStrategy, BaselineStrategy, BaselineRandomStrategy, NaiveStrategy, KeywordEqualWeightStrategy
from answerer import KeywordConfidenceStrategy, TopicWeightedKeywordSumStrategy, TopicWeightedNaiveSumStrategy
from answerer import Doc2VecStrategy, RelevancySortingStrategy
from evaluate import EvaluateStrategy

strategy_classes = [
'NaiveStrategy',
#'Doc2VecStrategy',
'KeywordEqualWeightStrategy',
'KeywordConfidenceStrategy',
'TopicWeightedKeywordSumStrategy',
'TopicWeightedNaiveSumStrategy',
'RelevancySortingStrategy',
]


class QueryByCommitteeKOTH(AnswerStrategy):

    def __init__(self, strategies, data_set_obj, model):
        AnswerStrategy.__init__(self, data_set_obj, model)
        self.strategy_list = strategies
        self.make_evaluate_classes(data_set_obj, model)

    def make_evaluate_classes(self, data_set_obj, model):
        evaluate_classes = []
        for strategy in self.strategy_list:
            strat_class = getattr(answerer, strategy)
            obj = strat_class(data_set_obj, model)
            eval_obj = EvaluateStrategy(obj)
            evaluate_classes.append(eval_obj)
        self.evaluate_classes = evaluate_classes

    def train(self, data_set_obj):
        max_type = {}
        max_idx = {}
        max_type['question'] = 0
        max_type['statement'] = 0
        max_type['answer_finisher'] = 0
        max_idx['question'] = -1
        max_idx['statement'] = -1
        max_idx['answer_finisher'] = -1
        idx = 0
        for obj in self.evaluate_classes:
            obj.run_evaluation(data_set_obj)
            if obj.question_type_accuracy > max_type['question']:
                max_type['question'] = obj.question_type_accuracy
                max_idx['question']  = idx
            if obj.statement_type_accuracy > max_type['statement']:
                max_type['statement'] = obj.statement_type_accuracy
                max_idx['statement']  = idx
            if obj.answer_finisher_type_accuracy > max_type['answer_finisher']:
                max_type['answer_finisher'] = obj.answer_finisher_type_accuracy
                max_idx['answer_finisher'] = idx
            idx += 1
        self.max_type = max_type
        self.max_idx = max_idx

    def answer(self, question_class):
        return self.evaluate_classes[self.max_idx[question_class.type]].strategy.answer(question_class)





class QueryByCommitteeWeighted(AnswerStrategy):

    def __init__(self, strategies, data_set_obj, model):
        AnswerStrategy.__init__(self, data_set_obj, model)
        self.strategy_list = strategies
        self.make_evaluate_classes(data_set_obj, model)

    def make_evaluate_classes(self, data_set_obj, model):
        evaluate_classes = []
        for strategy in self.strategy_list:
            strat_class = getattr(answerer, strategy)
            obj = strat_class(data_set_obj, model)
            eval_obj = EvaluateStrategy(obj)
            evaluate_classes.append(eval_obj)
        self.evaluate_classes = evaluate_classes

    def train(self, data_set_obj):
        accuracy_array = {}
        accuracy_array['question'] = []
        accuracy_array['statement'] = []
        accuracy_array['answer_finisher'] = []

        for obj in self.evaluate_classes:
            obj.run_evaluation(data_set_obj)
            accuracy_array['question'].append(obj.question_type_accuracy)
            accuracy_array['statement'].append(obj.statement_type_accuracy)
            accuracy_array['answer_finisher'].append(obj.answer_finisher_type_accuracy)

        self.accuracy_array = accuracy_array

    def answer(self, question_class):
        answer_values = [0,0,0,0]
        answer_option = ['A', 'B', 'C', 'D']
        idx = 0
        for value in self.accuracy_array[question_class.type]:
            answer_values[answer_option.index(self.evaluate_classes[idx].strategy.answer(question_class))] += value
            idx += 1

        return ['A', 'B', 'C', 'D'][answer_values.index(max(answer_values))]
