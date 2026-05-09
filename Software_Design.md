# Report: Software Design

**Note** Max 2500 words except diagrams. 

**After the word limit, teachers reserve the right to stop reading, which may affect the teams’ grade**

---

## Table of Contents

- [Report: Software Design](#report-software-design)
  - [Table of Contents](#table-of-contents)
  - [1. Dependencies](#1-dependencies)
    - [1.1 Methodology and Tools](#11-methodology-and-tools)
      - [Code Dependencies](#code-dependencies)
    - [1.2 Code Dependencies](#12-code-dependencies)
      - [Most dependent files (Highest Fan-out)](#most-dependent-files-highest-fan-out)
      - [Least dependent files (Lowest Fan-out)](#least-dependent-files-lowest-fan-out)
    - [1.3 Knowledge Dependencies](#13-knowledge-dependencies)
  - [2. Patterns](#2-patterns)
    - [2.1 Pattern 1: \[Pattern Name\]](#21-pattern-1-pattern-name)
  - [3. Summary](#3-summary)

---

## 1. Dependencies

### 1.1 Methodology and Tools

<!-- _Describe the methods and tools used to analyze the dependencies and the results obtained._ -->

#### Code Dependencies

In the section of Code Dependency a Python script was used for static analysis based on regex's import of the two core parts: log4j-core and log4j-api.

From this analysis was excluded tests and the package-info.java as they were considered not important for the purpose of this study.

Furthermore, there is a limitation reguarding the use of the Python's script compared to the use of professional tools. In fact, in Java language, the import of other intra-packag's classes are not required and this can cause some variation of the following results. Reguardless of this, the presented results remains  a good metrics for the inter-package relations.


### 1.2 Code Dependencies

<!-- _Evaluate code dependencies based on the imports in the source code._

- **Most/Least dependent files:** _Indicate which files have the most or least dependencies and explain why._  -->

#### Most dependent files (Highest Fan-out)

*Base path*: ./log4j-core/src/main/java/org/apache/logging/log4j/core

1. config/`AbstractConfiguration.java` - 43 internal imports
2. config/`LoggerConfig.java` - 32 internal imports
3. `LoggerContext.java` - 31 internal imports
<!-- 4. layout/`Rfc5424Layout.java` - 31 internal imports
5. appender/`SmtpAppender.java` - 30 internal imports -->

The most coupled file is AbstractConfiguration.java, the *orchestrator* of the system, indeed, it initializes, configures, starts, stops and sets up the configuration logging.
The high Fan-Out is justified because AbstractConfiguration.java is the integration point of the framework. (Facade pattern <-- too be removed :) )

Unlike AbstractConfiguration.java, whose coupling is about assembling the system, LoggerConfig.java is used as a *dispatcher* seated between the API layer and the Core layer. It receives log events and forwards them to the appropriate Appenders, applying filters.

The LoggerContext.java manages the *runtime lifecycles* of the logging system: it registry of active Loggers  and acts as a bridge between the API and Core infrastructure.


#### Least dependent files (Lowest Fan-out)

*Base path*: ./log4j-api/src/main/java/org/apache/logging/log4j

1. `BridgeAware.java`  - 0 internal imports
2. `LoggingException.java` - 0 internal imports
3. internal/`LogManagerStatus.java` - 0 internal imports
<!-- 3. `CloseableThreadContext.java` - 0 internal imports -->
<!-- 4. `Marker.java` - 0 internal imports -->

BridgeAware.java is an interface with a single method, *setEntryPoint*, and no imports. Since it is an interface, no implementation, there is no need to import any other classes. This maximise reusability.

LoggingException.java is an exception class that extends the Java's standard *RuntimeException*.
Responsable for encapsulate error message caught anywhere in the system.

LogManagerStatus.java is an internal utility that traks when LogManager has been initialized. This class can be accessible in anytime since it does not depends on anything else classes. This could be an example of the Single Responsibility Principle (SRP).

### 1.3 Knowledge Dependencies

_Evaluate knowledge dependencies based on co-change (how often two files are modified together in the same commit)._

- **Inconsistencies:** _Which knowledge dependencies are inconsistent with the code dependencies?_

## 2. Patterns

_Identify at least 4 instances of design patterns in the code._ _Include links to the source code for each._

### 2.1 Pattern 1: [Pattern Name]

- **Roles:** _Which classes play which role?_
- **Problem Solved / Rationale:** _Why is this pattern used? What problem does it solve?_
- **Alternatives:** _Is there an alternative? What would be the pros and cons?_

_(Repeat the structure for Patterns 2, 3, and 4)_

## 3. Summary

_Summarize the results regarding the two design aspects (Dependencies and Patterns)._
