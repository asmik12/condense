import scrapy

class ProjectSpider(scrapy.Spider):
    name = "proj"
    allowed_domains = ["devpost.com", "la-hacks-2024.devpost.com"]
    start_urls = ["https://la-hacks-2024.devpost.com/project-gallery"]

    def parse(self, response):
        for project in response.xpath('//*[@id="submission-gallery"]/div[position() >=2 and position() <= 9]/div[position() >= 1 and position()<=3]'):
            winner_badge = project.xpath('/html/body/div[1]/div/div/section/section/div/div[2]/div[1]/a/div/aside').get()
            if winner_badge:
                project_link = response.urljoin(project.xpath('.//a//@href').get())
                #yield {'link': project_link} --- this works, so links are functional
                yield response.follow(project_link, self.parse_project)

        next_page = response.css('li.next a::attr(href)').get()
        if  next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_project(self, response):
        #what_it_does = response.xpath('/html/body/section/article[1]/div/div/div[2]/h2[3]/following-sibling::node()[preceding-sibling::/html/body/section/article[1]/div/div/div[2]/h2[4]]')
        #yield {'reached': 'yes'} -- this works
        what_it_does_paragraphs = response.xpath('//h2[text()="What it does"]/following-sibling::p')
        insp_paragraphs = response.xpath('//h2[text()="Inspiration"]/following-sibling::p')
        # Extract text from paragraphs
        inspiration = [p.get() for p in insp_paragraphs]
        what_it_does = [p.get() for p in what_it_does_paragraphs]
        yield{
            'title':response.xpath('/html/body/section/header/div[1]/div/h1/text()').get(),
            'inspiration': inspiration, 
            'what_it_does': what_it_does
        }