import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt

# 此处填入所有敏感词
words = ["李卿", "付德权"]
# 新闻类型
# 比如通知公告的列表页为：http://cs.cumt.edu.cn/index/tzgg.htm
# 那么就将tzgg加入typeList列表
typeList = ["xwdt", "tzgg", "xsjl", "xshd", "ssfc", "jxky1"]

line = 0
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet("main")


def writeLine(type, title, link, words):
    global line, workbook, worksheet
    worksheet.write(line, 0, type)
    worksheet.write(line, 1, title)
    worksheet.write(line, 2, link)
    worksheet.write(line, 3, words)
    line = line + 1


def analyse(words, type):
    print("————————————" + "开始分析：" + type + "——————————————")
    url = "http://cs.cumt.edu.cn/index/" + type + "/"
    index = 1
    while True:
        url2 = url + str(index) + ".htm"
        print("\n查找：" + url2)
        try:
            response = urllib.request.urlopen(url2)
        except urllib.error.URLError as e:
            print("————————————" + "分析完毕：" + type + "——————————————")
            break
        bs = BeautifulSoup(response, "html.parser")
        liTag = bs.select("a[target='_blank']")
        for li in liTag:
            title = li.contents[0]
            detailUrl = "http://cs.cumt.edu.cn" + li['href'][5:]
            print(detailUrl)
            try:
                detailRes = urllib.request.urlopen(detailUrl, timeout=1)
            except IOError:
                continue
            detailRes = detailRes.read().decode('utf-8')
            wordsResult = []
            flag = False
            for word in words:
                pat = re.compile(word)
                match = pat.search(detailRes)
                if match is not None:
                    flag = True
                    wordsResult.append(word + " ")
            if flag:
                print(detailUrl + " 含：" + str(words) + "  已写入xls")
                writeLine(type, title, detailUrl, wordsResult)
        index = index + 1


if __name__ == '__main__':
    for type in typeList:
        analyse(words, type)
    workbook.save("result.xls")

