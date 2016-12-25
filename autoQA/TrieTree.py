# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/21/2016   19:46

class TrieNode:
    def __init__(self, character: str, is_end: bool = False):
        self.character = character
        self.is_end = is_end
        self.childs = dict()

    def add_child(self, child_str: str):
        # 防错处理
        if len(child_str) <= 0:
            # raise Exception("Child must not be empty!")
            self.is_end = True
            return

        this_child_key_character = child_str[0]
        if this_child_key_character not in self.childs.keys():
            tmp_node = TrieNode.make_new_node(child_str)
            self.childs[this_child_key_character] = tmp_node
        else:
            # 已经有这个node了
            self.merge_child_str(child_str)

    def merge_child_str(self, child_str:str):
        child_node = self.childs[child_str[0]]
        child_node.add_child(child_str[1:])

    def add_child_for_new_node(self, child_word: str):
        child_node_key_character = child_word[0]
        child_node = TrieNode.make_new_node(child_word)
        self.childs[child_node_key_character] = child_node

    @classmethod
    def make_new_node(cls, word:str):
        # 建立全新的trieTree
        if len(word) <= 0:
            raise Exception("word parameter can not be empty!")
        this_node = TrieNode(word[0])
        if len(word) == 1:
            # 仅有一个字
            this_node.is_end = True
        else:
            # 有多个字
            this_node.add_child(word[1:])
        return this_node

    def contains_word(self, word)->bool:
        if len(word) == 0:
            return self.is_end
        if word[0] not in self.childs.keys():
            return False
        else:
            return self.childs[word[0]].contains_word(word[1:])

    def __positive_max_match(self, word: str, max_depth: int, cur_word_ind: int, prev_match_ind: int):
        if self.is_end:
            prev_match_ind = cur_word_ind
        if cur_word_ind >= len(word):
            return word[0:prev_match_ind]
        if max_depth == 0:
            # 匹配数 用光了
            if self.is_end:
                return word[0:cur_word_ind]  # 正好遇到结尾
            else:
                return word[0:prev_match_ind]
        cur_character = word[cur_word_ind]
        if cur_character not in self.childs.keys():
            return word[0:prev_match_ind]
        else:
            return self.childs[cur_character].__positive_max_match(word, max_depth - 1, cur_word_ind + 1, prev_match_ind)

    def postive_max_match_root_node(self, word: str, max_depth: int = 10):
        # 假设当前的节点是根节点
        # 没有匹配上的话返回空字符串
        if word[0] not in self.childs.keys():
            return ''
        else:
            return self.__positive_max_match(word, max_depth, cur_word_ind= 0, prev_match_ind= 0)








    # @classmethod
    # def make_new_end_node(cls, one_character_word:str):
    #     if len(one_character_word) != 1:
    #         raise Exception("Only accepts one character!")
    #     this_node = TrieNode(one_character_word)
    #     this_node.is_end = True
    #     return this_node


def test_make_trie_tree():
    words = ['我', '北京', '天安门', '北京大学']
    trie_tree = make_trie_tree(words)
    print(trie_tree.contains_word('北京大学'))
    print(trie_tree.postive_max_match_root_node('北京大'))
    # pass



def make_trie_tree(words: list)->TrieNode:
    root_node = TrieNode('ROOT')
    for word in words:
        root_node.add_child(word)
    return root_node

if __name__ == '__main__':
    test_make_trie_tree()