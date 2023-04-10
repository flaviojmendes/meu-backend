
from dotenv import load_dotenv
from service.item_service import get_items, remove_item, save_item

load_dotenv()

from utils.constants import ALGORITHMS, API_AUDIENCE, API_DOMAIN, AUTH0_DOMAIN, ENV
from fastapi.middleware.cors import CORSMiddleware

import os
import json
from urllib.request import urlopen

from typing import Union
from fastapi import FastAPI, HTTPException, Header, Request, Response
import uvicorn
from jose import JWTError, jwt


app = FastAPI()
app_public = FastAPI(openapi_prefix='/public')
app_private = FastAPI(openapi_prefix='/api')


app.mount("/public", app_public)
app.mount("/api", app_private)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app_private.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app_public.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def decode_jwt(token: str):
    try:
        token = token.split(" ")[1]
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/",
                )
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="token_expired")
            except jwt.JWTClaimsError as err:
                raise HTTPException(status_code=404, detail="invalid_claims")

            except Exception:
                raise HTTPException(status_code=401, detail="invalid_header")
        if payload is not None:
            return payload
        raise HTTPException(status_code=401, detail="invalid_header")
    except:
        raise HTTPException(status_code=401, detail="invalid_header")


@app_private.middleware("http")
async def verify_user_agent(request: Request, call_next):
    try:
        token = request.headers["Authorization"]
        payload = decode_jwt(token)
        response = await call_next(request)
        return response
    except  Exception as err:

        return Response(status_code=403)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping")
def read_root():
    return "OK"



@app_private.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app_public.get("/items")
def read_item():
    return get_items()



@app_public.get("/items/add/{item_id}")
def add_item(item_id: str):
    return save_item(item_id,)


@app_public.get("/items/delete/{item_id}")
def read_item(item_id: str):
    return remove_item(item_id)








if __name__ == '__main__':
    if (ENV == 'prod'):
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=80,
                    reload=True,
                    ssl_keyfile=f"/code/certs/live/{API_DOMAIN}/privkey.pem",
                    ssl_certfile=f"/code/certs/live/{API_DOMAIN}/fullchain.pem"
                    )
    else:
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=8000,
                    reload=True
                    )