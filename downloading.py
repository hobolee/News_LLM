from newspaper import Article
import newspaper
import csv

# sina_paper = newspaper.build('http://www.sina.com.cn/', language='zh')
cnn_paper = newspaper.build('http://cnn.com', language='en', memoize_articles=False)

# for category in sina_paper.category_urls():
#     print(category)

numbers = len(cnn_paper.articles)
print(numbers)
print(cnn_paper.size())

header = ['id', 'title', 'content', 'keywords', 'summary', 'url']

f = open(r'C:\Users\hliem\Downloads\news\cnn_news.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)

for i in range(numbers):
    try:
        print(i)
        article = cnn_paper.articles[i]
        article.download()
        article.parse()
        article.nlp()
        # print(article.keywords)
        # print(article.summary)
        data = [i, str(article.title), str(article.text), str(article.keywords), str(article.summary), article.url]
        writer.writerow(data)
        if i == 540:
            print(i)
    except Exception as e:
        print(str(i) +': ', e)

f.close()
