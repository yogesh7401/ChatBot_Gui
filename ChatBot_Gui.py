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
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

app = tkinter.Tk()

msg_var=tkinter.StringVar()
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

#Preprocessing by WordNetLemmatizer
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching for greeting
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

    flag=True
    while(flag==True):
        user_msg = user_response.lower()
        listbox.insert(END,"")
        listbox.insert(END,"Me : "+user_msg)
        if(user_msg!='bye'):
            if(user_msg=='thanks' or user_msg=='thank you' ):
                msg_var.set("")
                flag=False
                listbox.insert(END,"Bot : You are welcome..")
            else:
                if(greeting(user_msg)!=None):
                    listbox.insert(END,"Bot : "+greeting(user_msg).capitalize())
                else:
                    # listbox.insert(END,"Bot : ",end="")
                    listbox.insert(END,"Bot: "+response(user_msg).capitalize())
                    sent_tokens.remove(user_msg)
        else:      
            msg_var.set("")
            flag=False
            listbox.insert(END,"Bot : Bye! take care..")
            # app.destroy()
        msg_var.set("")
        flag=False

app.title("Message bot")
app.geometry('350x500')
app.configure(bg='skyblue')
l = Label(app, text = "Message bot", height = 2, width = 39, font=("Arial")).place(x = 0, y = 0)
m = Label(app, text='My name is Bot. If you want to exit, type Bye', width = 35, bg= 'white').place(x = 45, y = 50)

scrollbar = Scrollbar(app)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(app, bg='skyblue', width = 36, font=("Arial", 12), height = 20, borderwidth = 0, fg = 'white')
listbox.config(highlightbackground='skyblue', highlightcolor='skyblue', yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)

listbox.place(x=3,y=75)
# listbox.pack()
# message_box = Message(app, text="Hello, Tkinter!", relief=RIDGE).place(x=10,y=100)
# message_box.pack()

msg = Entry(app, width='40', bd=4, textvariable = msg_var).place(x = 5, y = 460)
sbmitbtn = Button(app, text = "Submit",command = submit,activebackground = "pink", activeforeground = "blue").place(x = 270, y = 460)
app.mainloop()
