# Envelop Oracle API  
## API service
Microservice expose API based on FastAPI framework,  
[Documentation and test environment](https://domain/docs)  

### Docs
https://stage.api.envelop.is/docs  
https://api.envelop.is/docs  

### Local development
There are two `.env` files in this project. First located in 
`<project-root>` include environments variables for API app (db config etc.).  
Second located in `<project-root>\tests` folder include environments variables for
config pytest app.

```bash
cd <project-root>

## Run once for buld local containers
docker build -f ./DockerfileLocal -t apiservice_swarm:local .

## run with api & tests
docker-compose  -f docker-compose-local.yaml up


```
### Stage environment


