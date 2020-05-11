import json

from DataBaseSqlite import DataBase, SqlLine
from Request import Request, Card
import argparse


def console_interface():
    parser = argparse.ArgumentParser(description='Parse orders and arguments')
    parser.add_argument('--column', dest='columns', default='name', nargs='*',
                        help='choose columns to show, optional (program can take that argument form sort_by and filter_by)',
                        choices=["cardId",
                                 "name",
                                 "cardSet",
                                 "type",
                                 "faction",
                                 "rarity",
                                 "cost",
                                 "attack",
                                 "health",
                                 "Phrase",
                                 "artist",
                                 "collectible",
                                 "ISelite",
                                 "race"])
    parser.add_argument('--db_file', dest='db_file', default='CardDatabase.sqlite', help='set path to DataBase')
    parser.add_argument('--add', dest='card_name', nargs='*', help='Set name of card to GET it from API')
    parser.add_argument('--sort_by', dest='sort', default='cardId', nargs='*', help='choose columns to sort')
    parser.add_argument('--filter_by', dest='where', nargs=2, help='example: UI.py --filter_by type minion')
    parser.add_argument('--sort_way', dest='sort_way', default='asc', choices=['asc', 'desc'],
                        help='choose sorting asc/desc. Default=asc')
    parser.add_argument('--del', dest='delete', nargs='*', help='Delete row by CardId. Example: --del id id id ...')
    parser.add_argument('--update', dest='update', action='store_true',
                        help='Start to pull data from API by cardId and put date to DataBase.')
    parser.add_argument('--edit', dest='edit', nargs='*', help='Edit columns in row with specific cardID, first arg '
                                                               'is cardId, then column value. Example : --edit '
                                                               'EX1_572 name something type somethingElse ')
    args = parser.parse_args()

    edit = args.edit
    update = args.update
    db_file = args.db_file
    card_name = args.card_name
    where = args.where
    columns = args.columns
    sort = args.sort
    sort_way = args.sort_way
    delete = args.delete

    if delete:
        if type(delete) == list:
            for arg in delete:
                delete[delete.index(arg)] = (r'"' + arg + r'"')
            delete_str = ', '.join(delete)
        else:
            delete_str = r'"' + delete + r'"'
        DataBase().delete(delete=SqlLine(delete=delete_str).sqlDelete())
    elif edit:
        if len(edit) < 3:
            print("Error! Wrong edit formula. Try : --edit cardId columnname value ...")
        else:
            x = Request(name=edit[0]).from_api()
            # parse  JSON as x(one element list of dict):
            y = json.loads(x)
            cardId = edit.pop(0)
            for card in y:
                edited_card = Card(card).sql_attribute()
                for value in edit:
                    if edited_card.get(value):
                        edited_card[value] = edit[edit.index(value) + 1]

                DataBase(attributes_dict=edited_card, db_file=db_file).update(
                    update_cardId=r'"' + cardId + r'"')

    if type(sort) == list:
        sort_by = ', '.join(sort)
    else:
        sort_by = sort

    if type(columns) == list:
        columns_string = ', '.join(columns)
    else:
        columns_string = columns
    if where:
        where[1] = r'"' + where[1] + r'"'
        filter_by = '='.join(where)
    else:
        filter_by = None
    if card_name:
        if type(card_name) == list:
            for name in card_name:
                x = Request(name=name).from_api()
                # parse  JSON as x(one element list of dict):
                y = json.loads(x)
                for card in y:
                    DataBase(attributes_dict=Card(card).sql_attribute(), db_file=db_file).insert()
        else:
            x = Request(name=card_name).from_api()
            # parse  JSON as x(one element list of dict):
            y = json.loads(x)
            for card in y:
                DataBase(attributes_dict=Card(card).sql_attribute(), db_file=db_file).insert()
    elif update:

        for cardId in DataBase().select(SqlLine(sort_by='cardId', columns='cardId').sqlSelect()):

            x = Request(name=cardId[0]).from_api()
            # parse  JSON as x(one element list of dict):
            y = json.loads(x)
            for card in y:
                DataBase(attributes_dict=Card(card).sql_attribute(), db_file=db_file).update(
                    update_cardId=r'"' + cardId[0] + r'"')

    for row in DataBase().select(
            SqlLine(sort_by=sort_by, filter_by=filter_by, columns=columns_string, sort_way=sort_way).sqlSelect()):
        print(row)


if __name__ == "__main__":
    console_interface()
