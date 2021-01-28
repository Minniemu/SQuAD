import json
import csv 
from spacy.tokenizer import Tokenizer
import nltk
import spacy
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15000000000
context = []
sentence_num = 0

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

with open('train-v2.0.json') as readfile,open('result.csv' , 'w') as csvfile:
    #Read file
    read = json.load(readfile)

    #Write file
    fieldnames = ['Sentence #', 'Word', 'POS', 'Tag']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() #寫欄位名稱

    len_data = len(read['data'])
    sentence_num = 0

    for i in range(0,len_data):
        p = read['data'][i]
        len_para = len(p['paragraphs']) #計算總共有幾個paragraphs

        
        #Get qas and context
        for j in range(0,len_para) :
            answers = []
            tokens = []
            pos = []
            label = []
            para = p['paragraphs'][j]
            sentence_num += 1
            print("sentence_num = ",sentence_num)

            #Get qas
            qas = para['qas']
            qas_len = len(qas)
            key = 'plausible_answers' #qas 中有 'answers' and 'plausible_answers'
            for k in range(0,qas_len):
                ans = qas[k]['answers']

                for z in range(0,len(ans)):
                    answers.append(ans[z]['text'])
                if key in qas[k]:
                    answers.append(qas[k][key][0]['text'])
            answers = list(set(answers)) #移除重複答案
            #print("answers = ",answers)
            #Get context
            sentence = para['context']
            doc = nlp(sentence)

            #tokenize
            for token in doc:
                tokens.append(token.text) #斷詞
                pos.append(token.tag_) #POS
                label.append('O') #初始化label

            
            for answer in answers:  
                d = nlp(answer) # d 用來存放抓到的關鍵字
                t = [] #t 用來存放斷詞的結果
                for to in d:
                    t.append(to.text) #斷詞
                if len(t) >= 8:
                    continue
                t_len = len(t)
                i = 0 
                tag = False
                while(i < t_len):
                    tag = search(tokens,t[i])
                    if (tag == True) :
                        i += 1
                    else :
                        break
                if (tag == True):
                    index = tokens.index(t[0])
                    for k in range(0,t_len):
                        label[index+k] = 'A'
            for k in range(0,len(tokens)):
                if k == 0:
                    string = "Sentence: "+str(sentence_num)
                    writer.writerow({'Sentence #':string, 'Word': tokens[k], 'POS':pos[k], 'Tag':label[k]})
                else :
                    writer.writerow({'Sentence #':' ', 'Word': tokens[k], 'POS':pos[k], 'Tag':label[k]})


            #print("answers = ",answers)
            #print()






