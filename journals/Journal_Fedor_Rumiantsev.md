# Individual Journal: Fedor Rumiantsev - s336891

## Contribution Tracking

### 20.05.2026

Worked on the Software Architecture report: added C4 explanation, component-level view, SOLID discussion, architectural characteristics.

### 23.05.2026

Looked at the core patterns in Log4j2, specifically the API-vs-Core split and how extension points (appenders, layouts, filters) work. Drafted new notes on framework modularity and maintainability.

### 25.05.2026

Reviewed the Software Architecture draft. Spent most of the time mapping C4 model boundaries to the actual Log4j2 codebase, making sure the line between high-level context and internal component detail is clear.

### 28.05.2026

Worked on the component-level section. Focus was on the exact boundaries between `log4j-api` and `log4j-core`, checking how logging calls travel from application code into the actual processing logic.

### 04.06.2026

Checked the draft Context, Container, and Component diagrams for consistency, discussed them with others. Noted a few discrepancies in how external systems and dependencies are represented compared to the text. Cleaned up component and container descriptions. Aligned terminology across all three C4 diagrams so it matches what is actually in the repository.

### 06.06.2026

Reviewed the new C4 diagrams from Srbuhi Danielyan. They match the abstraction levels well and help clarify the final report.

### 07.06.2026

Updated Software_Architecture.md with the final diagrams. Rewrote the C4 level descriptions, added the flow details for bridge modules, and linked the relative diagram paths.
