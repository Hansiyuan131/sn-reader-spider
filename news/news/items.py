# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    """
    新闻文章
    """
    nav_id = scrapy.Field()
    tags = scrapy.Field()

    article_id = scrapy.Field()
    article_name = scrapy.Field()
    article_intro = scrapy.Field()

    author_id = scrapy.Field()
    publish_date = scrapy.Field()
    read_count = scrapy.Field()
    news_source = scrapy.Field()
    article_content = scrapy.Field()
    article_img_url = scrapy.Field()


class AuthorItem(scrapy.Item):
    """
    作者
    """

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_vip = scrapy.Field()
    author_identity = scrapy.Field()
    author_info = scrapy.Field()
    author_avatar_url = scrapy.Field()


class NavItem(scrapy.Item):
    """
    分类
    """
    nav_id = scrapy.Field()
    nav_name = scrapy.Field()
    nav_parent_id = scrapy.Field()
    nav_origin_url = scrapy.Field()
