# Individual Journal: Danielyan Srbuhi - s337777

## Contribution Tracking

### 10.05.2026

Started analyzing the architecture of Apache Log4j2 and looking through the project structure and main modules.
Focused on understanding how the logging flow works and how the project separates API, core logic, and extensions.

### 13.05.2026

Today I continued exploring the architecture of Apache Log4j2 and spent time understanding the role of the main modules such as `log4j-api`, `log4j-core`, appenders, layouts, async logging, configuration handling, and plugins.

I also set up PlantUML with C4 diagrams support and started creating the first architecture diagrams for the project. Created initial versions of the Context Diagram and Container Diagram and adjusted them after reviewing the C4 model structure more carefully.

Spent additional time checking how the main modules communicate with each other and how log events move through the system.

### 21.05.2026

Today I refactored the Container Diagram after spending more time understanding the C4 model and the actual structure of the Log4j2 repository.

Removed internal parts such as appenders, layouts, plugins, configuration handling, and async logging from the Container Diagram because they are not separately deployable modules. Moved them to the Component Diagram of `log4j-core` instead.

Updated the Container Diagram to focus on the real Log4j2 modules like `log4j-api`, `log4j-core`, `log4j-slf4j2-impl`, and `log4j-jul`.

Also added the first version of the `log4j-core` Component Diagram to represent the main internal logging flow and communication between the core components.

### 25.05.2026

Today I continued working on the architecture analysis and improved the Component level diagrams for both `log4j-core` and `log4j-api`.

Spent more time analyzing the separation between the public API layer and the internal logging engine. Added a separate component diagram for `log4j-api` to better represent the main abstractions exposed to applications, such as `Logger`, `LogManager`, `Message`, `Marker`, `Level`, and `ThreadContext`.

Also refined the `log4j-core` component diagram and adjusted the structure of the runtime logging pipeline after reviewing the repository and the relationships between the main processing components more carefully.

Updated the architecture report to keep the explanations consistent with the new diagrams and the C4 abstraction levels.


### 27.05.2026

Today I created an integrated Component Diagram showing the collaboration between the main Log4j2 modules and runtime components.

Spent time connecting log4j-api, log4j-core, bridge modules, appenders, layouts, async logging, and external outputs into one runtime architecture view. Also adjusted the layout to better represent log4j-core as the central runtime processing engine of the framework.
 