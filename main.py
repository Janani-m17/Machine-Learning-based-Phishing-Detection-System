import streamlit as st
import pickle
from nltk.corpus import stopwords
import string
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

css = """
<style>
body {
    background-color: #f0f2f6;
    font-family: Arial, sans-serif;
}

h1 {
    color: #2c3e50;
    text-align: center;
}

.stTextInput, .stTextArea {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    width: 100%;
}

.stButton button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #2980b9;
}

.stHeader {
    color: #2ecc71;
    text-align: center;
    margin-top: 20px;
}
</style>
"""

# Inject CSS into the app
st.markdown(css, unsafe_allow_html=True)

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Detection")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    transformed_sms = transform_text(input_sms)
    vector_input = tfidf.transform([transformed_sms])
    result = model.predict(vector_input)[0]
    if result == 1:
        st.header("Spam")
    else:
        st.header("It is safe to proceed")
