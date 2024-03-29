{
	inputs = {
		flake-utils.url = "github:numtide/flake-utils";
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
		poetry2nix = {
			url = "github:nix-community/poetry2nix";
			inputs.nixpkgs.follows = "nixpkgs";
		};
	};

	outputs =
		{
			self,
			nixpkgs,
			poetry2nix,
			flake-utils,
		}:

		flake-utils.lib.eachDefaultSystem (system:
			let
				pkgs = nixpkgs.legacyPackages.${system};
				inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
					mkPoetryApplication
					overrides;
			in
			{
				packages.default = mkPoetryApplication {
					projectDir = self;
					overrides = overrides.withDefaults (self: super: let
						fixPoetryPackage = pkg: pkg.overridePythonAttrs (old: {
							buildInputs = (old.buildInputs or [ ]) ++ (with super; [
								setuptools
								poetry
								pdm-pep517
								pdm-backend
								truststore
							]);
						});
						useWheel = pkg: pkg.override { preferWheel = true; };
					in
						{
							asyncio = fixPoetryPackage super.asyncio;
							sonyflake-py = fixPoetryPackage super.sonyflake-py;
							sse-starlette = fixPoetryPackage super.sse-starlette;
							sphinxcontrib-jquery = super.sphinxcontrib-jquery.overridePythonAttrs (old: {
								buildInputs = (old.buildInputs or [ ]) ++ (with super; [
									sphinx
								]);
							});
							numpy = useWheel super.numpy;
							scipy = useWheel super.scipy;
							pandas = useWheel super.pandas;
							scikit-learn = useWheel super.scikit-learn;
						}
					);
				};

				devShell = pkgs.mkShell {
					inputsFrom = [ self.packages.${system}.default ];

					packages = with pkgs; [
						nodejs
						poetry
						hurl
						foreman
					];

					shellHook = ''
						export PATH="$PATH:$(git rev-parse --show-toplevel)/node_modules/.bin"
					'';
				};
			}
		);
}
