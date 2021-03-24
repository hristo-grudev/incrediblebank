import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import IncrediblebankItem
from itemloaders.processors import TakeFirst


class IncrediblebankSpider(scrapy.Spider):
	name = 'incrediblebank'
	start_urls = ['https://www.incrediblebank.com/articles']

	def parse(self, response):
		post_links = response.xpath('//div[@class="card-body"]')
		for post in post_links:
			url = post.xpath('.//a[@data-link-type-id="page"]/@href').get()
			date = post.xpath('.//text()[normalize-space()]').getall()
			date = [p.strip() for p in date]
			date = ' '.join(date).strip()
			if url:
				try:
					date = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', date)[0]
				except:
					date = ''
				yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//title/text()').get()
		description = response.xpath('//div[@data-content-block="bodyCopy1"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=IncrediblebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
