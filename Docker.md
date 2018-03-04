# BioASQ Docker

This project runs the BioASQ pipeline services inside Docker containers.

## Prerequisites

This tutorial assumes that you have [Docker installed](https://store.docker.com/search?type=edition&offering=community) on your machine.

## Executive Summary

```
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management [1]
export RABBIT_HOST=172.17.0.2                             [2]
git clone https://github.com/cmu-11-791/BioASQ-Rabbit.git [3]
cd BioASQ-Rabbit
git checkout docker
virtualenv -p python2.7 .venv                             [4]
source .venv/bin/activate
make                                                      [5]
./start.sh docker                                         [6]
python pipeline.py data/training.json                     [7]
./save.py                                                 [8]
./stop.sh                                                 [9]
./cleanup.sh
cat /tmp/submission.json                                  [10]
```

1. Start the RabbitMQ server.  If the server is already running you can skip this step.  In fact, if the RabbitMQ server is already running this command will fail!
1. Export the `RABBIT_HOST` variable that is used to specify the IP address that Docker has assigned to the RabbitMQ server.  This will usually be 172.17.0.2, but may change. See [below](#rabbit-ip) for instructions on how to determine the IP address that Docker has assigned to RabbitMQ.
1. Clone the repository<br/>
   `git clone https://github.com/cmu-11-791/BioASQ-Rabbit`<br/>
   `cd BioASQ-Rabbit`
1. Create a virtual environment and activate it. Note that the project requires Python 2.7 so we need to ensure the virtual environment is created with the proper interpreter.<br/>
  `virtualenv -p python2.7 .venv`<br/>
  `source .venv/bin/activate`
1. Build the Docker images<br/>
  `make`
1. Start the containers<br/>
  `./start.sh docker`<br/>
  If you run the `start.sh` script with no parameters or with the `python` parameter then the `service.py` scripts will be run rather than launching the Docker container.
1. Run a pipeline<br/>
  `python pipeline.py one two three two one print`
1. Stop all the containers<br/>
  `./stop.sh`
1. View the output<br/>
  `cat /tmp/deiis-tutorial.log`

**Troubleshooting**

The above should work in the majority of instances.  However, the `start.sh` script expects that Docker will assign the IP address 172.17.0.2 to the RabbitMQ server, which it usually does. If the containers are not starting [check the IP address assigned to the RabbitMQ server](#rabbit-ip).

If Docker reports an error about a container name already in use you will need to delete (rm) that container before running it again.

```
docker: Error response from daemon: Conflict. The container name "XYZ" is already in use by container
$> docker rm XYZ
```

You can use the `./cleanup.sh` script to delete all stopped containers.

# The Long Version

## Setup

It is recommendeded that you create a *virtual environment* for this project.  Since the BioASQ services are not compatible with Python 3.x we should specify that we want a virtual environment for Python 2.7.

```
$> virtualenv -p python2.7 .venv
$> source .venv/bin/activate
```

## Start RabbitMQ

The RabbitMQ server is available as a Docker image so no installation or setup is required.  We can simply launch the container and start using the server.

```
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management
```

Once the RabbitMQ server has started you can login to its management console at http://localhost:15672 (username: *guest*, password: *guest*). We won't be using the RabbitMQ management console, but it is useful to check if your services are connected to the server and watch how many messages are flowing through the server.

<a name='rabbit-ip'></a>
### Get The IP Address of RabbitMQ

Services running on the same machine as the RabbitMQ server can access the server via *localhost*.  However, services running inside Docker containers are **not** on the *same machine* as the RabbitMQ server.  That is, for services running in a Docker container *localhost* is the Docker container, not the machine running the Docker container.  Therefore we need to know what IP address Docker has assigned to the RabbitMQ server.  Services running in Docker will be able to access RabbitMQ via this IP address.

To view information about the network that Docker has created use the `docker network inspect` command:

```
docker network inspect bridge
```

Look for the *Containers* section in the displayed JSON which contains information about each running container.  In particular we need to make a note of the *IPv4Address* assigned to our *rabbit* container.

```json
"Containers": {
    "61b390c1f1643c0ed5aeb3791b3ef00d70f8cf0d63c09d3f8c1feb2dbf176172": {
        "Name": "rabbit",
        "EndpointID": "4f056e9f757f3b940039c9988c731581a0e6ceec09dcb16d63db18b5c300c09f",
        "MacAddress": "02:42:ac:11:00:02",
        "IPv4Address": "172.17.0.2/16",
        "IPv6Address": ""
    }
}
```

Here we can see that Docker has assigned the IP address 172.17.0.2 to my RabbitMQ server.  This is the IP address that services running in a Docker container will use to access the RabbitMQ server.  We will store the IP address in an environment variable that the `start.sh` script will pass to to the Docker containers.

```
export RABBIT_HOST=172.17.0.2
```


## Project Layout

Each service lives in its own directory and all services contain the following files:

* **Dockerfile**<br/>
Copies all *.py files to /root and then sets the ENTRYPOINT to call the service.py script.  The Dockerfile will also setup any additional modules required by the service. For example, the Dockerfile for the `Expander` modules installs the MetaMap software and the `pymetamap` module.
* **Makefile**<br/>
Defines goals for building and running the Docker container.
* **service.py**<br/>
Start up script used to launch the service.  This is the entrypoint for Docker containers or it can be invoked from the command line.
* <strong>*.py</strong><br/>
The service implementation files.  Each service typically defines an abstract base class and then one or more services that extend the base class.

The *Dockerfile*, *Makefile*, and *service.py* files are almost identical across all projects.

## Building The Services

The `docker build` command is used to create a Docker image from the Dockerfile definition.

```
docker build -t image_name` .
```

The above command will create a Docker image named *image_name*. **Note** the period at the end of the `docker build` command.  This specifies that the current directory is to be used as the build context directory, that is, the directory containing the Dockerfile.

For this project we will be building five Docker images:

1. bioasq-rabbit/base
1. bioasq-rabbit/expander
1. bioasq-rabbit/ranker
1. bioasq-rabbit/tiler
1. bioasq-rabbit/results

You can run the `docker build` command manually in each project directory, or you can use the `make` to run the Docker command for you.

```
cd Expander
docker build -t bioasq-rabbit/expander .
```

or

```
cd Expander
make
```

The top level of the project also contains a Makefile that simply calls *make* for each of the services in turn.  So, from the top level directory we can run

```
make
# - or -
make expander
```

## Running The Services

```
$> docker run -d -e HOST=$RABBIT_HOST --name one tutorial/one
$> docker run -d -e HOST=$RABBIT_HOST --name two tutorial/two
$> docker run -d -e HOST=$RABBIT_HOST --name three tutorial/three
$> docker run -d -e HOST=$RABBIT_HOST --name printer -v /tmp:/var/log tutorial/printer
```

The `-v /tmp:/var/log` parameter used when starting the tutorial/printer container mounts the `/tmp` directory on the machine running Docker as `/var/log` in the Docker container.  Since the `printer` service writes its output to the /var/log directory this will cause the output to appear in the /tmp directory on the host machine.

A Bash script is also provided that starts all of the containers.

```
$> ./start.sh
```

### Running A Pipeline

The `pipeline.py` script creates a [Message](https://github.com/CMU-11-791/Docker-Tutorial/blob/master/deiis/deiis/rabbit.py#L33) object with the list of parameters as the *route* (list of services) the message will be sent to.

```
python pipeline.py one two three two one one three print
```

### Stopping The Services


The easiest way to stop all the services is to simply kill the Docker containers.  However, the problem with this is that the containers/services are not shutdown cleanly and a service may be terminated before it has finished processing all of its messages.

The correct way to terminate a service is to send it a *poison pill*, which is just a known message that services listen for to indicate they are to stop processing messages and terminate.  Use the `stop.sh` script to send the poison pill to all services:

```
$> ./stop.sh
```

To stop individual services use the *stop.py* script and specify just the message queues that the poison pill should be sent to:

```
$> ./stop.py one printer
```

**Note:** The `stop.sh` script simply calls `stop.py` and then removes the Docker containers.  You can also use the `cleanup.sh` script to remove all stopped containers.

