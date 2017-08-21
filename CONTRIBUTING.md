# Contributing Guidelines

Thanks for interest in contributing to MTF.

The following is a set of guidelines for contributing to MTF. These are not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## How to contribute to MTF

### Reporting Bugs

Before creating bug reports, please check a [list of known issues](https://github.com/fedora-modularity/meta-test-family/issues) to see if the problem has already been reported.

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/fedora-modularity/meta-test-family/issues/new). Be sure to include a **descriptive title, clear description and a package version** and please include **as many details as possible** to help maintainers reproduce the issue and resolve it faster. If possible, add a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). When you are creating an enhancement issue, **use a clear and descriptive title** and **provide a clear description of the suggested enhancement** in as many details as possible.

### Submitting changes

To submit changes, please send a [GitHub Pull Request](https://github.com/fedora-modularity/meta-test-family/pull/new/devel). Before submitting a PR, please **read the [Styleguides](#styleguides)** to know more about coding conventions used in this project. Also we will appreciate if you **check your code with pylint and pyflakes**. Always **create a new branch for each pull request** to avoid intertwingling different features or fixes on the same branch. Always **do "git pull --rebase" and "git rebase"** vs "git pull" or "git merge".

> **Note:** We are aware of [current syntax and style code errors](https://github.com/fedora-modularity/meta-test-family/issues/21) and working on fixing them.

## Styleguides

### Git Commit Messages

  * Use the present tense ("Add feature" not "Added feature")
  * Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
  * Limit the first line to 72 characters or less

      ```
      $ git commit -m "A brief summary of the commit
      >
      > A paragraph describing what changed and its impact."
      ```

  * Reference issues and pull requests liberally after the first line
  * When only changing documentation, include `[ci skip]` in the commit description
  * Consider ending the commit message with an applicable emoji:
      * :tada: `:tada:` initial commit
      * :bookmark: `:bookmark:` version tag
      * :construction: `:construction:` work in progress (WIP)
      * :package: `:package:` release
      * :art: `:art:` improvement of the format/structure of the code
      * :racehorse: `:racehorse:` performance improvement
      * :hatched_chick: `:hatched_chick:` new feature
      * :book: `:book:` docs update
      * :bug: `:bug:` bugfix
      * :pencil2: `:pencil2:` typo fix
      * :recycle: `:recycle:` remove code or files
      * :green_heart: `:green_heart:` CI build fix
      * :white_check_mark: `:white_check_mark:` add tests
      * :arrow_up: `:arrow_up:` dependencies upgrade
      * :arrow_down: `:arrow_down:` dependencies downgrade
      * :exclamation: `:exclamation:` important

### Codding guidelines

We don't think much of this should be too strange to readers familiar with contributing to Python projects, though it helps if we all get on the same page.

MTF project uses [Landscape tool](https://landscape.io/github/fedora-modularity/meta-test-family/49) to check every commit for errors.

[PEP 8](https://www.python.org/dev/peps/pep-0008/) is a great Python style guide, which we try to follow.

#### Licenses

  * Every file should have a license header, including the copyright of the original author.

#### Python Imports

  * To make it clear what is importing, imports should not be sprinkled throughout the code, but happen at the top of the file.

#### Comments

  * Readability is one of the most important goals for this project
  * Comment any non-trivial code where someone might not know why you are doing something in a particular way
  * Though if something should be commented, that's often a sign someone should write a function
  * All new functions must have a basic docstring comment
  * Commenting above a line is preferable to commenting at the end of a line

#### Whitespace

  * Four space indent is strictly required
  * Include meaningful whitespace between lines of code

#### Variables

  * Use descriptive variable names instead of variables like 'x, y, a, b, foo'
  * MTF python code uses identifiers like 'ClassesLikeThis and variables_like_this

#### Classes

  * It is desirable to see classes in their own files.
  * Classes should generally not cause side effects as soon as they are instantiated, move meaningful behavior to methods rather than constructors.

#### Functions and Methods

  * In general, functions should not be 'too long' and should describe a meaningful amount of work
  * When code gets too nested, that's usually the sign the loop body could benefit from being a function
  * Parts of our existing code are not the best examples of this at times.
  * Functions should have names that describe what they do, along with docstrings
  * Functions should be named with_underscores
  * "Don't repeat yourself" is generally a good philosophy

#### Exceptions

  * In the main body of the code, use typed exceptions where possible:

      ```
      # not this
      raise Exception("panic!")

      # this
      from moduleframework.exceptions import SomeTypedException
      ...
      raise SomeTypedException("panic!")
      ```

  * Similarly, exception checking should be fine grained:

      ```
      # not this
      try:
         foo()
      except:
         bar()

      # but this
      try:
         foo()
      except SomeTypedException:
         bar()
      ```

## Questions?

* Ask any question about how to use MTF in the [#fedora-modularity](https://webchat.freenode.net/?channels=fedora-modularity) chat channel on freenode IRC.

Thank you! :heart: :heart: :heart:

MTF Team
