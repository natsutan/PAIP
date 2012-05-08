# -*- coding: utf-8 -*-
from gps import *

house_ops = (
    operator(u'寝る',
             (u'家事done', u'消灯done',),
             (u'おやすみ',)),
    operator(u'消灯完了',
             (u'TV消すdone', u'空調切るdone',u'電気消すdone'),
             (u'消灯done')),
    operator(u'TV消す',
             (u'TVついてる',),
             (u'TV消すdone',),
             (u'TVついてる')),
    operator(u'空調消す',
             (u'空調ついてる',),
             (u'空調切るdone',),
             (u'空調ついてる')),
    operator(u'電気消す',
             (u'電気ついてる',),
             (u'電気消すdone',),
             (u'電気ついてる')),
    operator(u'家事完了',
             (u'洗い物done', u'洗濯物done', u'明日のご飯done'),
             (u'家事done',)),
    operator(u'洗い物する',
             (u'洗い物残ってる',),
             (u'洗い物done',),
             (u'洗い物残ってる',)),
    operator(u'明日のご飯作る',
             (u'ご飯が無い',),
             (u'明日のご飯done',),
             (u'ご飯が無い',)),
    operator(u'洗濯物完了',
             (u'洗濯物取り入れdone', u'洗濯物たたむdone', u'洗濯done', u'洗濯物干すdone'),
             (u'洗濯物done',),
             (u'洗濯物残ってる',)),
    operator(u'洗濯物取り入れる',
             (u'洗濯物取り入れてない',),
             (u'洗濯物取り入れdone',),
             (u'洗濯物取り入れてない',)),
    operator(u'洗濯物たたむ',
             (u'洗濯物たためてない',),
             (u'洗濯物たたむdone',),
             (u'洗濯物たためてない',)),
    operator(u'洗濯機を回す',
             (u'洗濯できてない',),
             (u'洗濯done',),
             (u'洗濯できてない',)),
    operator(u'洗濯物干す',
             (u'洗濯物干せてない',),
             (u'洗濯物干すdone',),
             (u'洗濯物干せてない',)),
)

print "洗い物だけ残っている時"
print gps((u'消灯done', u'洗い物残ってる', u'洗濯物done', u'明日のご飯done'),
          u'おやすみ',
          house_ops)
print ""

print "一通り終えて、TVだけがついている時"
print gps((u'TVついてる',  u'空調切るdone', u'電気消すdone', u'家事done'),
          u'おやすみ',
          house_ops)
print ""

print "電気がついていて、洗濯物と洗い物が残っている時"
print gps((u'TV消すdone',  u'空調切るdone', u'電気ついてる', 
           u'洗い物残ってる', u'明日のご飯done', 
           u'洗濯物取り入れてない', u'洗濯物たためてない', u'洗濯できてない', u'洗濯物干せてない'),
          u'おやすみ',
          house_ops)
print ""

print "何もかも残っているとき＞＜"
print gps((u'TVついてる',  u'空調ついてる', u'電気ついてる',
           u'洗い物残ってる', u'ご飯が無い', 
           u'洗濯物取り入れてない', u'洗濯物たためてない', u'洗濯できてない', u'洗濯物干せてない'),
          u'おやすみ',
          house_ops)

