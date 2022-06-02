# # import StemmerFactory class
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
# import re
# import string
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.probability import FreqDist


# # create stemmer
# def stemmer(sentence):
#     factory = StemmerFactory()
#     stemmer = factory.create_stemmer()
#     # # stemming process
#     # sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan'
#     # output   = stemmer.stem(sentence)
#     # print(output)
#     # # ekonomi indonesia sedang dalam tumbuh yang bangga
#     # print(stemmer.stem('Mereka meniru-nirukannya'))
#     # # mereka tiru
#     return stemmer.stem(sentence)

# def lowerSentence(sentence):
#     # kalimat = "Berikut ini adalah 5 negara dengan pendidikan terbaik di dunia adalah Korea Selatan, Jepang, Singapura, Hong Kong, dan Finlandia."
#     # lower_case = kalimat.lower()
#     # print(lower_case)
#     # # output
#     # # berikut ini adalah 5 negara dengan pendidikan terbaik di dunia adalah korea selatan, jepang, singapura, hong kong, dan finlandia.
#     return sentence.lower()

# def removePunctuation(sentence):
#     sentence = re.sub(r"\d+", "", sentence)
#     sentence = sentence.translate(str.maketrans("","", string.punctuation))
#     sentence = sentence.strip()
#     # kalimat = "Berikut ini adalah 5 negara dengan pendidikan terbaik di dunia adalah Korea Selatan, Jepang, Singapura, Hong Kong, dan Finlandia."
#     # hasil = re.sub(r"\d+", "", kalimat)
#     # print(hasil)
#     # # ouput
#     # # Berikut ini adalah negara dengan pend   
#     return sentence

# def tokenize(sentence):
#     sentence = stemmer(sentence)
#     print(sentence)
#     sentence = lowerSentence(sentence)
#     sentence = removePunctuation(sentence)
#     print(sentence)
#     token = sentence.split()
#     return token
#     pass



# def main():
#     kalimat = "APA ITU DIGITAL MARKETING, [SEBENARNYA]?"
#     token = tokenize(kalimat)
#     token = 
#     print(token)
#     kemunculan = nltk.FreqDist(token)
#     print(kemunculan.most_common())


#     pass

if __name__== "__main__":
    print("Hello World")
    # from nlp_id.lemmatizer import Lemmatizer 
    # lemmatizer = Lemmatizer() 
    # lemmatizer.lemmatize('Saya sedang mencoba') 
    # # saya sedang coba 