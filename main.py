from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import openai
import dbhelper
import json

api_key = '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'
access_key = "testkey"
debug_token = "debug"
oaibase = openai.OpenAIAPI(api_key)
dbidle = dbhelper.Database("testdebug")
messages = [{"role": "user", "content": "请说一句你独创的，发人深省的话，尽量不要让它落入俗套，它不需要很励志，可以包含一点负能量。你的输出只应该包括这句话。"}]

app = FastAPI()

class GPTQuery(BaseModel):
    gptauth: str
    recycle: bool = False

class GPTDebug(BaseModel):
    debugauth: str
    insdata: dict

@app.post('/hitokoto')
async def sum(workloads: GPTQuery):
    if workloads.gptauth == access_key:
        oaibase.contentInit(messages)
        response = oaibase.genRequest()
        resJSON = json.dumps(response)
        dbidle.log_request(False, resJSON)
        hitokoto = response["choices"][0]["message"]["content"]
        return {'result': hitokoto}
    else:
        raise HTTPException(status_code=400, detail='Body must contain auth.')

@app.post('/hitokoto-cached')
async def cachehtk(workloads: GPTQuery):
    if workloads.gptauth == access_key:
        if workloads.recycle:
            response = dbidle.random_anything()
        else:
            response = dbidle.random_usable()
        errno = response["err"]
        if errno == False:
            resJSON = json.loads(response["result"])
            reqid = resJSON["id"]
            resOBJ = resJSON["reqres"]["choices"][0]["message"]["content"]
            dbidle.update_reqstat(reqid, False)
            return {'result': resText}
        if errno == True:
            return {'result': "Something went wrong. Backend cache is currently unable to support your request."}
    else:
        raise HTTPException(status_code=400, detail='Body must contain auth.')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
