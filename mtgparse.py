#!/usr/bin/python

import argparse
import xml.etree.ElementTree as et
from difflib import get_close_matches
from titlecase import titlecase

class MtgData():
    def __init__(self, path):
        self.path = path
        try:
            self.root = et.parse(path).getroot()
        except:
            raise Exception
        self.cards = self.root.find('cards').findall('card')
        self.sets = self.root.find('sets').findall('set')
        self.names = [n.find('name').text for n in self.cards]
        self.kv_sets = dict((e.find('name').text, e.find('longname').text)
                                for e in self.sets)

    def find_card(self):
        card = titlecase(raw_input("Enter card name:\n"))
        match = get_close_matches(card, self.names, cutoff=0.7)

        if not match:
            # Try a more accepting fuzzy search
            print "No card found."
            match = get_close_matches(card, self.names, cutoff=0.3)
            if match:
                print "Did you mean one of these:"
                print ', '.join(match)
        else:
            print "Editions for {}:".format(match[0])
            for card in self.cards:
                if card.find('name').text == match[0]:
                    for s in card.findall('set'):
                        print "{} - {}".format(s.text, self.kv_sets[s.text])

def run(MtgObj):
    while True:
        MtgObj.find_card()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_path")
    args = parser.parse_args()

    try:
        print "Loading XML file"
        MtgObj = MtgData(args.xml_path)
    except Exception:
        print "Bad XML file"

    run(MtgObj)

if __name__ == '__main__':
    main()
