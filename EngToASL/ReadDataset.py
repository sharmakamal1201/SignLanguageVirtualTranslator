import json

datasetSignLanguage_MS = []

def ReadfromJsonFile(fileName):
    f = open(fileName)
    data = json.load(f)
    f.close()
    return data

def getVideoDetails(lemma):
    #print(lemma)
    global datasetSignLanguage_MS
    #distance = []
    #token1 = spacy_nlp(text)
    for data in datasetSignLanguage_MS:
        #token2 = spacy_nlp(data['text'])
        #sim = token1.similarity(token2)
        if(lemma.lower() == data['text'].lower()):
            #print(lemma.lower())
            return data['url'], data['start_time'], data['end_time'], data['box']
    return None, None, None, None