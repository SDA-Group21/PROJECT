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
This approach makes the diagrams easier to modify and maintain during the analysis process.
For this report, using diagrams as code was useful because the model changed a few times while we were deciding where to put the boundaries. With PlantUML, the diagrams can be reviewed in the repository in the same way as the Markdown files, instead of being separate images edited manually.

The Context and Container diagrams are in the `architecture` directory:

- `architecture/context.puml`
- `architecture/container.puml`

We did not try to describe every module in the Apache Log4j2 repository. The project is larger than the part that is useful for this analysis. We focused on the logging pipeline and especially on the boundary between `log4j-api` and `log4j-core`, because that is where the architecture becomes clear: application code sees the API, while the actual processing is handled by Core.

## 2. Context Level

The Context diagram shows how Apache Log4j2 interacts with external applications and logging targets.
At this level, the goal was to understand the role of the framework inside a larger system.
In the diagram, Log4j2 is treated as a black box. A Java application sends log events to it during execution, and a developer decides how the framework should behave by writing or changing configuration files. In C4 terms, the Java application is better seen as an external software system, not as a person. The developer is the human actor because they integrate and configure Log4j2.

The diagram shows three common logging targets: the file system, the console, and remote logging systems. They are outside the framework. The application does not need to know which of these targets will be used. It only makes a logging call, and Log4j2 uses the active configuration to decide where the event goes.

This is the main architectural role of the framework. It keeps logging decisions out of the application logic. For example, changing from console logging to file logging, or from a plain text layout to a JSON layout, should mostly be a configuration change rather than a change in the application code.

## 3. Container Level

The Container diagram focuses on the main Log4j2 modules and their responsibilities.
Particular attention was given to the separation between the API and the Core module.
This separation is the most relevant part of the Container view.

`log4j-api` is the part used directly by application developers. It contains the public logging interface: loggers, logging methods, levels, markers, and the types needed to make logging calls. Its job is not to perform all logging work, but to give client code a stable surface to depend on.

`log4j-core` is where the implementation lives. It receives events coming from the API side, applies the active configuration, checks filters, calls appenders, and manages the runtime context. In practice, this is the module that turns a simple call such as `logger.info(...)` into output written to a file, console, socket, or another destination.

The Configuration System loads external configuration files. Log4j2 supports XML, JSON, YAML, and properties files. This is important because logging requirements usually change between environments. A developer machine may only need console output, while a production deployment may need rolling files or a remote collector.

The Plugin System is the extension point of the framework. Appenders, layouts, filters, and other configuration elements can be discovered as plugins. This avoids hard-coding every possible destination or format inside the core pipeline.

The Async Logging part represents the asynchronous path based on LMAX Disruptor. When this mode is enabled, the application thread can hand off the event instead of doing all the logging work directly. This matters for applications where logging is frequent and blocking I/O would be too expensive.

Appenders write accepted events to concrete destinations such as files, consoles, sockets, databases, or remote systems. Layouts are used before that final write. They convert the structured event into the representation expected by the destination, for example a pattern-based string, JSON, or CSV.

So the runtime path is quite simple at this level: application code calls the API, the API reaches Core, Core applies configuration and plugin-based behavior, and appenders with layouts produce the final output.

### Clean architecture relationship

Log4j2 is not really a Clean Architecture system in the usual sense. Clean Architecture is normally discussed for business applications, where entities and use cases are placed at the center. Log4j2 is different: it is a technical framework, and the center of the design is the processing of log events.

Still, there is one clear similarity. Application code depends on `log4j-api`, not on the internal classes of `log4j-core`. This keeps implementation details behind a public boundary. For this reason, I would describe the relationship with Clean Architecture as partial: Log4j2 follows the idea of dependency control, but it is not structured around Clean Architecture layers.

## 4. Component Level

For the Component level, we expanded `log4j-core`. This is the container where most runtime decisions are made, so it gives more information than expanding the API module. We did not expand every container because that would make the diagram larger without adding much to the architectural explanation. `log4j-api` mostly defines the public surface, while appenders, layouts, filters, and plugins make sense as parts of the Core processing pipeline.

The components selected for the diagram are:

- `LoggerContext`: keeps the active logging context and connects loggers to the current configuration.
- `Configuration`: stores the logger configuration, appenders, filters, layouts, and related settings.
- `LoggerConfig`: applies the effective rules for a logger and decides how an event is processed.
- `Filter`: decides whether an event is accepted, rejected, or passed to the next step.
- `Appender`: writes accepted log events to a concrete destination.
- `Layout`: converts a log event into the format required by the appender.
- `LogEvent`: carries the data produced by a logging call.
- `AsyncLogger` or asynchronous logging components: move part of the work away from the application thread when asynchronous logging is used.

The following C4 Component diagram shows the event flow inside `log4j-core`:

