# Implementation

The main language used across the entire codebase is Python 3. I chose this as it is a general purpose programming language with huge library support. It focuses on readability and succinctness. It allows you to initially develop snippets of code using the REPL shell and simple scripts, and then easily refactor it into an object orientated and module based system. This, combined with the language's high level features, make it very quick to develop in. This allowed a rapid iteration of ideas, enabling the codebase to evolve as was needed.

The secondary language used in the project was JavaScript. Given I wanted to create an interactive, web-based visualisation, it was the obvious choice as it is the only scripting language supported by all major browsers. I could have used a language that transpiles to JavaScript, such as TypeScript, but I felt there was very little benefit unless I planned to build a much larger web-app. Although JavaScript began its life as a browser based scripting language, it has recently become popular as a server-side programming language as well. Node.js is a server-side JavaScript runtime built on top of Google Chrome's V8 JavaScript engine. This allows developers to use the same language on both front-end and back-end web development, reducing duplication of code and the overhead of context switching. This enabled me to use JavaScript rather than Python in situations where it was better suited.

I also designed all the services to be able to run as Docker containers. Containers are a growing trend in the technology industry as they allow software to run in isolation from its surroundings, without the overhead of using a virtual machine. Although both my development machine and production server are running Ubuntu 16.04, allowing the pipeline to be environment-independent is still hugely beneficial. The "Dockerfile" is a set of instructions on how an image should be built and how to run the software contained in it. An example Dockerfile is as follows:

``` Dockerfile
FROM python:3.6.4
COPY secrets.json /
COPY streamer/ /streamer
WORKDIR /streamer
RUN pip install -r streamer.requirements.txt
CMD ["python", "-u", "streamer.py"]
```

The `FROM` instruction tells the Docker service to start building this image on top of the Python image of version 3.6.4. Images are built as layers allowing re-use and saving storage space. The `COPY` instruction is moving the source code and secrets from the codebase into the image. This provides it with the necessary source code without needing to mount the local filesystem into the container at runtime. The `WORKDIR` instruction switches the context to the directory we created in the image to store the code. The `RUN` instruction executes the command preceding it in a shell while building the image. In this case, it uses Pip, the Python dependency manager, to install the dependencies for the streamer service. Finally the `CMD` instruction declares the command that should be used to run the program the container is meant to execute. There are many more supported instructions but they weren't needed by this service to allow it to run in a container. Building this image can be done by executing `docker build --file streamer/streamer.Dockerfile --tag streamer .`. To run this newly built image, execute `docker run streamer`. This will work on any host that has docker installed, regardless of environment or dependencies.

Rather than having to manage the running and building of all the Docker images manually, I added support for Docker-Compose. This is a container orchestration tool that automates the build and run lifecycle. To run the entire pipeline, simply execute `docker-compose up` and the whole system will start up. Once Docker and Docker-Compose are installed on a system, that one command is all that is needed to run the pipeline. This makes deployments completely frictionless on any OS.

#### TODO - Describe implementation of each service
