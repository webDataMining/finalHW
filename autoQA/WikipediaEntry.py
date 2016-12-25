# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/19/2016   21:54

import json


class Entry:
    def __init__(self, title: str, text: str, infobox=None):
        self.title = title
        self.text = text
        self.infobox = infobox

    def has_infobox(self):
        return self.infobox is None

    def __str__(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    entry = Entry('title_', 'text_', 'infobox_')
    print(entry)
