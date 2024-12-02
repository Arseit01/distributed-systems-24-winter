# distributed-systems-24-winter

Lab repository for class "Parallele und verteilte Systeme".  
Backend build in the Python Framework Flask  
Image can be found under https://hub.docker.com/r/dryssel/distr-flask

## Useful commands

run server localy in debug mode
```sh
flask run --debug  
```  

build the docker image 
```sh
docker build -t sampleapp:v1 .
```

build/download the images and start the containers
```sh
docker compose up -d
```

start the kubernetes pods
```sh
cd .\k8\
kubectl apply -f .
```

## 12-factor app methodology

Each factor will be briefly explained, followed by an explanation of its implementation in our application.

1. Codebase <br>
   **Principle**: There is only one codebase. The codebase is tracked using version control and is used for multiple
   deployments. <br>
   **Implementation**: The code is stored and tracked in the source code repository GitHub. <br> <br>
2. Dependencies: <br>
   **Principle**: Dependencies are declared and isolated. No implicit reliance. <br>
   **Implementation**: Dependencies are isolated inside the requirements.txt file and get installed dynamically. <br> <br>
3. Config <br>
   **Principle**: Configurations that vary between deployments are stored in the environment. <br>
   **Implementation**: The DATABASE_URL is read from the environment variables defined in the docker-compose file. The same is also true for the debug mode.<br> <br>
4. Backing services <br>
   **Principle**: The backing services, such as a database, are treated as attached resources. <br>
   **Implementation**: The postgresql database is treated as a separate service in the docker-compose file. It is attached via a separate environment variable in the backend service. <br> <br>
5. Build, release, run <br>
   **Principle**: Build and run stages are strictly separated. <br>
   **Implementation**: The build phase of the application is handled by docker, where the code is packaged into a docker image. 
The Release phase sets the environment variables before deploying the container. The Run phase refers to the actual execution of the application in the docker container. <br> <br>
6. Processes <br>
   **Principle**: The application is executed as one or more stateless processes. Persistent data is stored on a backing service. <br>
   **Implementation**: The application runs inside a docker container. It does not rely on in-memory state and all needed data is stored in an external backing service, such as the PostgreSQL database. A REST api is used to further support this factor. <br> <br>
7. Port binding <br>
   **Principle**: Services are making themselves available via exposed ports. <br>
   **Implementation**: The flask application is automatically exposed on port 5000 inside the Docker container. The docker-file then exposes the application on port 8080 to the host machine. This allows the application to be accessed externally. <br> <br>
8. Concurrency <br>
   **Principle**: The application can scale out via the process model.<br>
   **Implementation**: By running multiple instances of the application, the number of processes handling incoming requests can be increased. This can be done with Kubernetes. <br> <br>
9. Disposability <br>
   **Principle**: Maximize robustness and resilience with a fast startup and shutdown. <br>
   **Implementation**: Docker containers are designed to start quickly, with minimal initialization time, and to stop gracefully. In case of a failure, the container can restart quickly. <br> <br>
10. Dev/prod parity <br>
    **Principle**: Development, staging and production are kept as similar as possible. <br>
    **Implementation**: The same docker image is used for all environments. Differences are limited to environment-specific configurations, such as the database URL or other things. <br> <br>
11. Logs <br>
    **Principle**: The application should produce logs as event streams. <br>
    **Implementation**: The Flask Application doenst manage the logs itself, and only puts the debug info and more out to the console. The logs can be accessed via the docker logs command. <br> <br>
12. Admin processes <br>
    **Principle**: Run admin/management tasks as one-off processes. <br>
    **Implementation**: Administrative tasks, such as the database migration command "flask db upgrade", can be executed inside the container using the docker-compose exec command. This ensures that administrative tasks are separated from the main application logic. 

Sources: <br>
https://12factor.net/ <br>
https://en.wikipedia.org/wiki/Twelve-Factor_App_methodology <br>
https://www.divio.com/blog/12-factor-methodology-beginner-guide/



----


### More Kubernetes Stuff

create all .yaml files
```sh
sudo microk8s kubectl apply -f . 
```
```sh
sudo microk8s kubectl get pods
```

Monitor rollout
```sh
sudo microk8s kubectl rollout status deployment/shopping-app
```

Recrating Pods 
```sh
sudo microk8s kubectl delete pod -l app=shopping-app
```

Checking inside the database
```sh
kubectl exec -it shopping-db-5dd6877c7b-tb2tn -- psql -U admin -d shopping_db
\dt
```

Cleaning completly up
```sh
sudo microk8s kubectl delete -f deployment.yaml
sudo microk8s kubectl apply -f deployment.yaml
```
get node
```sh
sudo microk8s kubectl get nodes -o wide
``
