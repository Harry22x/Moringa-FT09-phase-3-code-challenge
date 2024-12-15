from database.connection import get_db_connection
conn = get_db_connection()
CURSOR = conn.cursor()

class Magazine:
    all={}
    def __init__(self,name, category,id = None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.id}: {self.name}, {self.category}>'

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if(isinstance(value,str) and 1<len(value)<17):
            self._name = value
        else:
            raise Exception("Name must be a string of length greater than 0 and less than 17 and cannot be changed once instantiated")
        

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if(len(value)>0 and isinstance(value,str)):
            self._category = value
        else:
            raise Exception("Category must be a string of length greater than 0")


    def save(self):
        sql = """INSERT INTO magazines (name,category) VALUES (?,?)"""
        CURSOR.execute(sql,(self.name,self.category))
        conn.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls,name,category):
        magazine = cls(name,category)
        magazine.save()
        return magazine

    @classmethod
    def instance_from_db(cls, row):

        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2])
            magazine.id = row[0]
            cls.all[magazine.id] = magazine
        return magazine
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT *
            FROM magazines
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
                    INNER JOIN magazines ON magazines.id = articles.magazine_id
                    WHERE magazines.id = ?                """
            CURSOR.execute(sql, (self.id,))
            article_data = CURSOR.fetchall()
            return [Article(*article) for article in article_data] if article_data else []
                
        except Exception as e:
            print(f"Error retrieving article: {e}")
            return None       

    def contributors(self):

        from author import Author
        
        try:
            sql = """
                    SELECT DISTINCT authors.*
                    FROM authors
                    INNER JOIN articles ON articles.author_id = authors.id
                    INNER JOIN magazines ON articles.magazine_id = magazines.id
                    WHERE magazines.id = ?                """
            CURSOR.execute(sql, (self.id,))
            authors = CURSOR.fetchall()
            return [Author(*author) for author in authors] if authors else []
                
        except Exception as e:
            print(f"Error retrieving authors: {e}")
            return None

    def contributing_authors(self):
        from author import Author
        
        try:
            
            sql = """
                SELECT authors.*
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING COUNT(articles.id) > 2
            """
            CURSOR.execute(sql, (self.id,))
            author_data = CURSOR.fetchall()
            
            return [Author(*author) for author in author_data] if author_data else None
                    
        except Exception as e:
            print(f"Error retrieving contributing authors: {e}")
            return None




    



