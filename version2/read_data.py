import json
import csv 
from spacy.tokenizer import Tokenizer
import nltk
import spacy
def find_index(ent_list,d):
    try :
        d = str(d) # 一定要用 str() 轉制不然會找不到
        index_ents = ent_list.index(d) #搜尋關鍵字是否有被spacy抓到
    except ValueError:
        index_ents = -1
        pass
    return index_ents

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15000000000
context = []
sentence_num = 0
with open('train-v1.1.json',encoding= 'utf-8') as file,open('result.csv','w',encoding= 'utf-8') as csvfile:
    fieldnames = ['Sentence #', 'Word', 'POS', 'Tag']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() #寫欄位名稱

    read = json.load(file)
    for p in read['data']:
        para = p['paragraphs']
        length = len(para) 
        
        #sentence = " "
        
        #print("length",length)
        for i in range(0,length):

            tokens = []
            pos = []
            answers = []
            seen = set()
            label = []
            sentence_num += 1
            print("sentence_num = ",sentence_num)
            #處理文章內容
            context.append(para[i]['context']) #取出文章內容
            sentence = para[i]['context']
            doc = nlp(sentence)
            for token in doc :
                tokens.append(token.text) #斷詞
                pos.append(token.tag_) #POS
                label.append('O') #初始化label

            qas = para[i]['qas']
            qas_length = len(qas)

            for j in range(0,qas_length):
                ans_length = len(qas[j]['answers'])
                for k in range(0,ans_length):
                    answers.append(qas[j]['answers'][k]['text']) #取出答案
            answers = list(set(answers))
            #ents = [e.text for e in doc.ents] #放關鍵字
            #l = [ e.label_ for e in doc.ents] #放LABEL

            '''print("Sentence",sentence_num)
            print("ents",ents)
            print("l",l)
            print("answers",answers)
            print("tokens",tokens)
            print()'''
            for i in range(0,len(answers)):
                d = nlp(answers[i]) # d 用來存放抓到的關鍵字
                ents = [e.text for e in d.ents]
                l = [e.label_ for e in d.ents]
                #print("ents ",ents)
                t = [] #t 用來存放斷詞的結果
                for to in d:
                    t.append(to.text) #斷詞


                for j in range(0,len(ents)):
                    #print("j=",j)
                    ent = nlp(ents[j])
                    token = []
                    for s in ent :
                        token.append(s.text)
                    #print(token)
                    try :
                        index = tokens.index(token[0]) # 搜尋關鍵字在句子中的位置
                    except ValueError : 
                        index = 0
                        pass

                    if len(ents) == 0:
                        continue
                    t_len = len(token) #計算關鍵字長度
                    if t_len == 1: #如果關鍵字只有一個字
                        label[index] = 'B-'+l[j]
                    else : #處理關鍵字超過一個字的
                        for k in range(0,t_len): 
                            if k == 0:
                                label[index] = 'B-'+l[j] #只有第一個字是以B-開頭
                            else:
                                label[index+k] = 'I-'+l[j] #其他都是以I-再加上Label
                #index_ents = find_index(ents,d)
                #if index_ents == -1:
                    #continue
                '''print(t[0])
                print("first keyword=",t[0],",index=",index)
            
                print("answer=",d,",index_ents=",index_ents,",Tag=",l[index_ents])
                print()'''
                

            for j in range(0,len(tokens)):
                if j == 0:
                    string = "Sentence: "+str(sentence_num)
                    writer.writerow({'Sentence #':string, 'Word': tokens[j], 'POS':pos[j], 'Tag':label[j]})
                else :
                    writer.writerow({'Sentence #':' ', 'Word': tokens[j], 'POS':pos[j], 'Tag':label[j]})
            

print("sentence_num:",sentence_num)
#print(context)
#print(answers)