import spacy
import random
import requests
import pandas as pd

class Person:
    #Class for managing rows of Age dataset dataframe
    def __init__(self, person: pd.core.series.Series):
        templist = list(person)
        self.name = templist[2]
        self.desc = templist[3]
        self.gender = templist[4]
        self.country = templist[5]
        self.occupation = templist[6]
        self.birth = int(templist[7])
        self.death = int(templist[8])
        self.manner = templist[9]
        self.wikidata = wikiExplainer(templist[1], removeEscapeChars=False)
    def __str__(self):
        return f"{self.name}, {self.birth}-{self.death}, {self.desc}"


class BSTNode:
    def __init__(self, blob=None):
        self.lchild = None
        self.rchild = None
        self.key = blob[0]
        self.dict_list = blob[1] #l

    def insert(self, blob):
        # Tree Empty Case
        if (self.key == None):
            self.key = blob[0]
            self.dict_list = blob[1]
            return
        # Key already in tree
        if (self.key == blob[0]):
            return
        # Left Child Insert Case
        if (blob[0] < self.key):
            if (self.lchild != None):
                self.lchild.insert(blob)
                return
            self.lchild = BSTNode(blob)
            return
        # Righ Child Insert Case
        if self.rchild:
            self.rchild.insert(blob)
            return

        self.rchild = BSTNode(blob)

    def search(self, key):
        # Current Node is wanted
        if (key == self.key):
            return self.dict_list
        # Node may be to the left of current node
        if (key < self.key):
            if self.lchild == None:
                return False
            return self.lchild.search(key)
        # Otherwise, Node may be to the right of the current node
        if (self.rchild == None):
            return False
        return self.rchild.search(key)


def reformat(lis, year):
    # reformats hashmap data to BST acceptable input
    dict_list = []
    for item in lis:
        new_dict = {}
        new_dict['Media Type'] = item["titleType"]
        new_dict["Title"] = item['primaryTitle']
        dict_list.append(new_dict)

    return [year, dict_list]

nlp = spacy.load('en_core_web_lg')


def wikiExplainer(title, removeEscapeChars=False, explainerLength=3):

    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }).json()
    response = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&exintro&titles=" +
                            title.replace(" ", "_") + "|" + title.replace(" ", "_") + "&redirects=").json()
    explainer = next(iter(response['query']['pages'].values()))
    if 'extract' in explainer:
        explainer = explainer['extract']
        if removeEscapeChars:
            explainer = ''.join(
                c for c in explainer if c.isalnum() or c == ' ')
            explainer = explainer.replace("\n", " ")
    else:
        explainer = ""

    doc = nlp(explainer)
    explainer = ""
    for j, sentence in enumerate(doc.sents):
        if(j+1 > explainerLength):
            break
        else:
            explainer += str(sentence.text) + " "
    if explainer == "":
        return "No Wikipedia Data Available"
    return explainer

