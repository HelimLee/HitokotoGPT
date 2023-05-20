from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request
import openai
import dbhelper
import json

configfile = open("./config.json", "r")
configjson = configfile.read()
config = json.loads(configjson)
api_key = config["api_key"]
access_key = config["access_token"]
open_port = config["port"]
rate = config["rate"]
rate_cached = config["rate_cached"]
configfile.close()
oaibase = openai.OpenAIAPI(api_key)
dbidle = dbhelper.Database(config["database"])
messages = [{"role": "user", "content": "请说一句你独创的，发人深省的话，尽量不要让它落入俗套，它不需要很励志，可以包含一点负能量。你的输出只应该包括这句话。"}]

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class GPTQuery(BaseModel):
    gptauth: str
    recycle: bool = False
    encycle: bool = False


class GPTDebug(BaseModel):
    debugauth: str
    insdata: dict

@app.post('/hitokoto')
@limiter.limit(rate)
async def sum(workloads: GPTQuery, request: Request):
    if workloads.gptauth == access_key:
        oaibase.contentInit(messages)
        response = oaibase.genRequest()
        resJSON = json.dumps(response)
        if "choices" in response:
            dbidle.log_request(workloads.encycle, resJSON)
            hitokoto = response["choices"][0]["message"]["content"]
            return {'result': hitokoto}
        else:
            return {'result': response}
    else:
        raise HTTPException(status_code=400, detail='Body must contain auth.')

@app.post('/hitokoto-cached')
@limiter.limit(rate_cached)
async def cachehtk(workloads: GPTQuery, request: Request):
    if workloads.gptauth == access_key:
        if workloads.recycle:
            response = dbidle.random_anything()
        else:
            response = dbidle.random_usable()
        errno = response["err"]
        if errno == False:
            resJSON = json.loads(response["result"][2])
            reqid = response["result"][0]
            resOBJ = resJSON["choices"][0]["message"]["content"]
            dbidle.update_reqstat(reqid, False)
            return {'result': resOBJ}
        if errno == True:
            return {'result': "Something went wrong. Backend cache is currently unable to support your request."}
    else:
        raise HTTPException(status_code=400, detail='Body must contain auth.')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=open_port)
