# [![DigitalRiver](res/logo.png)](http://digitalriver.hive.pt)

Simple test application for the DigitalOcean API library.

## Purpose

It's often difficult to be able to deploy constant infra-structure across a grid without maintaining state across the various nodes composing it. It should be possible to use an inexpensive infra-structure (like [DigitalOcean](https://www.digitalocean.com/) or others) to be able to manage a grid infra-structure with minimal state in the nodes/machines.

## Idea

The concept is to build simple JSON based files that define the way the feature is configured/build and/or destroyed. A simple bash script file should run the various steps to build the feature in the machine.

It should be possible to "recover" the state of the node from it's local information, avoiding the need for a constant centralized data source managed state.

The main engine is named **Torus** and is deployed as part of the base infra-structure required for the running of the **provisioning tasks** that deploye the **features** associated with the **instance**.

## Example

```json
{
    "build" : "build.sh",
    "destroy" : "destroy.sh",
    "start" : "docker start hello_service",
    "stop" : "docker stop hello_service",
    "depends" : [
        "https://server.com/docker/torus.json"
    ],
    "config" : [
        {
            "name" : "HOST",
            "default" : "127.0.0.1",
            "persist" : true
        }
    ]
}
```

## License

DigitalRiver is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://github.com/hivesolutions/digitalriver/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/digitalriver/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/digitalriver/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/digitalriver?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/digitalriver.svg)](https://pypi.python.org/pypi/digitalriver)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
