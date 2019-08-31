import tempfile

from PIL import Image
from test_plus.test import TestCase
from django.urls import reverse
from django.test import override_settings

from questioning.articles.models import Article


def get_temp_img():
    """生成临时文件并打开"""
    size = (200, 200)
    color = (255, 0, 0, 0)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        image = Image.new("RGB", size, color)
        image.save(f, "PNG")
    return open(f.name, mode="rb")


class ArticlesViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = self.make_user()
        self.client.login(username="testuser", password="password")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="程序员梦工厂",
            status="P",
            user=self.user,
        )
        self.test_image = get_temp_img()

    def tearDown(self) -> None:
        self.test_image.close()

    def test_index_articles(self):
        """测试文章列表页"""
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)

    def test_error_404(self):
        """访问一篇不存在的文章"""
        response_no_page = self.client.get(reverse("articles:article", kwargs={"pk": "55"}))
        self.assertEqual(response_no_page.status_code, 404)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # 重写settings.py文件中MEDIA_ROOT
    def test_create_article(self):
        """测试文章创建成功后跳转"""
        response = self.client.post(reverse("articles:write_new"),
                                    {"title": "这是文章标题1",
                                     "content": "这是文章内容1",
                                     "tags": "测试",
                                     "status": "P",
                                     "image": self.test_image})
        assert response.status_code == 302


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_article(self):
        """测试草稿箱功能"""
        response = self.client.post(reverse("articles:write_new"),
                                    {"title": "草稿文章",
                                     "content": "草稿箱的文章",
                                     "tags": "测试",
                                     "status": "D",
                                     "image": self.test_image})
        resp = self.client.get(reverse("articles:drafts"))
        assert resp.status_code == 200
        assert response.status_code == 302
