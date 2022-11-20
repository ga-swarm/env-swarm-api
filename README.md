## Envelop SWARM API service  
HTTP API, implemented with FastAPI python framework.

### Local development with docker env
API service is configured through environment variables, see `.env.example`.
Actually in this implementation you dont need any DB params. But it wiil be need soon. So 
you can use local docker postgress.
For use commands below just rename `.env.example` to `.env.local`

```bash
cd <project-root>

## Run once for buld local containers
docker build -f ./DockerfileLocal -t apiservice_swarm:local .

## run with api & tests
docker-compose  -f docker-compose-local.yaml up

##In browser
http://localhost:3007/docs

```
Only single endpoint that you need:
```bash
curl -X 'POST' \
  'http://localhost:3007/mint/new' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "desc": "string",
  "image": "string",
  "mime": "string",
  "props": [
    {
      "type": "string",
      "name": "string"
    }
  ]
}'
```





