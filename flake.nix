{
  description = "Python client for Coin Metrics API v4";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    nixpkgs = {
      url = "github:NixOS/nixpkgs";
    };
  };

  outputs = { self, flake-utils, nixpkgs }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };

      lib = import ./.;
    in {
      packages = {
        coinmetrics-api-client-py310 = pkgs.python310Packages.callPackage lib {};
        coinmetrics-api-client-py311 = pkgs.python311Packages.callPackage lib {};
        coinmetrics-api-client-py312 = pkgs.python312Packages.callPackage lib {};
      };
    }
  );
}
