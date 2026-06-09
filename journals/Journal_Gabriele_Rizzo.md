# Individual Journal: Gabriele Rizzo - s352512

## Contribution Tracking

 I was entirely responsible for drafting the Overview section, and I provided review and support for the Software Design section

# 07/05/2026

1 Overview Purpose
I reviewed the project information at
[source](https://logging.apache.org/log4j/2.x/manual/index.html)
to understand what it is, its use cases, and the contexts in which it can be applied. This helped me grasp the project's overall scope. Following this, I drafted the 'Purpose' section in the Overview.md file.

2 Overview Stakeholders

2.1
Then i cloned the repo [source](https://github.com/apache/logging-log4j2).
At this point, I attempted to export the directory structure to a text file using tree > dir.txt. However, I realized that the sheer volume of files and directories is too high, making this an ineffective approach for gaining a global overview of the project's structure.
For the time being, I have set this aside and pivoted to identifying the project's stakeholders. I began by checking the contributors on GitHub and analyzing the team members. I initially consulted [source](https://logging.apache.org/log4j/2.3.x/team-list.html), but found it to be outdated. I then moved to [source](https://logging.apache.org/team-list.html) where I successfully identified the active team and their respective roles, as well as the inactive members (including the founder of Log4j, Ceki Gülcü).

I attempted to identify the different types of project contributors by analyzing the statistics in the GitHub Insights section and cross-referencing the team members with the top contributors

2.2
To identify the external stakeholders, I analyzed several key areas:
- Maven Central Repository: I found that Log4j has over 20,000 usages [source](https://mvnrepository.com/search?q=log4j) furthermore, the official documentation's introduction section explicitly that the framework is targeted at Java developers.
- Indirect Users: I investigated potential indirect users, specifically focusing on Minecraft. I verified its dependency on Log4j through both online research and direct terminal inspection:
    
    <img src="https://i.imgur.com/NUmQ1aA.png" alt="Logo Log4j" width="800">

    Additionally, I conducted further research to identify other indirect users.
- Institutional Involvement: I looked into the organizations orbiting Log4j beyond the owner (ASF). I found that OpenSSF backs and defends Log4j, as it is considered a critical piece of international software framework (especially subsequent to the 2021 Log4Shell occurrences). Similarly, CISA maintains updated databases of vulnerable Log4j versions and mandates that federal agencies update to the latest patched releases


# 08/05/2026
3

In this part, I spent some time reading information about the project from the official website, and then I analyzed the `log4j-api` and `log4j-core` directories to better understand how the connection between the API side and the Core side works. I also tried to identify the starting point of the framework and understand which components play the most important roles inside the system.

For example, one of the main files I analyzed was `LoggerContext`, since it represents the direct link between the Core and the API parts of the framework.


4 Code Statistics
"In this section, I first identified the most relevant information to include in the system overview. Subsequently, I utilized specific commands (such as 'cloc') to calculate all the necessary metrics and statistics.
I used grep -rE "^\s*(public|protected|private).*\(" log4j-core/src/main/java | grep -v "class " | wc -l for #method and find log4j-core/src/main/java -name "*.java" | wc -l  for class

`10/05/2026`

`Point 1`

I have analyzed the file `Software_Design.md`.

The script created by Cristiano works correctly, i created my own and obtained the same result.
I believe there is a slight imprecision in the description of `AbstractConfiguration.java`; they are right to define it as the orchestrator, but I wanted to specify that it is precisely the manager of the component graph.
This is because, analyzing the code:

```
private ConcurrentMap<String, Appender> appenders = new ConcurrentHashMap<>();
private ConcurrentMap<String, LoggerConfig> loggerConfigs = new ConcurrentHashMap<>();
private List<CustomLevelConfig> customLevels = Collections.emptyList();
```

we find the data structures that store the components of the graph.

then, for example, in the `doConfigure()` method, it transforms textual references into physical links, e.g., it associates `AppenderRef` with the actual instance of an `Appender` present in the map.

Through the `setParents()` method, it defines a tree structure that allows logs to propagate from a child logger to a parent one.

Describing `AbstractConfiguration.java` as the manager of the component graph also justifies its high Fan-Out, as to build the graph it must import and know every single existing component; if it were only an abstract orchestrator, it could delegate the creation of the pieces to another external component.

`Point 2`

`LoggerContext` acts as a bridge, as explained by Cristiano, between the API and Core, and this is evident because by implementing org.apache.logging.log4j.spi.LoggerContext in log4j-api, this class—which lives in the Core—makes itself available to the API (LogManager) to provide logging services requested by the user code.

Furthermore, however, it must be noted that LoggerContext plays the role of an anchor, as it maintains a list of all the loggers requested by applications; this is also documented at line 67 of the file logging-log4j2/log4j-core/src/main/java/org/apache/logging/log4j/core/LoggerContext.java.

Lowest Fan-Out is fine as it is.

Regarding the Knowledge Dependencies part, it seems very accurate and well done, and I believe there is nothing to add; structural dependencies (code) and process dependencies (commit history) have been distinguished.
The 3 identified patterns explain well why those files change together despite the absence of direct imports.

# 23-05-2026 and 24-05-2026

I have reviewed the section completed by Beatrice and Cristiano regarding the Patterns, and I noticed that they have also updated the Code and Knowledge dependencies part.

Since I consider this section to be very well structured, I have no specific modifications to suggest.

Instead, I proceeded to create 3 diagrams:

### A high-level diagram to show the relationship between the core classes and methods (it fits well within the Software Design section and provides a general overview)

![ClassDiagram](../images/Software_Design/ClassDiagram.png)

- I have mapped the main interfaces and classes of the project, which constitute the entry point and the log processing chain: `LogManager` (facade), `LoggerContextFactory` (interface factory), `SimpleLoggerContextFactory` (fallback Singleton), `LoggerContext`, `InternalLoggerRegistry` (cache/flyweight), `Logger`, `LoggerConfig`, `Appender`, `Filter` e `CompositeFilter`.
- Examples of methods highlighted in the diagram and present in the code:
    - `org.apache.logging.log4j.LogManager#getLogger(...)` e `#getContext(...)` (use factory and obtain `LoggerContext`).
    - `org.apache.logging.log4j.spi.LoggerContextFactory#getContext(...)` (context creation contract).
    - `org.apache.logging.log4j.simple.SimpleLoggerContextFactory#INSTANCE` (fallback singleton instance).
    - `InternalLoggerRegistry#getLogger(name, messageFactory)` (cache with `computeIfAbsent` that implement Flyweight pattern).


### A diagram showing the Logger creation sequence, in this case the purpose is to illustrate how LogManager uses the factory and how the registry provides a Logger (Facade, Singleton, Flyweight).


![LoggerCreationSequence](../images/Software_Design/LoggerCreationSequence.png)

The diagram shows the precise sequence:
- `Client` invokes `LogManager.getLogger(...)`
- `LogManager` consults `LoggerContextFactory` (or resorts to `SimpleLoggerContextFactory.INSTANCE` if the factory is not available)
- il `LoggerContext` select `MessageFactory` (es `StringFormatterMessageFactory.INSTANCE`) and delegates the resolution/creation of the `Logger` to `InternalLoggerRegistry` that use `computeIfAbsent` to return a shared instance (flyweight) or create a new one.
`LogManager.getContext()` use `factory.getContext(...)` and in the catch block falls back on `SimpleLoggerContextFactory.INSTANCE.getContext(...)`

### A diagram showing the life cycle of the data and demonstrating the chain of Responsibility, which was explained in chapter 2.4, providing a visual understanding of how CompositeFilter queries the various filters.

![LogEventFlowSequence](../images/Software_Design/LogEventFlowSequence.png)

- The diagram illustrates the path of the `LogEvent` at runtime:
call to the `Logger` (flyweight) -> resolution of `LoggerConfig` via `LoggerContext` -> invocation of the `CompositeFilter` which iterates through the registered `Filters` (Chain of Responsibility) -> if accepted, dispatch to the `Appenders` and formatting with the `Layout`.

`LoggerConfig` is the component that receives and dispatches the event toward `CompositeFilter` and `Appenders`.
The classes `AbstractFilterable`, `CompositeFilter`, and the `Filter` implementations determine the result (`ACCEPT`/`DENY`/`NEUTRAL`), as described in chapter 2.4 of the design document.

