from wordcloud import WordCloud
import os
import tqdm
import pymongo
import matplotlib.pyplot as plt


URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages

def write_to_file():
    with open('full_text.txt', 'w') as f:
        #  text = col.find({"Author": {'$ne': "System message"}, "Body": {'$ne': "image omitted", '$ne': "video omitted", '$ne': "audio omitted"}},{"Body": 1, "_id": 0})
        text = col.find({"Body": {'$ne': "omitted"}},{"Body": 1, "_id": 0})
        all_mess = text.count()
        full_text = ""
        num = 0
        with tqdm.tqdm(total=all_mess) as pbar:
            for mess in text:
                message = mess['Body']
                f.write(message + ' ')
                num = num + 1
                pbar.update(1)
def get_all_words():
    return open('full_text.txt', 'r').read()
def generate_wordcloud(text):
    wordcloud = WordCloud(width=1600, height=800).generate(text)
    # Open a plot of the generated image.
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('cloud.png', bbox_inches='tight')


if __name__ == '__main__':
    write_to_file()
    text = get_all_words()
    generate_wordcloud(text)
