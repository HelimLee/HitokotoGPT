# -*- coding: utf-8 -*-

import openai
import dbhelper
import json
dbidle = dbhelper.Database("testdebug")
sentence_num = 20 #你希望生成多少句一言？
oaibase = openai.OpenAIAPI("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")
prompt = "请说一句你独创的，发人深省的话，尽量不要让它落入俗套，它不需要很励志，可以包含一点负能量。你的输出只应该包括%d句这样的话，一行一句，不要在句前加上序号。" % sentence_num
messages = [{"role": "user", "content": prompt}]
oaibase.contentInit(messages)
response = oaibase.genRequest()
hitokoto = response["choices"][0]["message"]["content"]
hitokotos = hitokoto.split("\n")
for i in hitokotos:
    i = i.replace("\n", "")
    i = i.split(' ', 1)[1]
    res_to_store = {}
    res_to_store["choices"][0]["message"]["content"] = i
    resJSON = json.dumps(res_to_store)
    dbidle.log_request(True, resJSON)
    print(i)