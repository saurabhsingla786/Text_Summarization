import bs4 as bs
import urllib.request
import re
import nltk
import heapq

page = urllib.request.urlopen("https://en.wikipedia.org/wiki/Lionel_Messi").read()
soup = bs.BeautifulSoup(page,'lxml')
#print(page)     #print the page

text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text
#print(text)

text = re.sub(r'\[[0-9]*\]',' ',text)            
text = re.sub(r'\s+',' ',text)    
clean_text = text.lower()
clean_text = re.sub(r'\W',' ',clean_text)
clean_text = re.sub(r'\d',' ',clean_text)
clean_text = re.sub(r'\s+',' ',clean_text)
sentences = nltk.sent_tokenize(text)
stop_words = nltk.corpus.stopwords.words('english')
#print(sentences)

word2count = {}  #line 1
for word in nltk.word_tokenize(clean_text):     #line 2
    if word not in stop_words:                  #line 3
        if word not in word2count.keys():
            word2count[word]=1
        else:
            word2count[word]+=1
for key in word2count.keys():                   #line 4
    word2count[key]=word2count[key]/max(word2count.values())

# Calculate the score
sent2score = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' '))<30:
                if sentence not in sent2score.keys():
                     sent2score[sentence]=word2count[word]
                else:
                    sent2score[sentence]+=word2count[word]

best_sentences = heapq.nlargest(7,sent2score,key=sent2score.get)
for sentences in best_sentences:
    print(sentences,'\n')
