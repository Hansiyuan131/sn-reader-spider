# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import NavItem, ArticleItem, AuthorItem


class JiemianSpider(CrawlSpider):
    name = 'jiemian'
    allowed_domains = ['jiemian.com']
    start_urls = ['https://www.jiemian.com/']

    rules = (
        # 文章列表爬取规则
        Rule(LinkExtractor(allow=r'.*/lists.+\d.html'),
             callback='parse_list', follow=True),

        # 文章规则
        Rule(LinkExtractor(allow=r'.*/article.*\d.html'),
             callback='parse_new', follow=False),

        # 文章作者规则
        Rule(LinkExtractor(allow=r'.*\?m=user.*id.*\d'),
             callback='parse_author', follow=False),

        # 视频规则
        Rule(LinkExtractor(allow=r'.*/video/.*html'),
             callback='parse_video', follow=False),

    )

    def parse_list(self, response):
        url = response.xpath("//div[@id='header-nav']/h2/a/@href").get()
        if url:
            if '_' in url:
                if 'index' in url:
                    p_nav_id = 1
                else:
                    p_nav_id = re.findall('.*lists.(.*\d)_1.html', url)[0]
            else:
                p_nav_id = re.findall('.*lists.(.*\d).html', url)[0]
            p_nav_name = response.xpath("//div[@id='header-nav']/h2/a/text()").get()
            p_nav_parent_id = 0
            p_nav_origin_url = url
            sub_list = response.xpath("//ul[@id='sub-nav']/li")

            if sub_list:
                for sub_nav in sub_list:
                    sub_url = sub_nav.xpath("./a/@href").get()
                    if 'video' in sub_url:
                        sub_nav_id = re.findall('.*lists.(.*\d)_1.html', sub_url)[0]
                    else:
                        sub_nav_id = re.findall('.*lists.(.*\d).html', sub_url)[0]
                    sub_nav_name = sub_nav.xpath("./a/text()").get()
                    sub_nav_parent_id = p_nav_id
                    sub_nav_origin_url = sub_url
                    item = NavItem(nav_id=sub_nav_id, nav_name=sub_nav_name,
                                   nav_parent_id=sub_nav_parent_id, nav_origin_url=sub_nav_origin_url)
                    yield item

            item = NavItem(nav_id=p_nav_id, nav_name=p_nav_name,
                           nav_parent_id=p_nav_parent_id, nav_origin_url=p_nav_origin_url)
            yield item

    def parse_new(self, response):
        nav_url = response.xpath("//div[@class='main-mate']/a/@href").get()
        if nav_url:
            nav_id = re.findall('.*lists.(.*\d).html', nav_url)
            tag_list = response.xpath("//div[@class='main-mate']/span")
            tags = []
            if tag_list:
                for tag in tag_list:
                    tag_url = tag.xpath("./a/@href").get()
                    if tag_url:
                        tag_id = re.findall('.*tags.*\d.*/(.*\d).html', tag_url)[0]
                        tag_name = tag.xpath("./a/text()").get()
                        tag_one = {
                            "id": tag_id,
                            "name": tag_name
                        }
                        tags.append(tag_one)
            article_url = response.url
            if article_url:
                article_id = re.findall('.*article.(.*\d).html', article_url)[0]
            article_name = response.xpath("//div[@class='article-header']/h1/text()").get()
            article_intro = response.xpath("//div[@class='article-header']/p/text()").get()

            author_url = response.xpath("//span[@class='author']/a/@href").get()
            if author_url:
                author_id = re.findall('.*id=(\d.*)', author_url)[0]
            publish_date = response.xpath("//div[@class='article-info']/p/span[2]").get()
            read_count = response.xpath("//span[@class='hit']/text()").get()
            news_source = response.xpath("//div[@class='article-info']/p/span[4]").get()
            article_content = response.xpath("//div[@class='article-content']").get()
            article_img_url = response.xpath("//div[@class='article-img']/img/@src").get()

            item = ArticleItem(nav_id=nav_id, tags=tags,
                               article_id=article_id, article_name=article_name,
                               article_intro=article_intro, author_id=author_id,
                               publish_date=publish_date, read_count=read_count,
                               news_source=news_source, article_content=article_content,
                               article_img_url=article_img_url)
            yield item
        else:
            pass

    def parse_author(self, response):
        url = response.xpath("//div[@class='author-name']/h3/a/@href").get()
        if url:
            if 'video' in url:
                pass
                author_id = re.findall('.*/user/(\d.*)/\d.*html', url)[0]
                author_name = response.xpath("//div[@class='author-name']/p/a/text()").get()
                author_identity = response.xpath("//div[@class='author-name']/p/span[2]/text()").get()
                author_vip = response.xpath("//div[@class='author-name']/p/span[1]/@class").get()
            else:
                author_id = re.findall('.*id=(\d.*)', url)[0]
                author_name = response.xpath("//div[@class='author-name']/h3/a/text()").get()
                author_identity = response.xpath("//div[@class='author-name']/h3/span[2]/text()").get()
                author_vip = response.xpath("//div[@class='author-name']/h3/span[1]/@class").get()
            author_info = response.xpath("//div[@class='author-info']/p/text()").get()
            author_avatar_url = response.xpath("//div[@class='author-avatar']/img/@src").get()
            item = AuthorItem(author_id=author_id, author_name=author_name,
                              author_info=author_info,
                              author_avatar_url=author_avatar_url,
                              author_identity=author_identity,
                              author_vip=author_vip)
            yield item