```plantuml
@startuml

!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Container_Boundary(core, "log4j-core") {
    Component(loggerContext, "LoggerContext", "Java class", "Manages the active logging context")
    Component(configuration, "Configuration", "Java interface/class hierarchy", "Stores logger, filter, appender, and layout configuration")
    Component(loggerConfig, "LoggerConfig", "Java class", "Applies logger-specific configuration to log events")
    Component(filter, "Filter", "Java interface", "Accepts, denies, or passes log events")
    Component(logEvent, "LogEvent", "Java interface", "Represents a structured logging event")
    Component(asyncLogger, "Async Logging Components", "Java classes / LMAX Disruptor", "Processes log events asynchronously")
    Component(appender, "Appender", "Java interface", "Writes log events to a destination")
    Component(layout, "Layout", "Java interface", "Formats log events for output")
}

System_Ext(destination, "Logging Destination", "File system, console, or remote system")

Rel(loggerContext, configuration, "Uses active configuration")
Rel(configuration, loggerConfig, "Provides logger rules")
Rel(loggerConfig, filter, "Evaluates event")
Rel(loggerConfig, logEvent, "Processes")
Rel(loggerConfig, asyncLogger, "Can delegate to")
Rel(loggerConfig, appender, "Sends accepted events")
Rel(asyncLogger, appender, "Dispatches events")
Rel(appender, layout, "Formats with")
Rel(appender, destination, "Writes to")

@enduml
```

The flow can be read as a pipeline. A logging call creates a `LogEvent`. The active configuration selects the relevant `LoggerConfig`. Filters may stop the event, or they may let it continue. If the event is accepted, an appender receives it, the layout formats it, and the appender writes the result to the destination.

### SOLID principles

At component level, Log4j2 mostly follows SOLID, although the central coordination classes are more coupled than the smaller extension components.

The Single Responsibility Principle is visible in the separation between filters, appenders, layouts, and configuration objects. A filter makes decisions about events. A layout formats events. An appender writes them somewhere. These responsibilities are separate enough to make the design understandable.

The Open/Closed Principle is probably the strongest part of the design. New appenders, layouts, and filters can be added through the plugin mechanism without changing the main processing flow. This is a good fit for a logging framework, because users often need new destinations or formats.

The Dependency Inversion Principle appears in the use of interfaces such as `Appender`, `Layout`, and `Filter`. Core code can work through these abstractions instead of depending only on concrete implementations. At a higher level, applications depend on `log4j-api` rather than directly on `log4j-core`.

The Interface Segregation Principle is also reasonably respected, since extension points are split into separate interfaces instead of one large interface for every logging component. The Liskov Substitution Principle is expected for implementations of these interfaces: a custom appender or layout should be usable wherever the corresponding interface is expected.

The weaker area is around `LoggerContext`, `Configuration`, and `LoggerConfig`. These classes connect many parts of the runtime. This is not automatically a SOLID violation, because a logging framework needs some central coordination, but these are the classes where changes are more likely to have wider effects.

## 5. Architectural Characteristics

The architecture of Log4j2 seems to be driven by two practical needs: it must be easy to adapt, and it must not make application execution too slow. Several architectural qualities follow from this.

Extensibility is handled through the Plugin System and through abstractions such as appenders, layouts, and filters. A project can add a new destination or output format without changing the whole framework. This is especially important for Log4j2 because logging targets vary a lot between applications.

Configurability is handled through external files. Developers can define logger hierarchies, levels, appenders, layouts, and filters outside the application code. This makes the same application easier to move between environments, for example from a local setup to a production deployment.

Performance is addressed through asynchronous logging and through the separation between creating an event and delivering it. With LMAX Disruptor, Log4j2 can reduce blocking on application threads when asynchronous logging is enabled. This matters because logging is spread across the whole application. If logging is slow, it can affect code that is not directly related to logging.

Modularity is most visible in the separation between `log4j-api` and `log4j-core`. The API module gives applications a stable entry point, while Core contains the implementation. This keeps client code away from most internal classes and makes the public dependency cleaner.

Maintainability depends on the division of responsibilities in the pipeline. Appenders, layouts, filters, and configuration elements have separate roles, so many changes can be isolated. The harder area is the central Core code, where runtime context, configuration, and event dispatching meet.

Integration with other systems depends mostly on appenders and layouts. Log4j2 can write to files, consoles, remote systems, and structured formats because output behavior is modeled through extension points rather than hard-coded in one place.

From a metrics perspective, we expect most complexity to be concentrated in `log4j-core`, while `log4j-api` remains smaller and more stable. This matches the architecture: the public API should stay lightweight, while the implementation module handles the difficult processing. Coupling is expected to be higher around configuration and runtime context classes. Components such as appenders, layouts, and filters should be more cohesive because their responsibilities are narrower and easier to isolate.
