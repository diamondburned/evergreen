# py-svelte-template

A full-stack web application template with Python FastAPI, Svelte, SQLite
database, session handling and integration testing.

## Features

- Uses [SvelteKit](https://kit.svelte.dev/) for the frontend
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the API
- Uses [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- Uses [SQLModel](https://sqlmodel.tiangolo.com/) for database models and
  migrations
- Uses [SQLite](https://www.sqlite.org/index.html) for the database
- Prioritizes asynchronous code for better performance (with `aiosqlite`)
- Contains a basic user authentication system with login and registration
  - Includes password hashing with PBKDF2 using `hashlib`
- Contains [hurl](https://hurl.dev) tests for the API (in `tests/`)

## Usage

It is recommended to use Nix with Flakes for development. If you have Nix
installed, you can simply run `nix develop` to enter a development environment
with all the necessary dependencies.

Once you have the development environment set up, you can run the following
commands:

```sh
foreman start
```

## License

This project is licensed under the terms of the ISC license. See the
[LICENSE](LICENSE) file for details.
