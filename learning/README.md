# Overview

This is to document the process of using Claude to develop this project

## Planning v1

```shell
# start the planning process with a rough specs
/plan

# NOTE: in "plan" mode, Claude can't write to file. It's also keen to execute the plan right away, so not so easy to review the plans
# ==> need to firmly ask it to write to a file for review & record keeping
"I want to create a web application using Python with minimal CSS usage. The application is to showcase my solutions to leetcode problems. Essentially, its main page will list all the available solutions in a tree-like structure, where solutions are grouped by their difficulties level. Each solution will have its own page, where user can enter the parameters, run the code and receive the result.
Please create 3 alternative designs with its pros & cons"
```

## Planning v2

Re-do the planning a-fresh

```shell
# Clear the context to restart fresh
/clear

"Starting from scratch, I want to create a web application using Python with minimal CSS usage. The application is to showcase my solutions to leetcode problems. Essentially, its main page will list all the available solutions in a tree-like structure, where solutions are grouped by their difficulties level. Each solution will have its own page, where user can enter the parameters, run the code and receive the result.
Please create 3 alternative designs with its pros & cons"

# Once the plan is accepted, it will ask for decision to implementation
"no, I want to write out the plan for more review"

"what is the pro & cons between Flask & FastAPI ?"

"I think I'm learning toward design A. Please provide an implementation approach"

"First, please write the original design plans to "docs/001/01_InitialPlan.md", and the implementation plans to "docs/001/02_ImplementationPlan.md""
```
