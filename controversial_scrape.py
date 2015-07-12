from lxml import html
import requests

page = requests.get('https://en.wikipedia.org/wiki/Wikipedia:List_of_controversial_issues')
tree = html.fromstring(page.text)

articles = tree.xpath('//*[@id="mw-content-text"]/div/ul/li/a/text()')

with open('controversial_articles.txt', 'w') as writer:
	for article in articles:
		writer.write(article.encode('utf-8') + '\n')
