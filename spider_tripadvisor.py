#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-02-27 01:49:25
# Project: maotuying_comments

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.com/Restaurant_Review-g294212-d8548826-Reviews-TRB_Forbidden_City-Beijing.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[class*="title"]').items():
            self.crawl(each.attr.href, fetch_type='js', callback=self.detail_page)
            
        next = response.doc('.unified.ui_pagination .nav.next').attr.href
        self.crawl(next, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "abstract": response.doc('.noQuotes').eq(0).text(),
            "content": response.doc('.partial_entry').eq(0).text(),
            "user": response.doc('span[class="expand_inline scrname"]').eq(0).text(),
            "rate": response.doc('div[class="rating reviewItemInline"]>span[class*="ui_bubble_rating"]').eq(0).attr('class')[-2],
            "date": response.doc('span[class="ratingDate relativeDate"]').eq(0).attr.title          
        }
