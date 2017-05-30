# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    pass

class AnswerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answerId= scrapy.Field()
    questionId = scrapy.Field()
    answerAuthorId= scrapy.Field()
    likeNumber= scrapy.Field()
    answerCommentNumber= scrapy.Field()
    pass

class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    questionId = scrapy.Field()
    questionTitle= scrapy.Field()
    questionAuthorId= scrapy.Field()
    topicIdList= scrapy.Field()
    answerNumber= scrapy.Field()
    followNumber= scrapy.Field()
    scanNumber= scrapy.Field()
    questionCommentNumber= scrapy.Field()
    foldAnswerNumber= scrapy.Field()
    pass

class PeopleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    peopleId= scrapy.Field()
    peopleName = scrapy.Field()
    peopleGender=scrapy.Field()
    peopleCarrier= scrapy.Field()
    peopleEducation= scrapy.Field()
    answerNumber= scrapy.Field()
    shareNumber= scrapy.Field()
    questionNumber= scrapy.Field()
    collectionNumber= scrapy.Field()
    likeNumber= scrapy.Field()
    thanksNumber= scrapy.Field()
    collectedNumber= scrapy.Field()
    followPeopleNumber= scrapy.Field()
    followedPeopleNumber= scrapy.Field()
    pass

class TopicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topicId= scrapy.Field()
    topicName = scrapy.Field()
    topicFollowedNumber=scrapy.Field()
    topicDescription= scrapy.Field()
    fatherTopic= scrapy.Field()
    childTopicList= scrapy.Field()
    pass