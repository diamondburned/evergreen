# Pixiecode

TBD

## Usage

It is recommended to use Nix with Flakes for development. If you have Nix
installed, you can simply run `nix develop` to enter a development environment
with all the necessary dependencies.

If you don't have Nix available, then you'll need to manually get these
dependencies:

- Python
- NodeJS
- [Foreman](https://theforeman.org/)
- [Poetry](https://python-poetry.org/)

Then run `poetry shell` to enter the Python development environment. Again,
`nix develop` automatically does this for you.

Once you have the development environment set up, you can run the following
commands:

```sh
npm install    # install frontend dependencies
foreman start  # start the development server
```
