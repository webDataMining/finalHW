# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   13:42

# 疑问代词的判断类

import Word as w
import commonVar as c



interrogative_pronouns = c.interrogative_pronouns

def is_interrogative_pronoun(word:w.Word):
    if word.content in interrogative_pronouns:
        return True
    return False
