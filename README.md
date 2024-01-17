# tsrc-cli


### Install

Clone.

```
git clone --recurse-submodules https://github.com/turbo-src/turbo-src.git
```

In the `turbo-src/tsrc-cli` directory.

```
poetry install
```

Initialize and start turbosrc in the `turbo-src` root directory per `turbo-src/README.md`.

### Commands

Create user

```
poetry run tsrc-cli create-user <contributor-id> <contributor-name> <contributor-signature> <github-token>
```

### tests

```
pytest
```