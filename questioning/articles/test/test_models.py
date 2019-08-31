from test_plus import TestCase
from questioning.articles.models import Article


class ArticleModelsTest(TestCase):
    def setUp(self) -> None:
        self.user = self.make_user("user01")
        self.article1 = Article.objects.create(
            user=self.user,
            title='first',
            content='first',
            tags='test1,test2'
        )
        self.article2 = Article.objects.create(
            user=self.user,
            title='second',
            content='second',
            tags='test1,test2',
            status='P'
        )


    def test_obj_instance(self):
        """测试实例是否为Article"""
        assert isinstance(self.article1, Article)
        assert isinstance(self.article2, Article)

    def test_return_values(self):
        """测试返回值"""
        assert Article.objects.get_published().count() == 1
        assert Article.objects.get_drafts().count() == 1
