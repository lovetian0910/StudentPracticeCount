# -*- coding: utf-8 -*-
import web
import json
import time
import os

urls = ("/index", "index",
        "/getData", "GetData",
        "/add", "AddCount",
        "/delete", "DeleteStudent")
app = web.application(urls, globals())


def getCurrentMonthFileName():
    nowTime = time.localtime(time.time())
    year = nowTime.tm_year
    month = nowTime.tm_mon
    strMonth = '{:0>2}'.format(str(month))
    filename = str(year) + strMonth
    return filename

def getCurrentDayStr():
    nowTime = time.localtime(time.time())
    year = nowTime.tm_year
    month = nowTime.tm_mon
    day = nowTime.tm_mday
    strMonth = '{:0>2}'.format(str(month))
    strDay = '{:0>2}'.format(str(day))
    return str(year) + strMonth + strDay

class hello:
    def GET(self):
        return "hello, world!"


class GetData:
    def GET(self):
        filename = getCurrentMonthFileName() + ".json"
        fileObject = open(filename, mode='r')
        return fileObject.read()

class AddCount:
    def GET(self):
        input = web.input()
        name = input.name
        count = input.count
        filename = getCurrentMonthFileName() + ".json"
        finalCount = 0
        if os.path.isfile(filename):
            fileObject = open(filename, mode='r')
            jsonObj = json.loads(fileObject.read())
            fileObject.close()
            data = jsonObj['data']
            hasname = False
            for tempdata in data:
                print(cmp(tempdata['name'], name))
                if cmp(tempdata['name'], name) == 0:
                    if cmp(count, '1') == 0:
                        tempdata['count'] += 1
                    elif cmp(count, '-1') == 0:
                        tempdata['count'] -= 1
                    else:
                        return -1
                    # tempdata['time'].append(getCurrentDayStr())
                    hasname = True
                    finalCount = tempdata['count']
                    break
            if not hasname:
                data.append({'name': name, 'count': 1, 'time': [getCurrentDayStr()]})
                finalCount = 1
            fileObject = open(filename, mode='w+')
            fileObject.write(json.dumps(jsonObj))
            fileObject.close()
        else:
            newfile = open(filename, mode='w+')
            jsondict = {'time': getCurrentMonthFileName()}
            tempdata = {'name': name, 'count': 1, 'time': [getCurrentDayStr()]}
            jsondict['data'] = [tempdata]
            outjson = json.dumps(jsondict)
            newfile.write(outjson)
            newfile.close()
            finalCount = 1
        return finalCount


class DeleteStudent:
    def GET(self):
        input = web.input()
        name = input.name
        filename = getCurrentMonthFileName() + ".json"
        fileObj = open(filename, mode='r')
        jsonObj = json.loads(fileObj.read())
        fileObj.close()
        data = jsonObj['data']
        for student in data:
            if cmp(student['name'], name) == 0:
                data.remove(student)
                fileObject = open(filename, mode='w+')
                fileObject.write(json.dumps(jsonObj))
                fileObject.close()
                return 1
        return "没有该学生!"

class index:
    def GET(self):
        hello = web.template.frender('test.html')
        result = hello()
        return result

if __name__ == "__main__":
    app.run()