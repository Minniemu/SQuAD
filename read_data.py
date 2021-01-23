'''import csv
with open('dev-v2.0.csv','r') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        print(row['data'])
        print()'''
import json
import csv 
from spacy.tokenizer import Tokenizer
import nltk
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15000000000
context = []
answers = []
sentence_num = 0
with open('test.json') as file,open('result.csv','w') as csvfile:
    fieldnames = ['Sentence #', 'Word', 'POS', 'Tag']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    read= json.load(file)
    for p in read['data']:
        para = p['paragraphs']
        length = len(para) 
        tokens = []
        pos = []
        #sentence = " "
        sentence_num += 1
        print("length",length)
        for i in range(0,length-1):
            #處理文章內容
            context.append(para[i]['context']) #取出文章內容
            sentence = para[i]['context']
            doc = nlp(sentence)
            for token in doc :
                tokens.append(token.text) #斷詞
                pos.append(token.tag_) #POS
            for j in range(0,len(tokens)-1):
                if j == 0:
                    string = "Sentence: "+str(sentence_num)
                    writer.writerow({'Sentence #':string, 'Word': tokens[j], 'POS':pos[j]})
                else :
                    writer.writerow({'Sentence #':' ', 'Word': tokens[j], 'POS':pos[j]})
            qas = para[i]['qas']
            qas_length = len(qas)
            for j in range(0,qas_length-1):
                answers.append(qas[j]['answers'][0]['text']) #取出答案
            print("i",i)

print("sentence_num:",sentence_num)
#print(context)
#print(answers)