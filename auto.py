#!/usr/bin/python3
# -*- coding: utf-8 -*

import json
import urllib.request
import ssl


def getJson(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    request = urllib.request.Request(url=url, headers=headers)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(request,context=context)
    return response.read()


def getProblemArray(jsonString):
    data = json.loads(jsonString)
    array = list(data['stat_status_pairs'])
    array.reverse()
    return array

def getSortedKey(elem):
    return int(elem['stat']['frontend_question_id'][3:5])

def getProblemString(array):
    array.sort(key=getSortedKey)
    difficultys = ('简单', '中等', '复杂')
    string = ''
    for x in array:
        string += '| %s |' % x['stat']['frontend_question_id'];
        string += '[%s](https://leetcode-cn.com/problems/%s)' % (
        x['stat']['question__title'], x['stat']['question__title_slug'])
        string += '| {%% post_link leetcode-interview-%s toDo%%} |' % x['stat']['frontend_question_id'][3:5];
        string += '| %s |' % difficultys[x['difficulty']['level'] - 1]
        string += '\n'
    return string


tencentUrl = 'https://leetcode-cn.com/api/problems/favorite_lists/50/'
topUrl = 'https://leetcode-cn.com/api/problems/favorite_lists/top/'
hotUrl = 'https://leetcode-cn.com/api/problems/favorite_lists/hot-100/'

offerUrl = 'https://leetcode-cn.com/api/problems/lcof/'

tencentJsonString = getJson(tencentUrl)
tencentArray = getProblemArray(tencentJsonString)

topJsonString = getJson(topUrl)
topArray = getProblemArray(topJsonString)

hotJsonString = getJson(hotUrl)
hotArray = getProblemArray(hotJsonString)

offerJsonString = getJson(offerUrl)
offerArray = getProblemArray(offerJsonString)

array = offerArray

string = getProblemString(array)
file = open('offer-fix.md', 'w')
file.write("""# title
your description

| Number | Title | Solution | Hard |
|:-------:| :------ | :-----: | :-----: |
""")
file.write(string)
file.close()
