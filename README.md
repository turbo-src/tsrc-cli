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

Add a `config/config.json`. Also a `tests/e2e/test-config.json`. They are identical (should be collapsed to one though)

It's the same config found in algorand, except the port is mapped to `4190` (verify on turbo-src/docker-compose.yml).
tsrc-cli is ran from host and isn't part of the overall systems docker network.

`cp algorand/algorand/tests/e2e/test-config.json tsrc-cli/tests/e2e/test-config.json`
`cp algorand/algorand/tests/e2e/test-config.json tsrc-cli/config/config.json`

And change the port number from 8080 -> 4190.

### algorand program (holdover)

Copy the algorand program binaries `tsrc-cli` project root directory from your algorand container

```
vote_approval.teal.tok
vote_clear_state.teal.tok
```

tsrc-cli in the future should just compile these using the python sdk.

### tests

```
python tests/e2e/e2e.py
```

Run from host in tsrc-cli project root directory, not turbo-src.
