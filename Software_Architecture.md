# Report: Software Architecture

**Note** Max 2500 words except diagrams. The goal of this
document is describe the software architecture of the system using the C4 model (levl 1, 2 and 3).

**After the word limit, teachers reserve the right to stop reading, which may affect the teams' grade**

---

## Table of Contents

- [Report: Software Architecture](#report-software-architecture)
  - [Table of Contents](#table-of-contents)
  - [1. Tooling](#1-tooling)
  - [2. Context Level](#2-context-level)
  - [3. Container Level](#3-container-level)
  - [4. Component Level](#4-component-level)
  - [5. Architectural Characteristics](#5-architectural-characteristics)

## 1. Tooling

The diagrams were created using PlantUML and the C4-PlantUML library.
This approach made the diagrams easier to modify and maintain during the analysis process.

Using diagrams as code was especially useful because the architecture model changed several times while we were deciding how to define the system boundaries and abstraction levels. With PlantUML, the diagrams can be reviewed and versioned directly in the repository instead of being maintained as separate manually edited images.

The Context, Container, and Component diagrams are located in the `architecture` directory:

- `architecture/context.puml`
- `architecture/container.puml`
- `architecture/component-core.puml`

We did not try to describe every module in the Apache Log4j2 repository because the project is significantly larger than the part relevant for this analysis. Instead, we focused mainly on the logging pipeline and especially on the separation between `log4j-api` and `log4j-core`, since this boundary represents the central architectural idea of the framework: application code interacts with the API, while the actual logging implementation and runtime processing are handled inside Core.

## 2. Context Level

The Context diagram shows how Apache Log4j2 interacts with external applications and logging targets.
At this level, the goal was to understand the role of the framework inside a larger system.
In the diagram, Log4j2 is treated as a black box. A Java application sends log events to it during execution, and a developer decides how the framework should behave by writing or changing configuration files. In C4 terms, the Java application is better seen as an external software system, not as a person. The developer is the human actor because they integrate and configure Log4j2.

The diagram shows three common logging targets: the file system, the console, and remote logging systems. They are outside the framework. The application does not need to know which of these targets will be used. It only makes a logging call, and Log4j2 uses the active configuration to decide where the event goes.

This is the main architectural role of the framework. It keeps logging decisions out of the application logic. For example, changing from console logging to file logging, or from a plain text layout to a JSON layout, should mostly be a configuration change rather than a change in the application code.

## 3. Container Level

The Container diagram focuses on the main Log4j2 modules and their responsibilities.
The most important part at this level is the separation between `log4j-api` and `log4j-core`.

`log4j-api` is the module used directly by applications. It contains the public logging API, including loggers, logging methods, levels, markers, and the main abstractions needed for logging calls. Its purpose is to give applications a stable interface without exposing the internal implementation details.

`log4j-core` contains the actual implementation of the logging engine. It receives log events from the API side, manages configuration, processes events, applies filters, calls appenders, handles layouts, and manages asynchronous logging. In practice, this is the module that turns a logging call such as `logger.info(...)` into output written to a file, console, or remote destination.

The separation between API and Core is one of the main architectural ideas in Log4j2. Applications depend only on the API module, while most implementation details stay inside Core. This improves modularity and keeps application code less dependent on internal framework changes.

The Container Diagram also includes bridge modules such as `log4j-slf4j2-impl` and `log4j-jul`. These modules allow external logging APIs like SLF4J and `java.util.logging` to forward log events into the Log4j2 engine.

At this level, the runtime flow is relatively simple: applications or external logging APIs create log events, the API or bridge modules forward them to `log4j-core`, and Core processes the events and sends the final output to logging destinations such as the file system, console, or remote logging systems.

### Clean architecture relationship

Log4j2 is not really a Clean Architecture system in the usual sense. Clean Architecture is normally discussed for business applications, where entities and use cases are placed at the center. Log4j2 is different: it is a technical framework, and the center of the design is the processing of log events.

Still, there is one clear similarity. Application code depends on `log4j-api`, not on the internal classes of `log4j-core`. This keeps implementation details behind a public boundary. For this reason, I would describe the relationship with Clean Architecture as partial: Log4j2 follows the idea of dependency control, but it is not structured around Clean Architecture layers.

## 4. Component Level

For the Component level, we decided to expand `log4j-core` because this is the part where most of the logging logic is actually handled. Expanding `log4j-api` would not provide the same level of detail since it mostly exposes interfaces and abstractions used by applications.

The component diagram focuses on the main parts involved in the logging pipeline and event processing flow.

The main components included in the analysis are:

- `LoggerContext` — keeps the active runtime logging context and connects the system to the current configuration.
- `Configuration` — stores logger settings, appenders, layouts, filters, and related configuration data.
- `LoggerConfig` — applies logging rules and controls how log events are processed.
- `Filter` — decides whether an event should continue in the pipeline or be rejected.
- `Appender` — writes log events to concrete destinations.
- `Layout` — transforms log events into the required output format.
- `LogEvent` — represents the logging event itself.
- `AsyncLogger` — handles asynchronous logging using the Disruptor-based async pipeline.

The diagram can be understood as a processing flow. A logging call creates a `LogEvent`, the active configuration selects the correct `LoggerConfig`, filters are applied, and then the event is passed to appenders. Before writing the final output, layouts format the message into the representation expected by the destination.

One important observation is that `LoggerConfig` acts as the central coordination point inside the runtime pipeline. It connects filtering, appenders, layouts, and asynchronous processing together, so most event-processing decisions pass through this component.

### SOLID principles

At the component level, Log4j2 generally follows SOLID principles reasonably well, especially for extension-related parts of the framework.

The Single Responsibility Principle can be seen in the separation between filters, layouts, appenders, and configuration-related components. Each of them mainly focuses on one part of the logging pipeline.

The Open/Closed Principle is one of the strongest aspects of the design. New appenders, layouts, and filters can be added through the plugin system without changing the main logging flow implemented in Core.

The Dependency Inversion Principle is visible through abstractions such as `Appender`, `Layout`, and `Filter`. The framework mainly works through interfaces instead of depending only on concrete implementations. Applications also depend on `log4j-api` instead of directly interacting with `log4j-core`.

The Interface Segregation Principle is mostly respected because logging-related responsibilities are separated into multiple smaller abstractions instead of one large interface.

The part that appears more tightly coupled is around `LoggerContext`, `Configuration`, and especially `LoggerConfig`, since these components coordinate many parts of the runtime behavior. However, for a logging framework this kind of central coordination is difficult to avoid completely.

## 5. Architectural Characteristics

The architecture of Log4j2 seems to be driven by two practical needs: it must be easy to adapt, and it must not make application execution too slow. Several architectural qualities follow from this.

Extensibility is handled through the Plugin System and through abstractions such as appenders, layouts, and filters. A project can add a new destination or output format without changing the whole framework. This is especially important for Log4j2 because logging targets vary a lot between applications.

Configurability is handled through external files. Developers can define logger hierarchies, levels, appenders, layouts, and filters outside the application code. This makes the same application easier to move between environments, for example from a local setup to a production deployment.

Performance is addressed through asynchronous logging and through the separation between creating an event and delivering it. With LMAX Disruptor, Log4j2 can reduce blocking on application threads when asynchronous logging is enabled. This matters because logging is spread across the whole application. If logging is slow, it can affect code that is not directly related to logging.

Modularity is most visible in the separation between `log4j-api` and `log4j-core`. The API module gives applications a stable entry point, while Core contains the implementation. This keeps client code away from most internal classes and makes the public dependency cleaner.

Maintainability depends on the division of responsibilities in the pipeline. Appenders, layouts, filters, and configuration elements have separate roles, so many changes can be isolated. The harder area is the central Core code, where runtime context, configuration, and event dispatching meet.

Integration with other systems depends mostly on appenders and layouts. Log4j2 can write to files, consoles, remote systems, and structured formats because output behavior is modeled through extension points rather than hard-coded in one place.

From a metrics perspective, we expect most complexity to be concentrated in `log4j-core`, while `log4j-api` remains smaller and more stable. This matches the architecture: the public API should stay lightweight, while the implementation module handles the difficult processing. Coupling is expected to be higher around configuration and runtime context classes. Components such as appenders, layouts, and filters should be more cohesive because their responsibilities are narrower and easier to isolate.
