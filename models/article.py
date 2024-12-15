


from database.setup import get_db_connection
conn = get_db_connection()
CURSOR = conn.cursor()

class Article:
    all={}
    def __init__(self, title, content, author_id, magazine_id,id = None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._title_set = True

    def __repr__(self):
        return f'<Article id: {self.id} {self.title}, {self.content}, {self.author_id}, {self.magazine_id}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if (not hasattr(self, '_title_set') and isinstance(value, str) and 4<len(value)<51):
            self._title = value
        else:
             raise Exception("Title must be a string of length greater than 4 and less than 51 and cannot be changed once instantiated")
    

    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        from author import Author
        if (isinstance(author_id,int) and Author.find_by_id(author_id)):
            self._author_id = author_id
        else:
            raise ValueError("Author ID must reference an author in the authors database")   

    @property
    def magazine_id(self):
        return self._magazine_id
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        from magazine import Magazine
        if (isinstance(magazine_id,int) and Magazine.find_by_id(magazine_id)):
            self._magazine_id = magazine_id
        else:
            raise ValueError("Magazine ID must reference a magazine in the database") 



    def save(self):
        sql = """INSERT INTO articles (title,content,author_id,magazine_id) VALUES (?,?,?,?)"""
        CURSOR.execute(sql,(self.title,self.content,self.author_id,self.magazine_id))
        conn.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls,title,content,author_id,magazine_id):
        article = cls(title,content,author_id,magazine_id)
        article.save()
        return article

   
    
    def article_author(self):
        from author import Author
        
        try:
            sql = """
                    SELECT authors.*
                    FROM authors
                    INNER JOIN articles ON articles.author_id = authors.id
                    WHERE articles.id = ?                """
            CURSOR.execute(sql, (self.id,))
            author_data = CURSOR.fetchone()
            return Author(*author_data) if author_data else None
        except Exception as e:
            print(f"Error retrieving author: {e}")
            return None

    def article_magazine(self):
        from magazine import Magazine
        
        try:
            sql = """
                    SELECT magazines.*
                    FROM magazines
                    INNER JOIN articles ON articles.magazine_id = magazines.id
                    WHERE articles.id = ?                """
            CURSOR.execute(sql, (self.id,))
            magazine_data = CURSOR.fetchone()
            return Magazine(*magazine_data) if magazine_data else None
        except Exception as e:
            print(f"Error retrieving author: {e}")
            return None






