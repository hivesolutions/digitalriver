# [DigitalRiver](http://digitalriver.hive.pt)

Simple test application for the DigitalOcean API library.

## Purpose

It's often difficult to be able to deploy constant infra-structure across a grid without maintaining state across the various nodes composing it. It should be possible to use an inexpensive infra-structure (like [DigitalOcean](https://www.digitalocean.com/)) to be able to manage a grid infra-structure with minimal state in the nodes/machines.

## Idea

The concept is to build simple JSON based files that define the way the feature is configured/build and/or destroyed. A simple bash script file should run the various steps to build the feature in the machine.
