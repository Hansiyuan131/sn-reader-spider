from scrapy.exporters import JsonLinesItemExporter
from news.items import NavItem, ArticleItem, AuthorItem

class NewsPipeline(object):
    def __init__(self):
        self.fp_article = open('article.json', 'wb')
        self.fp_author = open('author.json', 'wb')
        self.fp_navItem = open('navItem.json', 'wb')
        self.exporter_article = JsonLinesItemExporter(self.fp_article, ensure_ascii=False, encoding='utf-8')
        self.exporter_author = JsonLinesItemExporter(self.fp_author, ensure_ascii=False, encoding='utf-8')
        self.exporter_navItem = JsonLinesItemExporter(self.fp_navItem, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.exporter_article.export_item(item)
        if isinstance(item, AuthorItem):
            self.exporter_author.export_item(item)
        if isinstance(item, NavItem):
            self.exporter_navItem.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp_article.close()
        self.fp_author.close()
        self.fp_navItem.close()
