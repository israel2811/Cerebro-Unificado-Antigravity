FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Setup for CI build
RUN apt-get update && apt-get install -y git curl build-essential
