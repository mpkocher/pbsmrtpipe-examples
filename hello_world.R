#!/usr/bin/env Rscript
# Simple Hello World Example
# Load the example registry from the library code

library(pbcommandR)
library(argparser)
library(logging)
library(jsonlite, quietly = TRUE)

# This must be globabaly unique and
TC_NAMESPACE <- "pbsmrtpipe_examples"

# Import your function from library code
runHelloWorld <- function(inputTxt, outputTxt) {
  msg <- paste("Hello World from R. Input File ", inputTxt, "\n")
  cat(msg, file = outputTxt)
  return(0)
}

# Wrapper to convert Resolved Tool Contract to your library func
runHelloWorldRtc <- function(rtc) {
  return(runHelloWorld(rtc@task@inputFiles[1], rtc@task@outputFiles[1]))
}

# Example populated Registry for testing
toolRegistryBuilder <- function() {

  # The namespace must be globally unique and the exe must be in the path
  # the exe will be called with {driver} /path/to/resolved-tool-contract.json
  # Example "example.R run-rtc /path/to/resolved-tool-contract.json"
  r <- registryBuilder(TC_NAMESPACE, "hello_world.R run-rtc ")

  # Tool can be added and will be callable via a suparser-esque interface using
  # the global tool contract id (e.g, pbsmrtpipe_examples.tasks.hello_world_r)
  registerTool(r, "example_hello_world_r", "0.1.1", c(FileTypes$TXT), c(FileTypes$TXT), 1,
    FALSE, runHelloWorldRtc)
  # More Tools can be added by more calls to `registerTool`
  return(r)
}

# Run from a Resolved Tool Contract JSON file -> Rscript /path/to/exampleDriver.R
# run-rtc /path/to/rtc.json Emit Registered Tool Contracts to JSON -> Rscript
# /path/to/exampleDriver.R emit-tc /path/to/output-dir then make Tool Contracts
# JSON accessible to pbsmrtpipe Builds a commandline wrapper that will call your
# driver q(status=mainRegisteryMainArgs(exampleToolRegistryBuilder()))
q(status=mainRegisteryMainArgs(toolRegistryBuilder()))
