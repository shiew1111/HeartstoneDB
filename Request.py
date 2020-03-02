import requests
import sys


class Request:
    def __init__(self, name):
        self.name = name
        self.url = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/" + self.name
        self.headers = {
            'x-rapidapi-host': "omgvamp-hearthstone-v1.p.rapidapi.com",
            'x-rapidapi-key': "a92e5c6726msh31ddc7b004177fcp17260fjsn7449de112ee1"
        }
        self.response = requests.request("GET", self.url, headers=self.headers)

    def from_api(self):

        if self.response.json() == {"error": 404, "message": "Card not found."}:
            sys.exit(self.response.json())
        return self.response.text


# Object Card,
class Card:
    # advanced init metod, it can creat object from dict also  allows creating object with as many attributes as you will parse.
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


    # metode that  catch attributes witch are interesting for us, and put them into dict with keys named like sql columns.
    def sql_attribute(self):

        # list of interesting for us attributes, named like in JSON from API
        attribute_list = ["cardId", "name", "cardSet", "type", "faction", "rarity", "cost", "attack", "health", "text",
                          "artist", "collectible",
                          "elite", "race"]
        mapping = {
            'elite': 'ISelite',
            'text': 'Phrase'
        }

        attributes_dict = {}
        # iterating by interesting for us attributes of card  and put it into dict with changed kay names
        for element in attribute_list:
            # check if element from dict fetch element in our object
            if element in self.__dict__:
                # check if key is in mapping --> change name, if not --> leave it
                attr = mapping.get(element, element)
                attributes_dict[attr] = self.__dict__.get(element)
        for e in attribute_list:
            if e not in attributes_dict:
                attr = mapping.get(e, e)
                attributes_dict[attr] = "--"
        return attributes_dict
