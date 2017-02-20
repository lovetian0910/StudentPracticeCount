import web
import json
import time
import os

urls = ("/index", "index",
        "/getData", "GetData",
        "/add", "AddCount")
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
    def GET(self, name):
        filename = getCurrentMonthFileName() + ".json"
        if os.path.isfile(filename):
            fileObject = open(filename, mode='w+')
            jsonObj = json.loads(fileObject.read())
            data = jsonObj['data']
        else:
            newfile = open(filename, mode='w+')
            jsondict = {'time': getCurrentMonthFileName()}
            tempdata = {'name': name, 'count': 1, 'time': [getCurrentDayStr()]}
            jsondict['data'] = [tempdata]
            outjson = json.dumps(jsondict)
            newfile.write(outjson)
            newfile.close()
        return 1

class index:
    def GET(self):
        hello = web.template.frender('test.html')
        return hello()

if __name__ == "__main__":
    # app.run()
    getdata = AddCount()
    getdata.GET('kjw')