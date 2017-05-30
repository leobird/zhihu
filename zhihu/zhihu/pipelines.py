# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

from zhihu.items import QuestionItem, AnswerItem, PeopleItem, TopicItem


class ZhihuPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user = 'root', passwd ='19930803', db = 'zhihu', host = 'localhost', charset = 'utf8', use_unicode = True)
        self.cursor = self.conn.cursor()
        # 清空表
        # self.cursor.execute('truncate table tablename;')
        # self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, QuestionItem):
            self.cursor.execute("insert into zhihu.question set QuestionId='%s',QuestionTitle='%s',QuestionAuthorId='%s',QuestionCommentNumber='%s',TopicIdList='%s',AnswerNumber='%s',FollowNumber='%s',ScanNumber='%s',FoldAnswerNumber='%s',CreateDateTime=now(),UpdateDateTime=now() on duplicate key update QuestionTitle='%s',QuestionAuthorId='%s',QuestionCommentNumber='%s',TopicIdList='%s',AnswerNumber='%s',FollowNumber='%s',ScanNumber='%s',FoldAnswerNumber='%s',UpdateDateTime=now(); "
                                % (
                                    item['questionId'],
                                    item['questionTitle'],
                                    item['questionAuthorId'],
                                    item['questionCommentNumber'],
                                    item['topicIdList'],
                                    item['answerNumber'],
                                    item['followNumber'],
                                    item['scanNumber'],
                                    item['foldAnswerNumber'],
                                    item['questionTitle'],
                                    item['questionAuthorId'],
                                    item['questionCommentNumber'],
                                    item['topicIdList'],
                                    item['answerNumber'],
                                    item['followNumber'],
                                    item['scanNumber'],
                                    item['foldAnswerNumber']))
            self.conn.commit()
            pass
        elif isinstance(item, AnswerItem):
            self.cursor.execute("insert into zhihu.answer set AnswerId='%s',QuestionId='%s',AnswerAuthorId='%s',LikeNumber='%s',AnswerCommentNumber='%s',CreateDateTime=now(),UpdateDateTime=now() on duplicate key update QuestionId='%s',AnswerAuthorId='%s',LikeNumber='%s',AnswerCommentNumber='%s',UpdateDateTime=now(); "
                                % (
                                    item['answerId'],
                                    item['questionId'],
                                    item['answerAuthorId'],
                                    item['likeNumber'],
                                    item['answerCommentNumber'],
                                    item['questionId'],
                                    item['answerAuthorId'],
                                    item['likeNumber'],
                                    item['answerCommentNumber'],
                                ))
            self.conn.commit()
            pass
        elif isinstance(item, PeopleItem):
            self.cursor.execute("insert into zhihu.people set PeopleId='%s',PeopleName='%s',PeopleGender='%s',PeopleCarrier='%s',PeopleEducation='%s',AnswerNumber='%s',ShareNumber='%s',QuestionNumber='%s',CollectionNumber='%s',LikeNumber='%s',ThanksNumber='%s',CollectedNumber='%s',FollowPeopleNumber='%s',FollowedPeopleNumber='%s',CreateDateTime=now(),UpdateDateTime=now() on duplicate key update PeopleName='%s',PeopleGender='%s',PeopleCarrier='%s',PeopleEducation='%s',AnswerNumber='%s',ShareNumber='%s',QuestionNumber='%s',CollectionNumber='%s',LikeNumber='%s',ThanksNumber='%s',CollectedNumber='%s',FollowPeopleNumber='%s',FollowedPeopleNumber='%s',UpdateDateTime=now(); "
                                % (
                                    item['peopleId'],
                                    item['peopleName'],
                                    item['peopleGender'],
                                    item['peopleCarrier'],
                                    item['peopleEducation'],
                                    item['answerNumber'],
                                    item['shareNumber'],
                                    item['questionNumber'],
                                    item['collectionNumber'],
                                    item['likeNumber'],
                                    item['thanksNumber'],
                                    item['collectedNumber'],
                                    item['followPeopleNumber'],
                                    item['followedPeopleNumber'],
                                    item['peopleName'],
                                    item['peopleGender'],
                                    item['peopleCarrier'],
                                    item['peopleEducation'],
                                    item['answerNumber'],
                                    item['shareNumber'],
                                    item['questionNumber'],
                                    item['collectionNumber'],
                                    item['likeNumber'],
                                    item['thanksNumber'],
                                    item['collectedNumber'],
                                    item['followPeopleNumber'],
                                    item['followedPeopleNumber'],
                                ))
            self.conn.commit()
            pass
        elif isinstance(item, TopicItem):
            self.cursor.execute("insert into zhihu.topic set TopicId='%s',TopicName='%s',TopicFollowedNumber='%s',TopicDescription='%s',FatherTopic='%s',ChildTopicList='%s',CreateDateTime=now(),UpdateDateTime=now() on duplicate key update TopicName='%s',TopicFollowedNumber='%s',TopicDescription='%s',FatherTopic='%s',ChildTopicList='%s',UpdateDateTime=now(); "
                                % (
                                    item['topicId'],
                                    item['topicName'],
                                    item['topicFollowedNumber'],
                                    item['topicDescription'],
                                    item['fatherTopic'],
                                    item['childTopicList'],
                                    item['topicName'],
                                    item['topicFollowedNumber'],
                                    item['topicDescription'],
                                    item['fatherTopic'],
                                    item['childTopicList'],
                                ))
            self.conn.commit()
            pass
        else:
            pass
        return item

    def select(self,tableName,columnName,columnValue):
        resultNumber=self.cursor.execute("SELECT * FROM zhihu.%s WHERE %s='%s'" % (tableName,columnName,columnValue))
        return resultNumber
