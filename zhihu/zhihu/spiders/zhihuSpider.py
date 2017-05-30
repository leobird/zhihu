#!/usr/bin/python
# coding=utf-8
import cookielib
import json
import os
import re
import subprocess
import urllib2
from urlparse import urlsplit

import scrapy
import scrapy_splash
import time
from requests.cookies import RequestsCookieJar
from scrapy import FormRequest
from scrapy import Request
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from zhihu.items import QuestionItem, AnswerItem, PeopleItem, TopicItem
from zhihu.settings import DEFAULT_REQUEST_HEADERS
from zhihu.spiders.logManager import LogManager
from zhihu.spiders.zhihuLogin import zhihuLogin


class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    #account = "562302448@qq.com"
    #secret = "Lm19930803"
    account = "18652057762"
    secret = "19930803"
    getElementError=u'obtainError'

    rules = [
        Rule(LinkExtractor(allow='^https://www.zhihu.com/question/\d+/answer/\d+$'), callback='parse_answer',follow=True),
        Rule(LinkExtractor(allow='^https:##//www.zhihu.com/question/\d+$'), callback='parse_question',follow=True),
        Rule(LinkExtractor(allow='^https://www.zhihu.com/topic/\d+\S*$'), callback='parse_topic',follow=True),
        Rule(LinkExtractor(allow='^https://www.zhihu.com/lives/\d+$'), callback='parse_live',follow=True),
        Rule(LinkExtractor(allow='^https://www.zhihu.com/roundtable/\w+$'), callback='parse_roundtable',follow=True),
        Rule(LinkExtractor(allow='^https://www.zhihu.com/people/\S+$'), callback='parse_people',follow=True),
        Rule(LinkExtractor(allow='^https://www.zhihu.com/\S*$'),follow=True),
    ]

    def __init__(self,  *a,  **kwargs):
        loginCookie = cookielib.LWPCookieJar(filename=os.path.dirname(os.getcwd())+'\\zhihu\\zhihu\\config\\loginCookie')
        loginCookie.load(ignore_discard=True)
        self.cookies=loginCookie._cookies['.zhihu.com']['/']
        #self.cookies={}
        self.headers =DEFAULT_REQUEST_HEADERS
        super(CrawlSpider, self).__init__(*a, **kwargs)
        self._compile_rules()
        zhihuLogin()

    def start_requests(self):
        yield FormRequest('https://www.zhihu.com/question/26192324',
                          headers=self.headers,
                          cookies=self.cookies,
                          callback = self.afterLogin)#jump to login page

    def afterLogin(self,response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_answer(self, response):
        self.humanCheckIssue(response.url)
        print 'parse_answer     '+response.url
        item = AnswerItem()
        try:
            x = response.url.split('/')
            item['answerId']=response.url.split('/')[6]
        except:
            LogManager.writeToLog('parse_answer    '+response.url+':get answerId error')
        try:
            item['questionId']=response.url.split('/')[-3]
        except:
            item['questionId'] = self.getElementError
            LogManager.writeToLog('parse_answer    ' + response.url + ':get questionId error')
        try:
            item['answerAuthorId']=response.xpath('//div[@class="QuestionAnswer-content"]//a[@class="UserLink-link"]/@href').extract_first().split('/')[-1]
        except:
            item['answerAuthorId'] = u'匿名用户'
        try:
            item['likeNumber']=response.xpath('//div[@class="QuestionAnswer-content"]//button[@class="Button VoteButton VoteButton--up"]/text()').extract_first()
        except:
            item['likeNumber'] = self.getElementError
            LogManager.writeToLog('parse_answer    ' + response.url + ':get likeNumber error')
        try:
            item['answerCommentNumber']=re.findall(r"\d+\.?\d*", response.xpath('//div[@class="QuestionAnswer-content"]//button[@class="Button ContentItem-action Button--plain"]/text()').extract_first())[0]
        except:
            item['answerCommentNumber'] = u'0'
        yield item

        time.sleep(1)

    def parse_answer_fromApi(self,response):
        self.humanCheckIssue(response.url)
        print 'parse_answer     ' + response.url
        jsonResponse=json.loads(response.body)
        for eachAnswer in jsonResponse['data']:
            item = AnswerItem()
            try:
                item['answerId'] = str(eachAnswer['id'])
            except:
                LogManager.writeToLog('parse_answer_fromApi    ' + response.url + ':get answerId error')
            try:
                item['questionId'] = str(eachAnswer['question']['id'])
            except:
                item['questionId'] = str(self.getElementError)
            try:
                item['answerAuthorId'] = eachAnswer['author']['url_token']
                if item['answerAuthorId'] == '' :
                    item['answerAuthorId'] = u'匿名用户'
            except:
                item['answerAuthorId'] = u'匿名用户'
            try:
                item['likeNumber'] = str(eachAnswer['voteup_count'])
            except:
                item['likeNumber'] = self.getElementError
            try:
                item['answerCommentNumber'] = str(eachAnswer['comment_count'])
            except:
                item['answerCommentNumber'] = u'0'
            yield item

        time.sleep(1)

        if int(jsonResponse['paging']['totals']) > int(re.findall(r"\d+\.?\d*", jsonResponse['paging']['next'].split('&')[-2])[0]):
            yield Request(url=jsonResponse['paging']['next'], headers=self.headers,
                          cookies=self.cookies, callback=self.parse_answer_fromApi)


    def parse_question(self, response):
        self.humanCheckIssue(response.url)
        print 'parse_question   '+response.url
        item = QuestionItem()
        try:
            item['questionId']=response.url.split('/')[4]
        except:
            LogManager.writeToLog('parse_question    ' + response.url + ':get questionId error')
        try:
            item['questionTitle']=response.xpath('//h1[@class="QuestionHeader-title"]/text()').extract_first()
        except:
            item['questionTitle'] =self.getElementError
            LogManager.writeToLog('parse_question    ' + response.url + ':get questionTitle error')
        item['questionAuthorId'] = u"SystemWaitingInput"
        try:
            item['topicIdList']=','.join(map(lambda a: a.split('/')[-1], response.xpath('//a[@class="TopicLink"]/@href').extract()))
        except:
            item['topicIdList'] =self.getElementError
            LogManager.writeToLog('parse_question    ' + response.url + ':get topicIdList error')
        try:
            item['answerNumber']=re.findall(r"\d+\.?\d*", response.xpath('//*[@class="Card"]/div/div/*/span/text()').extract_first())[0]
        except:
            item['answerNumber'] =self.getElementError
            LogManager.writeToLog('parse_question    ' + response.url + ':get answerNumber error')
        try:
            followInfo = response.xpath('//*[@class="QuestionHeader-follow-status"]/div/div/*/div[@class="NumberBoard-value"]/text()').extract()
            item['followNumber'] =followInfo[0]
            item['scanNumber']=followInfo[1]
        except:
            item['followNumber'] =self.getElementError
            item['scanNumber'] =self.getElementError
            LogManager.writeToLog('parse_question    ' + response.url + ':get followNumber error')
            LogManager.writeToLog('parse_question    ' + response.url + ':get scanNumber error')
        try:
            item['questionCommentNumber']=re.findall(r"\d+\.?\d*",response.xpath('//*[@class="QuestionHeader-Comment"]/button/text()').extract_first())[0]
        except:
            item['questionCommentNumber'] =u'0'
            #LogManager.writeToLog('parse_question    ' + response.url + ':get questionCommentNumber error')
        try:
            item['foldAnswerNumber']=re.findall(r"\d+\.?\d*",response.xpath('//*[@class="CollapsedAnswers-bar"]/button/text()').extract_first())[0]
        except:
            item['foldAnswerNumber'] =u'0'
            #LogManager.writeToLog('parse_question    ' + response.url + ':get foldAnswerNumber error')
        yield item

        time.sleep(1)

        yield Request(url=self.createMoreAnswerUrl(item['questionId'],3),headers=self.headers,cookies=self.cookies, callback=self.parse_answer_fromApi)

    #def parse_questionLog(self, response):
    #    print 'parse_questionLog      '+response.url
    #    item = QuestionItem()
    #    try:
    #        item['questionId']=response.url.split('/')[-2]
    #    except:
    #        item['questionId'] =self.getElementError
    #    try:
    #        x=response.xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][last()]/div/a/@href').extract_first().split('/')[-1]
    #        item['questionAuthorId']=response.xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][last()]/div/a/@href').extract_first().split('/')[-1]
    #    except:
    #        item['questionAuthorId'] = self.getElementError

    def parse_topic(self, response):
        self.humanCheckIssue(response.url)
        print 'parse_topic      '+response.url
        item = TopicItem()
        try:
            item['topicId']=response.url.split('/')[4]
        except:
            LogManager.writeToLog('parse_topic    ' + response.url + ':get topicId error')
        try:
            item['topicName']=response.xpath('//div[@class="topic-info"]/div[@class="topic-name"]/h1/text()').extract_first()
        except:
            item['topicName'] =self.getElementError
        try:
            item['topicFollowedNumber']=response.xpath('//div[@class="zm-topic-side-followers-info"]/a/strong/text()').extract_first()
        except:
            item['topicFollowedNumber'] = self.getElementError
        try:
            item['topicDescription']=response.xpath('//div[@id="zh-topic-desc"]/div[@class="zm-editable-content"]/text()').extract_first()
        except:
            item['topicDescription'] = self.getElementError
        try:
            item['fatherTopic']=','.join(map(lambda a: a.split('/')[-1],response.xpath('//div[@id="zh-topic-side-parents-list"]/div/div/a[@class="zm-item-tag"]/@href').extract()))
        except:
            item['fatherTopic'] = self.getElementError
        try:
            item['childTopicList']=','.join(map(lambda a: a.split('/')[-1], response.xpath('//div[@id="zh-topic-side-children-list"]/div/div/a/@href').extract()))
        except:
            item['childTopicList'] = self.getElementError
        yield item

        time.sleep(1)

    #def parse_topic_forApi(self,response):
    #    offset = response.xpath("//div[@class='feed-item feed-item-hook']/@data-score")
    #    form_data = {
    #        'start': '0',
    #        'offse#t': offset
    #    }
    #    yield scrapy.FormRequest(url=response.url, formdata=form_data, headers=self.headers,cookies=self.cookies, callback=self.parse_topic_forApi)
#
    #    self._response_downloaded(response)

    def parse_live(self, response):
        print 'parse_live       '+response.url

    def parse_roundtable(self, response):
        print 'parse_roundtable '+response.url

    def parse_people(self, response):
        self.humanCheckIssue(response.url)
        print 'parse_people     '+response.url
        item = PeopleItem()
        try:
            item['peopleId'] = response.url.split('/')[4]
        except:
            LogManager.writeToLog('parse_people    ' + response.url + ':get peopleId error')
        try:
            item['peopleName'] = response.xpath('//span[@class="ProfileHeader-name"]/text()').extract_first()
        except:
            item['peopleName'] =self.getElementError
        try :
            if response.xpath('//svg[contains(@class, "Icon Icon--male")]'):
                item['peopleGender']=u'male'
            elif response.xpath('//svg[contains(@class, "Icon Icon--female")]'):
                item['peopleGender'] = u'female'
            else:
                item['peopleGender'] = u'unknown'
        except:
            item['peopleGender'] =self.getElementError
        try:
            item['peopleCarrier'] =u'unknown'
            item['peopleEducation'] = u'unknown'
            for i in range(len(response.xpath('//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"]'))):
                iconClass=response.xpath('//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"]['+str(i+1)+']/div/svg/@class').extract_first()
                if(iconClass=='Icon Icon--company'):
                    item['peopleCarrier']=' '.join(response.xpath('//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"]['+str(i+1)+']/text()').extract())
                elif(iconClass=='Icon Icon--education'):
                    item['peopleEducation'] = ' '.join(response.xpath('//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][' + str(i + 1) + ']/text()').extract())
        except:
            item['peopleCarrier'] =self.getElementError
            item['peopleEducation'] = self.getElementError
        try:
            item['answerNumber']=response.xpath('//div[@class="ProfileMain-header"]/ul/li[@aria-controls="Profile-answers"]/a/span/text()').extract_first()
        except:
            item['answerNumber'] =self.getElementError
        try:
            item['shareNumber'] = response.xpath('//div[@class="ProfileMain-header"]/ul/li[@aria-controls="Profile-posts"]/a/span/text()').extract_first()
            if item['shareNumber']==None:
                item['shareNumber'] = self.getElementError+'BecauseOfZhihuLayoutChange'
        except:
            item['shareNumber'] =self.getElementError
        try:
            item['questionNumber'] = response.xpath('//div[@class="ProfileMain-header"]/ul/li[@aria-controls="Profile-asks"]/a/span/text()').extract_first()
        except:
            item['questionNumber'] =self.getElementError
        try:
            item['collectionNumber'] = response.xpath('//div[@class="ProfileMain-header"]/ul/li[@aria-controls="Profile-collections"]/a/span/text()').extract_first()
        except:
            item['collectionNumber'] =self.getElementError
        try:
            for i in range(len(response.xpath('//div[@class="Profile-sideColumnItems"]/div[@class="Profile-sideColumnItem"]'))):
                iconClass=response.xpath('//div[@class="Profile-sideColumnItems"]/div[@class="Profile-sideColumnItem"]['+str(i+1)+']/div[@class="IconGraf"]/div/svg/@class').extract_first()
                if(iconClass=='Icon IconGraf-icon Icon--like'):
                    item['likeNumber']=re.findall(r"\d+\.?\d*",response.xpath('//div[@class="Profile-sideColumnItems"]/div[@class="Profile-sideColumnItem"][' + str(i + 1) + ']/div[@class="IconGraf"]/text()').extract_first())[0]
                    item['thanksNumber']=re.findall(r"\d+\.?\d*",response.xpath('//div[@class="Profile-sideColumnItems"]/div[@class="Profile-sideColumnItem"][' + str(i + 1) + ']/div[@class="Profile-sideColumnItemValue"]/text()').extract_first())[0]
                    item['collectedNumber']=re.findall(r"\d+\.?\d*",response.xpath('//div[@class="Profile-sideColumnItems"]/div[@class="Profile-sideColumnItem"][' + str(i + 1) + ']/div[@class="Profile-sideColumnItemValue"]/text()').extract_first())[1]
                else:
                    item['likeNumber'] =u''
                    item['thanksNumber'] =u''
                    item['collectedNumber'] =u''

        except:
            item['likeNumber'] =self.getElementError
            item['thanksNumber'] =self.getElementError
            item['collectedNumber'] =self.getElementError
        try:
            item['followPeopleNumber'] = response.xpath('//div[@class="Card FollowshipCard"]/div/a[1]/div[@class="NumberBoard-value"]/text()').extract_first()
        except:
            item['followPeopleNumber'] =self.getElementError
        try:
            item['followedPeopleNumber'] = response.xpath('//div[@class="Card FollowshipCard"]/div/a[2]/div[@class="NumberBoard-value"]/text()').extract_first()
        except:
            item['followedPeopleNumber'] =self.getElementError
        yield item

        time.sleep(1)

    def createMoreAnswerUrl(self,questionId,offset):
        return 'https://www.zhihu.com/api/v4/questions/'+questionId+'/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset='+str(offset)

    def humanCheckIssue(self,url):
        if(url=='https://www.zhihu.com/imhuman'):
            subprocess.call("pause", shell=True)