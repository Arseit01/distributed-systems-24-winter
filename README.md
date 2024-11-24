# distributed-systems-24-winter

Lab repository for class "Parallele und verteilte Systeme".  
Backend build in the Python Framework Flask  
Image can be found under https://hub.docker.com/r/dryssel/distr-flask

## Useful commands

run server localy in debug mode

```sh
flask run --debug  
```  

docker build command

```sh
docker build -t sampleapp:v1 .
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
   **Principle**: <br>
   **Implementation**:<br> <br>
6. Processes <br>
   **Principle**: <br>
   **Implementation**:<br> <br>
7. Port binding <br>
   **Principle**: <br>
   **Implementation**:<br> <br>
8. Concurrency <br>
   **Principle**: <br>
   **Implementation**:<br> <br>
9. Disposability <br>
   **Principle**: <br>
   **Implementation**:<br> <br>
10. Dev/prod parity <br>
    **Principle**: <br>
    **Implementation**:<br> <br>
11. Logs <br>
    **Principle**: <br>
    **Implementation**:<br> <br>
12. Admin processes <br>
    **Principle**: <br>
    **Implementation**: 

Sources: <br>
https://12factor.net/ <br>
https://en.wikipedia.org/wiki/Twelve-Factor_App_methodology <br>
https://www.divio.com/blog/12-factor-methodology-beginner-guide/
