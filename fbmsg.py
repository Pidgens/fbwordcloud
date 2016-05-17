import argparse
import re
from wordcloud import WordCloud
from HTMLParser import HTMLParser
import matplotlib.pyplot as plt

class MyHTMLParser(HTMLParser):

    def __init__(self, tName, mName):
        HTMLParser.__init__(self)
        self.dataList = []
        self.mName = mName
        self.tName = tName
        self.addMode = False
        self.canAdd = False

    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        pass

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        pass

    def handle_data(self, data):

        # For names X Y
        pattern2 = re.compile("[A-Z][a-z]+\s[A-Z][a-z]+\,\s[A-Z][a-z]+\s[A-Z][a-z]+\Z")

        # For names X-Y Z
        patternAlt = re.compile("[A-Z][a-z]+\s[A-Z][a-z]+\,\s[A-Z][a-z]+\-[A-Z][a-z]+\s[A-Z][a-z]+")

        # For names X Y Z
        pattern3 = re.compile("[A-Z][a-z]+\s[A-Z][a-z]+\,\s[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+")
        if pattern2.match(data) or patternAlt.match(data):
            # print 'MATCH _ 1', self.mName + ', ' + self.tName
            # print 'MATCH _ 2', data
            if data == self.mName + ', ' + self.tName or data == self.tName + ', ' + self.mName:
                print 'DATA:', data
                self.addMode = True
            else:
                self.addMode = False

        if data == self.mName or data == self.tName:
            self.canAdd = False
        if self.canAdd and self.addMode:
            self.dataList.append(data)
        pattern = re.compile("[a-zA-z]+\,\s[a-zA-z]+\s[0-9]+\,\s[0-9]+\s[a-z]+\s[0-9]+\:[0-9]+[a-z]+\s[A-Z]+")
        if pattern.match(data):
            self.canAdd = True

        # if data

        # print "Encountered some data  :", data

    def getData(self):
        return self.dataList

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()
name = args.name
myHTMLParser = MyHTMLParser(name, 'Derek Chiu')
html_file = open('messages.htm').read().decode("UTF-8").splitlines()


for line in html_file:
    myHTMLParser.feed(line)
    # if line == matchName:
    #     print line

# print 'OUTPUT', myHTMLParser.getData()


newfile = open('messageOutput.txt', mode='w')
for line in myHTMLParser.getData():
    newfile.write(line.encode('utf-8').strip()+"\n")

text = open("messageOutput.txt", mode='r').read()

wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud)
plt.axis("off")

wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
