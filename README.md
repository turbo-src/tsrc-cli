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

```

### Config

It's the same config found in algorand, except the port is mapped to `4190` (verify on turbo-src/docker-compose.yml).
tsrc-cli is ran from host and isn't part of the overall systems docker network.

`cp algorand/algorand/tests/e2e/test-config.json tsrc-cli/tests/e2e/test-config.json`

And change the port number from 8080 -> 4190.

### tests

```
python tests/e2e/e2e.py
```

Run from host in tsrc-cli project root directory, not turbo-src.
