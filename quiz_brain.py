import catsim
import catsim.estimation
import catsim.initialization
import catsim.irt
import catsim.selection
import catsim.stopping
import catsim.cat
import numpy as np
import pandas as pd
import difficulty_bank

class QuizBrain:

    def __init__(self, questions):
        self.question_no = 0
        self.score = 0
        self.questions = questions
        self.current_question = None
        self.difficulty_matrix = difficulty_bank.difficulty_matrix
        self.estimator = catsim.estimation.NumericalSearchEstimator(method='golden2')
        self.stopping = catsim.stopping.MinErrorStopper(0.3)
        self.selector = catsim.selection.RandomesqueSelector(5)
        self.initializer = catsim.initialization.RandomInitializer(dist_type='normal', dist_params=(0,1))
        self.ability = self.initializer.initialize(index=0)
        self.question_index = 0
        self.response_vector = []
        self.administered_items = []
        self.ability_scores = []
        self.question_list = []

    def has_more_questions(self):
        return self.stopping.stop(index=0, administered_items=self.difficulty_matrix[self.administered_items], theta=float(self.ability))

    def next_question(self):
        """Get the next question by incrementing the question number"""
        self.question_index = self.selector.select(index=0, 
                                                   items=self.difficulty_matrix, 
                                                   administered_items=self.administered_items, 
                                                   est_theta=self.ability)
        self.administered_items.append(int(self.question_index))
        self.current_question = self.questions[self.question_index]
        self.question_list.append(self.question_no)
        self.question_no += 1
        q_text = self.current_question.question_text
        return f"{q_text}"

    def check_answer(self, user_answer):
        """Check the user's answer against the correct answer and maintain the score"""
        
        correct_answer = self.current_question.correct_answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            self.response_vector.append(True)
            self.ability_scores.append(self.ability)
            self.ability = self.estimator.estimate(index=0, items=self.difficulty_matrix,
                                                   administered_items=self.administered_items,
                                                   response_vector=self.response_vector,
                                                   est_theta=self.ability)
            return True
        else:
            self.response_vector.append(False)
            self.ability_scores.append(self.ability)
            self.ability = self.estimator.estimate(index=0, items=self.difficulty_matrix,
                                                   administered_items=self.administered_items,
                                                   response_vector=self.response_vector,
                                                   est_theta=self.ability)
            return False

    def get_score(self):
        """Get the number of correct answers, wrong answers, and score percentage."""

        wrong = self.question_no - self.score
        score_percent = int(self.score / self.question_no * 100)
        return (self.score, wrong, score_percent)