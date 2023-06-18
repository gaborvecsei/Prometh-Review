# Prometh Review - AI Pull-Request Reviewer Companion

_Unveil the extraordinary power of Prometh-Review, an AI-driven companion that kindles the flames
of pull request enlightenment, empowering developers to ascend to new heights of collaborative mastery._

With `Prometh Review` you can get instant feedback on any pull-request:

- bugs
- security issues
- missed best practices
- general feedback

You can also start an interactive session and talk with the AI about the changes in the pull request

> _Warning_: Proof of concept tool and right now only works with Bitbucket/Stash

# Setup

## Required Tools

`git`, `python3` and `pip3` is required. The required packages are in the `requirements.txt`.

## Install

```
$ pip3 install git+https://github.com/gaborvecsei/Prometh-Review.git
```

Or `Docker` can be used

```shell
docker built -t prometh .
```

## Environment variables

You'll need some environment variables depending on how you'd like to run the tool

### OpenAI

Required to use the OpenAI GPT LLM family

```
export OPENAI_API_KEY=<YOUR_TOKEN>
```

### Stash/Bitbucket

Required if you have the repo on Stash/Bitbucket

```
export STASH_HTTP_ACCESS_TOKEN=<YOUR_TOKEN>
```

### GitHub

TODO

### GitLab

TODO

# Usage

- On your machine **go to the folder of the repository**. Update the refs. You can use the script only from there
  - (_Why?_ It works from the local `git diff`, I really don't want to parse Github/Bitbucket API diff responses...)
- Get the necessary parameters from Github/Stash/Bitbucket (check the help for these). These are the most important ones:
  - Project Name (e.g.: AI)
  - Repo slug (simplified name of the repository) (e.g.: churn-prediction)
  - Pull request ID (e.g.: 85)

```
$ prometh --help
```

```
$ docker run -it -e OPENAI_API_KEY="TODO" [other required env vars] prometh prometh -h
```

There are 2 modes for the LLMs:
- **OpenAI** based
    - You only need to include the OpenAI Token and you are ready to go
- **Local/On-prem** deployment based with [`LocalAI`](https://github.com/go-skynet/LocalAI)
    - You'll need to deploy a LLM (no GPUs required) by following the *how-to* in the repo above
    - Once you have a deployment, confirm it with `curl http://localhost:8080/v1/models`
    - In the CLI use the model name you've deployed, e.g.: `prometh --llm-type my_deployed_model ...` 

## Defaults

You can set default values for some of the not commonly used parameters (e.g.: base-url) with the `.promethrc.json` file.

The localtion of the file should be in your home `~/.promethrc.json`.

See the example included in the repo (`.promethrc.json.example`).

## Example

```
$ prometh -p ai -r churn-prediction -id 85 -c 10 -i
```

> (AI Stash project, churn-prediction repository, pull request with the id 85)

# FAQ

**What to do if the script fails with some token count error?**

This means that you have a big diff 😏 and the GPT model cannot handle it because of the context limitation.

What to do? First let's try to reduce the `--nb-context-lines`, but if this is not enough, then I would go file by file
what can be done with the file filter `-x`.

**How much does this cost with OpenAI 💰?**

You can do a calculation here [https://gpt-calculator.gaborvecsei.com/](https://gpt-calculator.gaborvecsei.com/)

A single PR-Review (without the interactive session) (with the `gpt-3.5-turbo-16k`) should not cost more than _$0.05_.

# Todo

Some ideas what needs to be done in order to have a tool which is fun to use

- [ ] Support GitHub
- [ ] Support Manual mode
- [ ] Error handling (as right now there is `None`)
- [ ] Make the output more pretty with `rich`
- [ ] More consistent output format from GPT
- [ ] More control on what to check in the PRs
  - [ ] Check single files only
  - [ ] Include, exclude file trypes (e.g.: Jupyter-Notebooks)
- [ ] When the diff too big, do some smart truncation, or file-by-file analyzis
- [ ] Check token count before sending the request to OpenAI
- [ ] Allow other LLMs other than OpenAI GPT family (e.g.: locally deployed models)

---

Made with ❤️❤️❤️
