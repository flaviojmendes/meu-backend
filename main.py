
from dotenv import load_dotenv

load_dotenv()

from utils.constants import ALGORITHMS, API_AUDIENCE, AUTH0_DOMAIN, ENV
from fastapi.middleware.cors import CORSMiddleware

import os
import json
from urllib.request import urlopen

from typing import Union
from fastapi import FastAPI, HTTPException, Request, Response
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


@app_private.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


if __name__ == '__main__':
    if (ENV == 'prod'):
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=80,
                    reload=True,
                    ssl_keyfile="privkey.pem",
                    ssl_certfile="fullchain.pem"
                    )
    else:
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=8000,
                    reload=True
                    )