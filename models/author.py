
from database.connection import get_db_connection



conn = get_db_connection()
CURSOR = conn.cursor()

class Author:

    all ={}
    def __init__(self, name,id = None):
        self.id = id
        self.name = name
        self._name_set = True

    def __repr__(self):
        return f'<Author id: {self.id} {self.name}>'

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if (not (hasattr(self, '_name_set')) and isinstance(value,str) and len(value)>0 ):
            self._name = value
        else:
            raise Exception("Name must be a string of length greater than 0 and cannot be changed once instantiated")
    
    
    def save(self):
        sql = """INSERT INTO authors (name) VALUES (?)"""
        CURSOR.execute(sql,(self.name,))
        conn.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls,name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def instance_from_db(cls, row):

        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1])
            author.id = row[0]
            cls.all[author.id] = author
        return author

    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def articles(self):
        pass
        from article import Article
        
        try:
            sql = """
                    SELECT articles.*
                    FROM articles
                    INNER JOIN authors ON authors.id = articles.author_id
                    WHERE authors.id = ?                """
            CURSOR.execute(sql, (self.id,))
            article_data = CURSOR.fetchall()
            return [Article(*article) for article in article_data] if article_data else []
                
        except Exception as e:
            print(f"Error retrieving article: {e}")
            return None
        
    def magazines(self):
        pass
        from magazine import Magazine
        
        try:
            sql = """
                    SELECT DISTINCT magazines.*
                    FROM magazines
                    INNER JOIN articles ON articles.magazine_id = magazines.id
                    INNER JOIN authors ON articles.author_id = authors.id
                    WHERE authors.id = ?                """
            CURSOR.execute(sql, (self.id,))
            magazines = CURSOR.fetchall()
            return [Magazine(*magazines) for magazines in magazines] if magazines else []
                
        except Exception as e:
            print(f"Error retrieving magazines: {e}")
            return None

    def article_titles(self):
        
        try:
            sql = """
                SELECT articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """
            CURSOR.execute(sql, (self.id,))
            article_titles = CURSOR.fetchall()
            
            # Convert list of tuples to list of strings
            return [title[0] for title in article_titles] if article_titles else None
                    
        except Exception as e:
            print(f"Error retrieving article titles: {e}")
            return None

    










