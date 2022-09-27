import openai
import random
from itemadapter import ItemAdapter

class ScrapeitPipeline:

    def open_spider(self, spider):
        print("Starting scraping..\n")
        self.reviews = []

    def close_spider(self, spider):
        print('Scraping finished.\n')
        if spider.summarize:
            print('Compiling summary..\n')
            self.summarize(spider)

    def process_item(self, item, spider):
        review = ItemAdapter(item).asdict()
        body = review['body']
        if body is not None:
            self.reviews.append(f"{body}")
        return item

    def gpt3(self, prompt):        
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        response = openai.Completion.create(
            engine='text-davinci-002',
            prompt=prompt,
            temperature=0.7,
            max_tokens=400,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        text = response['choices'][0]['text'].strip()
        return text

    def summarize(self, spider):
        # Select 5 random reviews to generate our summary
        samples = random.sample(self.reviews, 8)
        prompt = f'The following are user reviews of {spider.domain}. Write a comprehensive summary synthesizing the information presented in each review.\n\n----------\n'
        
        for sample in samples:
            prompt += f'{sample}\n---------\n'
        
        summary = self.gpt3(prompt)
        print(f'"{summary}"')