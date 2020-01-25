import tqdm
import pymongo
import matplotlib.pyplot as plt


URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages

def write_to_file():
    names = ['Rafa', 'Quinn', 'Matias', 'Martin', 'Liam', 'Luke', 'Cynder', 'Babak', 'Collin', 'Davo', 'Evan', 'Hannan', 'Israel', 'Jimmy', 'John', 'Felipe']

    with open('full_text.txt', 'w') as f:
        text = col.find({"Author": {'$ne': "System message"}}, {"_id": 0, "Body":1})
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
    wordcloud = WordCloud(max_font_size=150, width=2000, height=1200).generate(text)
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
