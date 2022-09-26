import openai
import random
from itemadapter import ItemAdapter

class ScrapeitPipeline:

    def open_spider(self, spider):
        self.reviews = []

    def close_spider(self, spider):
        if spider.summarize:
            self.summarize()

    def process_item(self, item, spider):
        review = ItemAdapter(item).asdict()
        self.reviews.append(f"## {review['title']}\n{review['body']}")
        return item

    def gpt3(self, prompt):        
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        response = openai.Completion.create(
            engine='text-davinci-002',
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        text = response['choices'][0]['text'].strip()
        print(f'PROMPT: {prompt}\n\n')
        print(f'RESPONSE: {text}')
        return text

    def summarize(self):
        # Select 20 random reviews to generate our summary
        samples = random.sample(self.reviews, 5)
        
        # Extract key points from each review
        key_points = ""
        for sample in samples:
            prompt = f'Write a list summarizing the key points made in the following user review: "{sample}"\n\nList:\n- '
            key_points += f'{self.gpt3(prompt)}\n'
        
        # Now write write a master summary using the aggregated key points
        prompt = f'Below is a list of key findings from different user reviews for a website. Write a paragraph summarizing the pros and cons of the service from the perspective of a third-party.\n\nKey Findings:\n{key_points}\n\nPros:'

        print(f'\n\n\n{self.gpt3(prompt)}')