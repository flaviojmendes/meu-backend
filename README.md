# Backend

## Como rodar em Ambiente de Desenvolvimento

Primeiro, instale as dependências:

```bash

pipenv install

```

Dê uma olhada no arquivo `.env.example` e crie um arquivo `.env` com as variáveis de ambiente necessárias.


Depois, rode o servidor:

```bash

uvicorn main:app --reload

```

## Como rodar em Ambiente de Produção


### Seu app precisa ter SSL

Para isso, você pode usar o [certbot](https://certbot.eff.org/instructions?ws=webproduct&os=ubuntubionic) para gerar um certificado SSL gratuitamente.



### Rode com Docker

Tenha o Docker instalado e rode o comando:

```bash

docker build -t meu_app_backend .

```

Após ter sua imagem criada, rode o comando:

```bash

docker run -d -p 443:80 -v /code/certs:/etc/letsencrypt/live/{seu_dominio} meu_app_backend

```

```

