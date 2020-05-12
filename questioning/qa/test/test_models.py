from test_plus.test import TestCase

from questioning.qa.models import Question, Answer


class QAModelsTest(TestCase):
    def setUp(self) -> None:
        self.user1 = self.make_user('admin01')
        self.user2 = self.make_user('admin02')
        self.q1 = Question.objects.create(
            user=self.user1,
            title='q1',
            content='q1',
            tags='t1,t2'
        )
        self.q2 = Question.objects.create(
            user=self.user1,
            title='q2',
            content='q2',
            has_answer=True,
            tags='t1,t2'
        )
        self.answer = Answer.objects.create(
            user=self.user1,
            question=self.q2,
            content='a2',
            is_answer=True
        )

    def test_can_vote_question(self):
        """测试给问题投票"""
        self.q1.votes.update_or_create(
            user=self.user1,
            defaults={'value': True}
        )
        self.q1.votes.update_or_create(
            user=self.user2,
            defaults={'value': True}
        )
        assert self.q1.total_votes() == 2


    def test_can_vote_answer(self):
        """测试给回答投票"""

