# Report: Software Design

**Note** Max 2500 words except diagrams. 

**After the word limit, teachers reserve the right to stop reading, which may affect the teams’ grade**

---

## Table of Contents

- [Report: Software Design](#report-software-design)
  - [Table of Contents](#table-of-contents)
  - [1. Dependencies](#1-dependencies)
    - [1.1 Methodology and Tools](#11-methodology-and-tools)
    - [1.2 Code Dependencies](#12-code-dependencies)
    - [1.3 Knowledge Dependencies](#13-knowledge-dependencies)
  - [2. Patterns](#2-patterns)
    - [2.1 Pattern 1: \[Pattern Name\]](#21-pattern-1-pattern-name)
  - [3. Summary](#3-summary)

---

## 1. Dependencies

### 1.1 Methodology and Tools

_Describe the methods and tools used to analyze the dependencies and the results obtained._
In the following sections, some custom Python scripts were used for a static analysis of the code. 

In particular, in the Code Dependencies section, the static analysis was performed utilizing regular expressions to identify imports within the the two core components: log4j.core and log4j-api. Tests and `package-info.java` were excluded from this analysis as they were not considered important for the purpose of this study. 
However, there are some limitations reguarding the use of Python scripts compared to the use of professional tools. In fact, in Java language, the imports of intra-package classes are not required. This can cause some variations of the results. Reguardless of this, the analysis remains a good metric for the inter-package relationships. 

To analyze the knowledge dependencies, the commit history was extracted from the Apache Log4j Git Repository. Using a Python script, it was possible to filter the commit history for `.java` files and to track how often two files were modified together in the same commit. A minimum threshold of 15 "co-changes" was added to focus only on the most meaningful relationships. 

### 1.2 Code Dependencies

_Evaluate code dependencies based on the imports in the source code._

- **Most/Least dependent files:** _Indicate which files have the most or least dependencies and explain why._

### 1.3 Knowledge Dependencies

<!--_Evaluate knowledge dependencies based on co-change (how often two files are modified together in the same commit)._-->

Understandably, the results of the Python script showed some obvious connections, like direct dependencies between a class and its testing class (for example, `RingBufferLogEvent.java` changing with `RingBufferLogEventTest.java`). However, the most instresting dependecies are those where there are no strong links, like structural dependencies, between the files. 

  <!--_**Inconsistencies:** Which knowledge dependencies are inconsistent with the code dependencies?_-->
We found some cases in which two files have a high co-change rate but don`t actually import each other in the code. These fall into three main architectural patterns: 
1. **Keeping Output Formats in Sync (Layouts):**
   The most frequently co-changed pair in the analysis (28 times) was `JsonLayout.java` and `XmlLayout.java`, followed by (21 times) `JsonLayout.java` and `YamlLayout.java`. These files sit in the same package, but they never call each other. They change together because of feature parity: whenever developers add a new detail to the logs, they have to update all the layout files at the same time so it works in every format.
2. **Standard vs. "Garbage-Free" Implementations:**
   Another big inconsistency is between `CopyOnWriteSortedArrayThreadContextMap.java` and `GarbageFreeSortedArrayThreadContextMap.java` (24 co-changes). Log4j provides a standard implementation and a "garbage-free" one, for high performance tasks. Since they basically do the same thing, every time a change is needed in one of them, it has to be mirrored in the other. 
3. **Configuration and Security Setup:**
    Finally, files that handle configuration or security setup change together. For example, `KeyStoreConfiguration.java` and `TrustStoreConfiguration.java` (19 co-changes) don`t interact in the code, but, since they both deal with security certificates, they often change together. The same logic applies to configuration files, for example `JsonConfiguration.java` and `XmlConfiguration.java` (19 co-changes). Since both configuration files do the same operations, but with different formats, their behaviors need to change similarly. 

In conclusion, the inconsistencies found in Log4j are design choices, not architectural flaws. They are necessary to ensure feature parity, optimize performance, and keep parallel configurations synchronized across independent files. 

## 2. Patterns

_Identify at least 4 instances of design patterns in the code._ _Include links to the source code for each._

### 2.1 Pattern 1: [Pattern Name]

- **Roles:** _Which classes play which role?_
- **Problem Solved / Rationale:** _Why is this pattern used? What problem does it solve?_
- **Alternatives:** _Is there an alternative? What would be the pros and cons?_

_(Repeat the structure for Patterns 2, 3, and 4)_

## 3. Summary

_Summarize the results regarding the two design aspects (Dependencies and Patterns)._
