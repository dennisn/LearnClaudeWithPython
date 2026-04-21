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

## 001. Initial scaffold

```shell

# with a fresh session/terminal
"implement the implementation plan at "docs/001/02_ImplementationPlan.md""

# create the initial "CLAUDE.md"
/init
```

## 002. Adding unittest & changing the name

- Update CLAUDE.md to add mandatory git branch creation

```shell

"In current project, I want to add unittest for solution 001_two_sum.py"

"Current design means solution name starting with a digit, which is invalid python identifier name. Please change it so the name starts with known prefix instead,
for example "sol_001_two_sum.py" instead of "001_two_sum.py""
```

## 003. Adding solution for "Add Two Numbers"

```shell
I want to add the "Add Two Numbers" solution, with unittest. This is a medium difficulty problem, described at https://leetcode.com/problems/add-two-numbers/description/
```

## 004. Adding solution for "Median of Two Sorted Arrays"

```shell
I want to add the "Median of Two Sorted Arrays" solution, with unittest. This is a hard difficulty problem, with following specs: "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.". 
Do not implement the solution, but create the framework for me to solve it
```
