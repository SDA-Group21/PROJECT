# Report: Software Architecture

## Table of Contents

- [Report: Software Architecture](#report-software-architecture)
  - [Table of Contents](#table-of-contents)
  - [1. Tooling](#1-tooling)
  - [2. Context Level](#2-context-level)
  - [3. Container Level](#3-container-level)
    - [Clean architecture relationship](#clean-architecture-relationship)
  - [4. Component Level](#4-component-level)
    - [Components](#components)
    - [Execution Flow](#execution-flow)
    - [SOLID principles](#solid-principles)
  - [5. Architectural Characteristics](#5-architectural-characteristics)

## 1. Tooling

The Context, Container, and Component diagrams are located in the [architecture](architecture) directory:

- [context.jpg](architecture/context.jpg)
- [container.jpg](architecture/container.jpg)
- [component.jpg](architecture/component.jpg)

We did not try to describe every module in the Apache Log4j2 repository because the project is significantly larger than the part relevant for this analysis. Instead, we focused mainly on the logging pipeline and especially on the separation between `log4j-api` and `log4j-core`, since this boundary represents the central architectural idea of the framework: application code interacts with the API, while the actual logging implementation and runtime processing are handled inside Core.

## 2. Context Level

The [Context diagram](architecture/context.jpg) shows how Apache Log4j2 interacts with external applications, facade interfaces, and logging targets.

In the diagram, Log4j2 is a black box. The main systems interacting with it are:

- A standard Java application invoking the Log4j2 API directly.
- The SLF4J API, routing its logging calls through the Log4j2 engine.
- The java.util.logging API, also redirecting its events to Log4j2.

On the output side, the framework translates these calls into writes to three external targets:

- The File System, using File I/O.
- The Console, using Standard Output.
- Remote Logging Systems, using Network I/O.

A developer decides how the framework behaves by writing or changing configuration files. In C4 terms, the Java application and facades are external software systems rather than human actors. The developer remains the primary human actor responsible for integration and configuration.

This setup highlights the main architectural role of the framework: keeping logging decisions out of application logic. For example, changing from console logging to file logging, or from plain text to JSON, is purely a configuration change. The application and facade calls remain unchanged.

## 3. Container Level

The [Container diagram](architecture/container.jpg) shows the modular structure of Apache Log4j2. The framework consists of four primary containers:

- `log4j-api`: The public logging interface. Applications use this module directly to manage loggers, markers, levels, and context.
- `log4j-core`: The central logging engine. It processes log events, checks configurations, runs filters, formats messages, and writes the output.
- `log4j-slf4j2-impl`: A bridge that intercepts SLF4J API calls and translates them into Log4j2 API operations.
- `log4j-jul`: A bridge that routes standard `java.util.logging` events into Log4j2 API calls.

This design decouples client applications from the concrete engine. The runtime flow follows a clear hierarchy:

1. Applications or external facades initiate a logging call.
2. Bridge modules (`log4j-slf4j2-impl` or `log4j-jul`) forward facade calls to `log4j-api` using method calls.
3. The `log4j-api` container routes these requests to `log4j-core` using method calls.
4. The `log4j-core` container processes the logging event and writes the output to the File System (File I/O), Console (Standard Output), or Remote Logging Systems (Network I/O).

### Clean architecture relationship

Log4j2 is not really a Clean Architecture system in the usual sense. Clean Architecture is normally discussed for business applications, where entities and use cases are placed at the center. Log4j2 is different: it is a technical framework, and the center of the design is the processing of log events.

Still, there is one clear similarity. Application code depends on `log4j-api`, not on the internal classes of `log4j-core`. This keeps implementation details behind a public boundary. For this reason, I would describe the relationship with Clean Architecture as partial: Log4j2 follows the idea of dependency control, but it is not structured around Clean Architecture layers.

## 4. Component Level

The unified [Component diagram](architecture/component.jpg) diagram details the internal elements of both the API and Core modules, along with the bridge adapters.

### Components

The architecture relies on several primary components across the different modules:

- **log4j-api components**:
  - `LogManager`: The entry point for applications to look up and retrieve logger instances.
  - `Logger`: The primary interface that applications interact with for logging calls.
  - `ExtendedLogger`: An internal API extension that coordinates log event creation and hands off processing to the core module.
  - `Message`: Encapsulates message data and formats.
  - `Level`: Represents the severity of the log event.
  - `Marker`: Allows tagging log statements for group filtering.
  - `ThreadContext`: Stores context data bound to the current execution thread.
- **log4j-core components**:
  - `LoggerContext`: Manages the overall logging state and references the active configuration.
  - `Configuration`: Houses the rules, filters, appenders, layouts, and plugins currently active.
  - `LogEvent`: A container object wrapping all relevant context, payload, and thread data.
  - `LoggerConfig`: The central coordinator in the core module that routes events based on configuration rules.
  - `Filter`: Evaluates whether a log event should be written or discarded.
  - `AsyncLogger`: Implements asynchronous execution using the LMAX Disruptor queue.
  - `AppenderControl`: Manages thread safety and coordinates sending events to appenders.
  - `Appender`: The component responsible for writing log messages to specific external channels.
  - `Layout`: Transforms log events into text or binary formats before writing.
  - `PluginManager`: Discovers and dynamically loads custom appenders, filters, and layouts.
- **Bridge components**:
  - `SLF4J Adapter` (in `log4j-slf4j2-impl`): Intercepts SLF4J API logs and forwards them to the Log4j2 `Logger`.
  - `JUL Adapter` (in `log4j-jul`): Intercepts JDK standard logs and redirects them to the Log4j2 `Logger`.

### Execution Flow

The logging pipeline flows across the API-to-Core boundary in a sequence of steps:

1.  **Call Interception**: An application calls the `Logger` directly, or an external facade routes the call through its adapter (`SLF4J Adapter` or `JUL Adapter`) to the `Logger`.
2.  **Event Creation**: The `Logger` packages the log details (`Message`, `Level`, `Marker`, and `ThreadContext`) into a `LogEvent` object.
3.  **Boundary Handoff**: The `Logger` delegates to `ExtendedLogger`, which passes the `LogEvent` to the core module's `LoggerConfig`.
4.  **Configuration & Filtering**: `LoggerConfig` retrieves configuration settings from the active `Configuration` (obtained via `LoggerContext`) and runs any specified `Filter` checks.
5.  **Dispatching**:
    - _Synchronous_: `LoggerConfig` passes the event directly to `AppenderControl`.
    - _Asynchronous_: `LoggerConfig` hands the event to `AsyncLogger`. The LMAX Disruptor processes it on a separate thread and then dispatches it to `AppenderControl`.
6.  **Formatting & Write**: `AppenderControl` invokes the appropriate `Appender`. The appender uses a `Layout` to format the message and writes the output to the destination.

### SOLID principles

Log4j2 adheres to the SOLID principles at the component level:

The Single Responsibility Principle shows in the clean split between configuration, filtering, formatting (`Layout`), and output dispatching (`Appender`). Each component manages a narrow, dedicated step in the pipeline.

The Open/Closed Principle is visible through the Plugin System. `PluginManager` dynamically loads new `Appender`, `Layout`, or `Filter` implementations at startup. Developers can extend the framework without rewriting any core code.

The Dependency Inversion Principle is supported by using abstractions like `Appender`, `Layout`, and `Filter`. The runtime engine works with these interfaces rather than concrete implementations, and applications depend on the high-level `log4j-api` interface instead of the `log4j-core` engine.

The Interface Segregation Principle is visible in the design of clean, small interfaces instead of single, heavy APIs.

Some tight coupling exists around the core orchestrators: `LoggerContext`, `Configuration`, and `LoggerConfig`. This central coordination is hard to avoid, but isolating it inside these classes protects the rest of the logging pipeline.

## 5. Architectural Characteristics

The design of Log4j2 centers on two primary goals: flexibility and execution speed.

Extensibility relies heavily on the Plugin System and `PluginManager`. By coding against abstract interfaces like `Appender`, `Layout`, and `Filter`, developers can introduce new output channels or formats without modifying the core engine.

Configurability is managed through external configuration files. The `LoggerContext` links these files to the active runtime configuration, allowing developers to change levels, appenders, and filtering rules dynamically without recompiling application code.

Performance depends on the asynchronous logging pipeline. By routing events through `AsyncLogger` and the LMAX Disruptor, the framework delegates the expensive I/O operations to background threads, minimizing the performance impact on the application's execution path.

Modularity is enforced by splitting the framework into `log4j-api` and `log4j-core`. Keeping client applications dependent only on the API protects them from changes to the underlying logging engine.

Integration is simplified by the bridge modules (`log4j-slf4j2-impl` and `log4j-jul`). These libraries adapt calls from other logging facades so they can be processed by the same core engine.

As a result, most code complexity is concentrated in `log4j-core`, while `log4j-api` remains small and stable. Coupling is naturally higher around orchestrating components like `LoggerConfig` and `Configuration`, whereas appenders and layouts show high cohesion because they perform single, well-defined tasks.
