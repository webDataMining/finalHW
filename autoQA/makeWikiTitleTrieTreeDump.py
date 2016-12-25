# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/24/2016   11:41

# import loadWikipediaTitles as wt
import loadSampleTitles as st
import TrieTree as tt
import pickle

wiki_titles_trie_tree = tt.make_trie_tree(st.titles)
print(wiki_titles_trie_tree.postive_max_match_root_node('052D'))


# with open('z_wiki_titles_trie_tree.dump', 'wb') as f:
#     pickle.dump(wiki_titles_trie_tree, f)
