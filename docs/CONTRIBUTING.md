# Contributing to the River Architect Wiki
We'd love for you to contribute to our source code and to make River Architect even better than it is
today. Here are the guidelines we'd like you to follow:

* [Coding Conventions](#conv)
* [Code of Conduct](#coc)
* [Questions and Problems](#question)
* [Issues and Bugs](#issue)
* [Feature Requests](#feature)
* [Improving Documentation](#docs)
* [Issue Submission Guidelines](#submit)
* [Pull Request Submission Guidelines](#submit-pr)
* [Signing the CLA](#cla)

## <a name="conv"></a> Coding Conventions
*River Architect* code styles follow the [PEP 8 style conventions](https://www.python.org/dev/peps/pep-0008/). In brief, that means:

 - Beautiful is better than ugly.
 - Explicit is better than implicit.
 - Simple is better than complex.
 - Complex is better than complicated.
 - Flat is better than nested.
 - Sparse is better than dense.
 - Readability counts.
 - Special cases are not special enough to break the rules.
 - Practicality beats purity.
 - **Errors should never pass silently**.
 - Unless explicitly silenced.
 - In the face of ambiguity, there should be one - and preferably only one - obvious way to program.
 - If the implementation is hard to explain, it is a bad idea.
 - If the implementation is easy to explain, it may be a good idea.
 - Use namespaces.

## <a name="coc"></a> Code of Conduct

Help us keep River Architect open and inclusive.

## <a name="requests"></a> Questions, Bugs, Features

### <a name="question"></a> Got a Question or Problem?

Do not open issues for general support questions as we want to keep GitHub issues for bug reports
and feature requests. You have got much better chances of getting your question answered on dedicated
support platforms, the best being [Stack Overflow](https://stackoverflow.com/):

- there are thousands of people willing to help on Stack Overflow
- questions and answers stay available for public viewing so your question / answer might help
  someone else
- Stack Overflow's voting system assures that the best answers are prominently visible.

To save your and our time, we will systematically close all issues that are requests for general
support and redirect people to the section you are reading right now.


### <a name="issue"></a> Found an Issue or Bug?

If you find a bug in the source code, you can help us by submitting an issue to our
[GitHub Repository][github]. Even better, you can submit a Pull Request with a fix.

**Please see the [Submission Guidelines](#submit) below.**


### <a name="feature"></a> Missing a Feature?

You can request a new feature by submitting an issue to our [GitHub Repository][github-issues].

If you would like to implement a new feature then consider what kind of change it is:

* **Major Changes** that you wish to contribute to the project should be discussed first in an
  [GitHub issue][github-issues] that clearly outlines the changes and benefits of the feature.
* **Small Changes** can directly be crafted and submitted to the [GitHub Repository][github]
  as a Pull Request. See the section about [Pull Request Submission Guidelines](#submit-pr), and
  for detailed information the [core development documentation][developers].

### <a name="docs"></a> Want a Doc Fix?

Should you have a suggestion for the documentation, you can open an issue and outline the problem
or improvement you have, or creating the doc fix yourself.

If you want to help improve the docs, it's a good idea to let others know what you're working on to
minimize duplication of effort. Create a new issue (or comment on a related existing one) to let
others know what you're working on.

If you're making a small change (typo, phrasing) don't worry about filing an issue first. Use the
friendly blue "Improve this doc" button at the top right of the doc page to fork the repository
in-place and make a quick change on the fly. The commit message is preformatted to the right type
and scope, so you only have to add the description.

For large fixes, please build and test the code before submitting to be sure you
haven't accidentally introduced any issues. You should also make sure that your
commit message follows the **[Commit Message Guidelines][developers.commits]**.

## <a name="submit"></a> Issue Submission Guidelines
Before you submit your issue search the archive, maybe your question was already answered.

If your issue appears to be a bug, and hasn't been reported, open a new issue. Help us to maximize
the effort we can spend fixing issues and adding new features, by not reporting duplicate issues.

The "[new issue][github-new-issue]" form contains a number of prompts that you should fill out to
make it easier to understand and categorize the issue.

In general, providing the following information will increase the chances of your issue being dealt
with quickly:

* **Overview of the Issue** - if an error is being thrown a non-minified stack trace helps
* **Motivation for or Use Case** - explain why this is a bug for you
* **Browsers and Operating System** - is this a problem with all browsers or only specific ones?
* **Reproduce the Error** - provide a live example or an unambiguous set of steps.
* **Related Issues** - has a similar issue been reported before?
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point to what might be
  causing the problem (line of code or commit)


## <a name="submit-pr"></a> Pull Request Submission Guidelines
Before you submit your pull request consider the following guidelines:

* Search [GitHub](https://github.com/sschwindt/RiverArchitect/pulls) for an open or closed Pull Request
  that relates to your submission. You don't want to duplicate effort.
* Create the [development environment][developers.setup]
* Make your changes in a new git branch:

    ```shell
    git checkout -b my-fix-branch master
    ```

* Create your patch commit, **including appropriate test cases**.
* Follow our [Coding Rules][developers.rules].
* Commit your changes using a descriptive commit message that follows our
  [commit message conventions][developers.commits]. Adherence to the
  [commit message conventions][developers.commits] is required, because release notes are
  automatically generated from these messages.

    ```shell
    git commit -a
    ```
  Note: the optional commit `-a` command line option will automatically "add" and "rm" edited files.

* Before creating the Pull Request, package and run all tests a last time:

    ```shell
    ... test
    ```

* Push your branch to GitHub:

    ```shell
    git push origin my-fix-branch
    ```

* In GitHub, send a pull request to `RiverArchtiect:master`. This will trigger the check of the
[Contributor License Agreement](#cla) and the Travis integration.


* If we suggest changes, then:

  * Make the required updates.
  * Re-run River Architect to ensure that it is still working.
  * Commit your changes to your branch (e.g. `my-fix-branch`).
  * Push the changes to your GitHub repository (this will update your Pull Request).

    You can also amend the initial commits and force push them to the branch.

    ```shell
    git rebase master -i
    git push origin my-fix-branch -f
    ```

    This is generally easier to follow, but seperate commits are useful if the Pull Request contains
    iterations that might be interesting to see side-by-side.

That's it! Thank you for your contribution!

#### After your pull request is merged

After your pull request is merged, you can safely delete your branch and pull the changes
from the main (upstream) repository:

* Delete the remote branch on GitHub either through the GitHub web UI or your local shell as follows:

    ```shell
    git push origin --delete my-fix-branch
    ```

* Check out the master branch:

    ```shell
    git checkout master -f
    ```

* Delete the local branch:

    ```shell
    git branch -D my-fix-branch
    ```

* Update your master with the latest upstream version:

    ```shell
    git pull --ff upstream master
    ```

## <a name="cla"></a> Signing the Contributor License Agreement (CLA)

Upon submmitting a Pull Request, a friendly bot will ask you to sign our CLA if you haven't done
so before. Unfortunately, this is necessary for documentation changes, too.
