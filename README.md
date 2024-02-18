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
poetry install --no-root  # install backend dependencies
npm install               # install frontend dependencies
foreman start             # start the development server
```

## Adding the Unity build

In order for the game to fully be functional, you need to add the Unity WebGL build into the project.

1. Build the Unity project to WebGL. This will create a `Build` directory in
   the Unity project.
2. Copy the contents of the `Build` directory into the `frontend/game` directory.
   You should be copying `.br` and `.js` files.
3. Start up the server as usual.
