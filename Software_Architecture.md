# Report: Software Architecture

**Note** Max 2500 words except diagrams. The goal of this
document is describe the software architecture of the system using the C4 model (levl 1, 2 and 3).

 **After the word limit, teachers reserve the right to stop reading, which may affect the teams’ grade**

 ---

## Table of Contents

- [Report: Software Architecture](#report-software-architecture)
  - [Table of Contents](#table-of-contents)
  - [1. Tooling](#1-tooling)
  - [2. Context Level](#2-context-level)
  - [3. Container Level](#3-container-level)
  - [4. Component Level](#4-component-level)
  - [5. Architectural Characteristics](#5-architectural-characteristics)

---

**Goal**:  *document and describe the architecture of the system*


## 1. Tooling

The diagrams were created using PlantUML and the C4-PlantUML library.  
This approach makes the diagrams easier to modify and maintain during the analysis process.

## 2. Context Level

The Context diagram shows how Apache Log4j2 interacts with external applications and logging targets.  
At this level, the goal was to understand the role of the framework inside a larger system.

## 3. Container Level

The Container diagram focuses on the main Log4j2 modules and their responsibilities.  
Particular attention was given to the separation between the API and the Core module.

- **Clean Architecture:** _Did you find any relationship with the Clean Architecture blueprint?_

## 4. Component Level

_Insert the Component diagrams and their explanations._ _(Justify your decisions if you had to discard specific containers)._

- **SOLID Principles:** _Did you observe any violations of the SOLID principles at this level?_

## 5. Architectural Characteristics

_Comment on the important architectural characteristics/qualities of the system._ * **Architecture Support:** *How are these characteristics supported by the architecture?\*

- **Metrics:** _You can use coupling and cohesion metrics to support your reasoning._
