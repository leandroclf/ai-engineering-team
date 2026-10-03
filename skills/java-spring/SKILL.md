---
name: java-spring
description: Java and Spring/Spring Boot engineering extension.
---
# Java / Spring
Detect Maven or Gradle and the project Spring version. Follow the existing MVC/WebFlux choice and avoid blocking calls in reactive flows. Respect configuration, validation, exception handling and dependency injection conventions. Run native tests, build and static checks.

## Inputs
Java repository, Spring version, build tool and existing MVC/WebFlux conventions.

## Outputs
Stack-aligned change, tests, build and compatibility results.

## Boundaries
Respect the selected programming model; never add blocking work to reactive flows without an explicit boundary.

## Validation
Run the repository's Maven/Gradle build, tests and static checks with the supported JDK and dependency constraints.
