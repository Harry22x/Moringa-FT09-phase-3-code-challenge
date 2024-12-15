#Personal code testing.(IGNORE)

from author import Author
from magazine import Magazine
from article import Article

# author1 = Author.create("Bob")
# author2 = Author.create("Alice")
# author3 = Author.create("John")

# magazine1 = Magazine.create('Tech Monthly', 'Technology')
# magazine2 = Magazine.create('Health Weekly', 'Health')

# article1 = Article.create('AI Revolution','Content about AI', 1, 1)
# article2 = Article.create('Healthy Living Tips', 'Content about health', 2, 2)
# article3 = Article.create('Advanced AI Techniques', 'Content about advanced AI', 1, 1)
# article4 = Article.create('Health Benefits of Running', 'Running is beneficial', 2, 2)




# Fetch author with id 1 and list their articles
author = Author.find_by_id(1)
print(author.articles())

# Fetch magazines an author has contributed to
print(author.magazines())

# Fetch magazine with id 1 and list its articles
magazine = Magazine.find_by_id(1)
print(magazine.articles())

# List contributors for a specific magazine
print(magazine.contributors())

# Get contributing authors (those with more than 2 articles for a magazine)
print(magazine.contributing_authors())
 
# print(article1.article_author())

# print(article2.article_magazine())