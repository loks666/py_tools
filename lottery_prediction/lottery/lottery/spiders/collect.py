import scrapy


class SsqSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['zhcw.com']
    start_urls = ['https://www.zhcw.com/kjxx/ssq/kjxq/?kjData=2024025']

    def parse(self, response):
        # 选择带有 data-zhou 属性的 <tr> 元素
        for row in response.xpath('//tr[@data-zhou]'):
            yield {
                '期号': row.xpath('./td[1]/text()').get(),
                '开奖日期': row.xpath('./td[2]/text()').get(),
                '红球号码': row.xpath('./td[3]//span[@class="jqh"]/text()').getall(),
                '蓝球号码': row.xpath('./td[4]//span[@class="jql"]/text()').get(),
                '销售额': row.xpath('./td[5]/text()').get(),
                '一等奖数': row.xpath('./td[6]/text()').get(),
                '一等奖奖金': row.xpath('./td[7]/text()').get(),
                '二等奖数': row.xpath('./td[8]/text()').get(),
                '二等奖奖金': row.xpath('./td[9]/text()').get(),
                '总投注数': row.xpath('./td[10]/text()').get(),
                '总奖金': row.xpath('./td[11]/text()').get(),
            }
