# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/12/2016   19:42

import initializeLTP as ltp
import Sentence as s

question_test1 = "百度公司位于北京。"

sen = s.Sentence(question_test1)

for role in sen.getSemanticRoles():
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
