## Envelop SWARM API service  
HTTP API, implemented with FastAPI python framework.

### Local development with docker env
API service is configured through environment variables, see `.env.example`.
Actually in this implementation you dont need any DB params. But it wiil be need soon. So 
you can use local docker postgress.
For use commands below just rename `.env.example` to `.env.local`

### Swarm Dev Environment
#### Swarm Nodes Env
```bash
# in separate terminal:
npm install -g @fairdatasociety/fdp-play
fdp-play start --fairos
```

### Envelop API
```bash
cd <project-root>

## Run once for buld local containers
docker build -f ./DockerfileLocal -t apiservice_swarm:local .

## run with api & tests
docker-compose  -f docker-compose-dev.yaml up

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
  "name": "name",
  "desc": "Descr string",
  "image": "png;example.png",
  "mime": "image/png",
  "props": [
    {
      "type": "string",
      "name": "string"
    }
  ]
}'
```





