import scrapy
import os

#now lets start by building a spider class
class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = ['https://blog.scrapinghub.com/']
    #start_urls = ['https://blog.scrapinghub.com/page/1', 'https://blog.scrapinghub.com/page/2']

    # def parse(self, response):
    #     page = response.url.split('/')[-1]
    #     filename = 'posts-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #
    #     print('done all data scraped')

    def parse(self, response):
        for post in response.css('div.post-item'):
            yield {
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get()
            }
        next_page = response.css('a.next-posts-link::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

#to use run command in terminal at location
#scrapy crawl posts

#or use os system call in this script and run it
#os.system("scrapy crawl posts")

#send all the output data to a jason file
os.system("scrapy crawl posts -o posts.csv")
print('done all data scraped')

