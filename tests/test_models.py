import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from models.database.setup import create_tables


class TestModels(unittest.TestCase):
    create_tables()


    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly","category")
        self.assertEqual(magazine.name, "Tech Weekly")
    
    def test_author_insert_db(self):
        pass

if __name__ == "__main__":
    unittest.main()
