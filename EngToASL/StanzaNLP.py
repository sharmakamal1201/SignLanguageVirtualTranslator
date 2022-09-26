import os
import subprocess
#import stanfordnlp
import stanza
from operator import itemgetter, attrgetter, methodcaller
import json
import spacy
import pafy
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc
from time import sleep
import cv2


#stanfordnlp.download('en')
#nlp = stanfordnlp.Pipeline(models_dir='D:\python_projects\Eng_ASL',processors='tokenize,mwt,pos,lemma,depparse', treebank='en_ewt', use_gpu=False, pos_batch_size=3000)

#proxies = {'http': 'http://ip:port', 'https': 'http://ip:port'}

#stanza.download('en')  # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline('en')             # This sets up a default neural pipeline in English

#spacy_nlp = spacy.load('en_core_web_md')

def wordToDictionary(word):
  dictionary = {
    'id': word.id,
    'head': word.head,
    'text': word.text.lower(),
    'lemma': word.lemma.lower(),
    'upos': word.upos,
    'xpos': word.xpos,
    'deprel': word.deprel,
    'feats': word.feats,
    'start_char': word.start_char,
    'end_char': word.end_char
  }
  return dictionary


def getMeta(sentence):
  englishStruct = {}
  aslStruct = {
    'rootElements':[],
    'UPOS': {
      'ADJ':[], 'ADP':[], 'ADV':[], 'AUX':[], 'CCONJ':[], 'DET':[], 'INTJ':[], 'NOUN':[], 'NUM':[], 'PART':[], 'PRON':[], 'PROPN':[], 'PUNCT':[], 'SCONJ':[], 'SYM':[], 'VERB':[], 'X':[]
    }
  }
  reordered = []
  words = []
  for token in sentence.tokens:
    for word in token.words:
      #print(word.id, word.head, word.text, word.lemma, word.upos, word.deprel) # , word.feats)
      #print(word)
      #j = len(words)
      #for i, w in enumerate(words):
      #  if word.head <= w['head']:
      #    continue
      #  else:
      #    j = i
      #    break
      #words.insert(j, wordToDictionary(word))
      words.append(wordToDictionary(word))
    #words.extend(token.words)
  reordered = words
  #print(reordered)
  return reordered


def getLemmaSequence(meta):
  tone = ""
  translation = []
  for word in meta:
    #print(word)
    # Remove blacklisted words
    if (word['text'].lower(), word['lemma'].lower()) not in (('is', 'be'), ('the', 'the'), ('of', 'the'), ('is', 'are'), ('by', 'by'), (',', ','), (';', ';'), (':'), (':')):
      
      # Get Tone: get the sentence's tone from the punctuation
      if word['upos'] == 'PUNCT':
        if word['lemma'] == "?":
          tone = "?"
        elif word['lemma'] == "!":
          tone = "!"
        else:
          tone = ""
        continue
      
      # Remove symbols and the unknown
      elif word['upos'] == 'SYM' or word['upos'] == 'X':
        continue
      
      # Remove particles
      if word['upos'] == 'PART':
        continue

      # Convert proper nouns to finger spell
      elif word['upos'] == 'PROPN':
        fingerSpell = []
        for letter in word['text'].lower():
          #print(letter)
          spell = {}
          spell['text'] = letter
          spell['lemma'] = letter
          # Add fingerspell as individual lemmas
          fingerSpell.append(spell)
        #print(fingerSpell)
        translation.extend(fingerSpell)
        #print(translation)

      # Numbers
      elif word['upos'] == 'NUM':
        fingerSpell = []
        for letter in word['text'].lower():
          spell = {}
          # Convert number to fingerspell
          pass
          # Add fingerspell as individual lemmas
          fingerSpell.append(spell)

      # Interjections usually use alternative or special set of signs
      elif word['upos'] == 'CCONJ':
        translation.append(word)
      
      # Interjections usually use alternative or special set of signs
      elif word['upos'] == 'SCONJ':
        if (word['text'].lower(), word['lemma'].lower() not in (('that', 'that'))):
          translation.append(word)
      
      # Interjections usually use alternative or special set of signs
      elif word['upos'] == 'INTJ':
        translation.append(word)

      # Adpositions could modify nouns
      elif word['upos']=='ADP':
        # translation.append(word)
        pass

      # Determinants modify noun intensity
      elif word['upos']=='DET':
        pass

      # Adjectives modify nouns and verbs
      elif word['upos']=='ADJ':
        translation.append(word)
        # pass

      # Pronouns
      elif word['upos'] == 'PRON' and word['deprel'] not in ('nsubj'):
        translation.append(word)

      # Nouns
      elif word['upos'] == 'NOUN':
        translation.append(word)

      # Adverbs modify verbs, leave for wh questions
      elif word['upos']=='ADV':
        translation.append(word)
      
      elif word['upos']=='AUX':
        pass

      # Verbs
      elif word['upos']=='VERB':
        translation.append(word)

  # translation = tree
  return (translation, tone)



def translate(parse):
    meta = getMeta(parse)
    #print(meta)
    translation = getLemmaSequence(meta)
    #print(translation)
    return translation