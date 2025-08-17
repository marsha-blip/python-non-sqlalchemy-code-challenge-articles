
class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._title = None
        self.author = author
        self.magazine = magazine
        self.title = title  
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        
        if self._title is not None:
            return
        if not isinstance(value, str):
            return
        if not (5 <= len(value) <= 50):
            return
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        from classes.many_to_many import Author
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from classes.many_to_many import Magazine
        if isinstance(value, Magazine):
            self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Author name must be a string.")
        if len(name.strip()) == 0:
            raise Exception("Author name must be longer than 0 characters.")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        
        return

    def articles(self):
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        cats = {a.magazine.category for a in self.articles()}
        return list(cats) if cats else None


class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            return
        if not (2 <= len(value) <= 16):
            return
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            return
        if len(value.strip()) == 0:
            return
        self._category = value

    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        return list({a.author for a in self.articles()})

    def article_titles(self):
        titles = [a.title for a in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        from collections import Counter
        counts = Counter(a.author for a in self.articles())
        qualified = [auth for auth, cnt in counts.items() if cnt > 2]
        return qualified if qualified else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        counts = {}
        for a in Article.all:
            counts[a.magazine] = counts.get(a.magazine, 0) + 1
        return max(counts, key=counts.get)


