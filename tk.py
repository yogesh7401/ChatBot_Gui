import tkinter
from tkinter import *  
import io
import random
import string 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
from chatterbot.trainers import ChatterBotCorpusTrainer

app = tkinter.Tk()

msg_var=tkinter.StringVar()
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

    #TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


    # Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response
def submit():
 
    msg=msg_var.get()
    user_response = msg
    print("The name is : " + msg)

    flag=True
    # print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
    while(flag==True):
        user_msg = user_response.lower()
        if(user_msg!='bye'):
            if(user_msg=='thanks' or user_msg=='thank you' ):
                msg_var.set("")
                flag=False
                print("ROBO: You are welcome..")
            else:
                if(greeting(user_msg)!=None):
                    print("ROBO: "+greeting(user_msg))
                else:
                    print("ROBO: ",end="")
                    print(response(user_msg))
                    sent_tokens.remove(user_msg)
        else:      
            msg_var.set("")
            flag=False
            print("ROBO: Bye! take care..")
        msg_var.set("")
        flag=False

app.title("Message bot")
app.geometry('350x500')
app.configure(bg='skyblue')
l = Label(app, text = "Message bot", height = 2, width = 39, font=("Arial")).place(x = 0, y = 0)
m = Label(app, text='My name is Robo. If you want to exit, type Bye', width = 35, bg= 'white').place(x = 45, y = 50)
msg = Entry(app, width='45', bd=4, textvariable = msg_var).place(x = 5, y = 460)
sbmitbtn = Button(app, text = "Submit",command = submit,activebackground = "pink", activeforeground = "blue").place(x = 290, y = 460)
app.mainloop()
