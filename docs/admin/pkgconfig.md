---
title:  Solution Package Configuration
parent: Administrator Guide
nav_order: 1
has_children: false
---

# Solution Package Configuration (`llmgrader_config.xml`)

## Solution Package Overview 

A **solution package** is a lightweight, instructor‑authored bundle that tells the LLM grader which units belong to a course and where to find their XML definitions. It contains:

- a single **configuration file**: `llmgrader_config.xml`
- one **unit XML file** for each unit, each already validated by the instructor
- no source code, no student files, and no extra directories

The [unit XML file](./unitxml.md) describes the questions in each unit, along with reference solutions,
grading notes, point assignments, and other settings.  
Overall the package is small, predictable, and easy to debug.

---

## 📦 Directory Structure of a Solution Package

After running the packaging script, your solution package directory will look like:

```
soln_package/
    llmgrader_config.xml
    unit1_basic_logic.xml
    unit2_numbers.xml
    ...
```

In the future, we will permit the unit XML files and other assets,
such as images, to reside in sub-folders within the package.
But, for now, it is a single flat structure.
When zipped, the archive contains these files at the root level (no nested folder):

```
llmgrader_config.xml
unit1_basic_logic.xml
unit2_numbers.xml
```

This is exactly what the admin upload page expects.

---

## 🧭 Purpose of `llmgrader_config.xml`

Generally, we expect that the course solutions are in some file system,
typically a GitHub repository, although any folder system can be used.
The solution package configuration file, `llmgrader_config.xml` 
describes how to find the unit XML files within that local repository or file system.
Specifically, this file defines:

- the **course metadata** (name, term, etc.)
- the **list of units** included in the package
- the **mapping** from instructor repo paths → packaged filenames

The grader uses this file to:

- load units in the correct order  
- locate each unit’s XML file  
- display course information in the admin UI  


To make the config example concrete, here is a typical instructor solution repository:

```
hwdesign-soln/
    llmgrader_config.xml        ← optional: some instructors keep it here
    unit1/
        basic_logic.xml
        images/
            circuit_diag.jpg
            truth_table.png
    unit2/
        numbers.xml
        images/
            number_line.png
    unit3/
        alu.xml
```

In this example:

- Each unit lives in its own directory (`unit1/`, `unit2/`, …)
- The unit XML file is inside that directory  
- Supporting assets (images, diagrams, etc.) live in subfolders such as `images/`
- The `<source>` paths in `llmgrader_config.xml` refer to these locations

A corresponding minimal configuration file might reference these files like so:

```xml
<llmgrader>
  <course>
    <name>ECE-GY 9463:  Introduction to Hardware Design</name>
    <term>Spring 2026</term>
  </course>

  <units>
    <unit>
      <name>unit1_basic_logic</name>
      <source>unit1/basic_logic.xml</source>
      <destination>unit1_basic_logic.xml</destination>
    </unit>

    <unit>
      <name>unit2_numbers</name>
      <source>unit2/numbers.xml</source>
      <destination>unit2_numbers.xml</destination>
    </unit>
  </units>
</llmgrader>
```

This shows the mapping clearly:

- `<source>` points to the instructor’s repo structure  
- `<destination>` is the filename that will appear in the **flat** solution package (for now)

Later, when nested directories and assets are supported, the `<destination>` paths can mirror the instructor repo structure (e.g., `unit1/basic_logic.xml`), allowing images and other files to be included naturally.



---

Next:  [Describing the units](./unitxml.md) and examples of unit XML files.