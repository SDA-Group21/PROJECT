# Individual Journal: Gabriele Rizzo - s352512

## Contribution Tracking

07/05/2026

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


08/05/2026
3

In this part, I spent some time reading information about the project from the official website, and then I analyzed the `log4j-api` and `log4j-core` directories to better understand how the connection between the API side and the Core side works. I also tried to identify the starting point of the framework and understand which components play the most important roles inside the system.

For example, one of the main files I analyzed was `LoggerContext`, since it represents the direct link between the Core and the API parts of the framework.


4 Code Statistics
"In this section, I first identified the most relevant information to include in the system overview. Subsequently, I utilized specific commands (such as 'cloc') to calculate all the necessary metrics and statistics.
I used grep -rE "^\s*(public|protected|private).*\(" log4j-core/src/main/java | grep -v "class " | wc -l for #method and find log4j-core/src/main/java -name "*.java" | wc -l  for class