# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   10:43

import playground_utility as pu
import questionAnalysis as qana

questions = pu.read_question_with_id()

for ques in questions:
    alter = qana.gen_question_alter_form_str(ques.content)
    if alter:
        ques.alter_form1 = alter
        print(str(ques))

