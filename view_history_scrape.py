from lxml import html
import requests

def get_page_history(page_name, output_name):
        writer = open('view_history/' + output_name, 'w')
        page = requests.get('https://en.wikipedia.org/w/index.php?title=' + page_name.replace(' ', '_') + '&action=history')
        tree = html.fromstring(page.text)

        edits = tree.xpath('//*[@id="pagehistory"]/li')
        for edit in edits:
                date = edit.xpath('./a[@class="mw-changeslist-date"]/text()')[0]
                user = edit.xpath('./span[@class="history-user"]/a/text()')[0]
                size = edit.xpath('./span[@class="history-size"]/text()')[0]
                comment = ''.join(edit.xpath('./span[@class="comment"]//text()'))
                writer.write('Edit: %s, %s, %s, %s' % (date, user, size, comment.encode('utf-8')))
        writer.close()

article_reader = open('controversial_articles.txt', 'r')
for line in article_reader:
        get_page_history(line[0:len(line)-1], line[0:len(line)-1] + '_history.txt')
article_reader.close()
