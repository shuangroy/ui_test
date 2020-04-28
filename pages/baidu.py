#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @desc:测试页面实例
 @author: nancy
"""
from public.basepage import BasePage


class HomePage(BasePage):
    kw = ['id', 'kw']
    su = ['id', 'su']

    def type_search(self, text):
        self.type(self.kw, text)

    def send_submit_btn(self):
        self.click(self.su)
