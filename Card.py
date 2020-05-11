class Card:

    def __init__(self, cardId, name, cardSet='none', type='none', faction='none', rarity='none', cost='none', attack='none', health='none', text='none', artist='none', collectible='none',
                 elite='none', race='none'):
        self.rarity = rarity
        self.cost = cost
        self.attack = attack
        self.health = health
        self.text = text
        self.artist = artist
        self.collectible = collectible
        self.elite = elite
        self.race = race
        self.faction = faction
        self.type = type
        self.cardSet = cardSet
        self.name = name
        self.cardId = cardId

        self.CardList = {
            "cardId": cardId,
            "name": name,
            "cardSet": cardSet,
            "type": type,
            "faction": faction,
            "rarity": rarity,
            "cost": cost,
            "attack": attack,
            "health": health,
            "Phrase": text,
            "artist": artist,
            "collectible": collectible,
            "ISelite": elite,
            "race": race
        }

