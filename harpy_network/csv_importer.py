"""
Module to support CSV importing of Kindred and Boons in the following Format:
DEBTOR, CREDITOR, WEIGHT, COMMENT
"""
import csv

from sqlalchemy import func

from harpy_network import db
from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon

class BoonImporter(object):

    def import_from_csv(self, file_path, encoding="ISO-8859-1"):
        with open(file_path, "rt", encoding=encoding) as csvfile:
            boonreader = csv.reader(csvfile)
            for row in boonreader:
                print(row)
                self.process_row(row)

    def process_row(self, row):
        debtor = self.fetch_or_create_character(row[0])
        creditor = self.fetch_or_create_character(row[1])
        weight = row[2]
        comment = row[3] or ""
        self.create_boon(creditor, debtor, weight, comment)

    def fetch_or_create_character(self, character_name):
        character = Character.query.filter(func.lower(Character.name) == func.lower(character_name)).first()
        if not character:
            character = Character(character_name)
            db.session.add(character)
            db.session.commit
        return character

    def create_boon(self, creditor, debtor, weight, comment):
        if weight.lower() not in ('trivial', 'minor', 'major', 'blood', 'life'):
            print("Unable to add {WEIGHT} boon owed by {DEBTOR} to {CREDITOR}".format(WEIGHT=weight,
                                                                                      DEBTOR=debtor.name,
                                                                                      CREDITOR=creditor.name))
        boon = Boon(debtor, creditor, weight.lower())
        boon.comment = comment
        db.session.add(boon)
        db.session.commit()