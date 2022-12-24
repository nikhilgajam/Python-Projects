import urllib.request as req
from collections import Counter
import matplotlib.pyplot as plt
import string


def write_inshort_data(filename, category):
    raw_data = req.urlopen("https://inshortsapi.vercel.app/news?category=" + category)    # https://github.com/pari08tosh/Inshorts-API
    raw_data = str(raw_data.read(), "utf-8").lower()

    length = len(raw_data)
    start = end = 0

    p = open(filename, "w")
    c = 1

    # print(length)
    # print(raw_data)

    content_count = raw_data.count('"content":"')
    while c != content_count:
        start = raw_data.find('content":"', end)
        end = raw_data.find('",', start+1)

        # print(raw_data[start+10:end])
        # print(str(c) + ". " + raw_data[start+10:end] + "\n")
        # if c <= 2 :
        #     print(str(c) + ". " + raw_data[start+10:end] + "\n")

        # p.write(str(c) + ". " + raw_data[start+10:end] + "\n")
        p.write(raw_data[start+10:end] + "\n")

        # if c == 40:
        #     break

        c += 1

    p.close()


def clean_data(filename):
    file = open(filename, "r")
    cleaned_data = file.read()
    cleaned_data = cleaned_data.translate(str.maketrans('', '', string.punctuation))   # Cleaning the text and removing punctuations
    file.close()

    return cleaned_data


def tokenize_and_remove_stop_words(string_data):
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                  "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
                  "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
                  "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
                  "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                  "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
                  "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
                  "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                  "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    tokens = string_data.split()
    needed_words = []
    for i in tokens:
        if i not in stop_words:
            needed_words.append(i)

    return needed_words


def sentimental_analysis(token_list):
    emotion_list = []

    with open("emotional_words.txt", 'r') as file:
        for line in file:
            line = line.replace("\n", "")
            word, emotion = line.split(":")

            if word in token_list and emotion not in emotion_list:
                emotion_list.append(emotion)

    return emotion_list


def counting_different_emotions(token_list):
    return Counter(token_list)


def plot_graph(counter_obj, pic_name):
    fig, ax1 = plt.subplots()
    ax1.bar(counter_obj.keys(), counter_obj.values())
    fig.autofmt_xdate()
    plt.savefig(pic_name)
    plt.show()


if __name__ == '__main__':
    write_inshort_data("data.txt", "politics")
    data = clean_data("data.txt")
    tokens_list = tokenize_and_remove_stop_words(data)
    tokens_list = sentimental_analysis(tokens_list)
    count = counting_different_emotions(tokens_list)
    plot_graph(count, "a.png")


