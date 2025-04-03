{ inputs, lib, ... }: {
  perSystem =
    { config
    , self'
    , inputs'
    , system
    , pkgs
    , final
    , ...
    }:
    let
      python = pkgs.python311;

      workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../../.; };
      overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };
      baseSet = pkgs.callPackage inputs.pyproject-nix.build.packages { inherit python; };

      # Overrides for the pyproject.nix package set
      pyprojectOverrides = final: prev: {
        fluree-py = prev.fluree-py.overrideAttrs (old: {

          passthru = old.passthru // {
            tests =
              let
                # Construct a virtual environment with only the test dependency-group enabled for testing.
                virtualenv = final.mkVirtualEnv "fluree-py-pytest-env" {
                  fluree-py = [ "dev" ];
                };
              in
              (old.tests or { })
                // {
                pytest = pkgs.stdenv.mkDerivation {
                  name = "${final.fluree-py.name}-pytest";
                  inherit (final.fluree-py) src;
                  nativeBuildInputs = [
                    virtualenv
                  ];
                  dontConfigure = true;

                  # Because this package is running tests, and not actually building the main package
                  # the build phase is running the tests.
                  buildPhase = ''
                    runHook preBuild
                    pytest --cov tests --cov-report html
                    runHook postBuild
                  '';

                  # Install the HTML coverage report into the build output..
                  installPhase = ''
                    runHook preInstall
                    mv htmlcov $out
                    runHook postInstall
                  '';
                };
              };
          };
        });
      };

      pythonSet = baseSet.overrideScope
        (
          lib.composeManyExtensions [
            inputs.pyproject-build-systems.overlays.default
            overlay
            pyprojectOverrides
          ]
        );
    in
    {
      checks = pythonSet.fluree-py.passthru.tests;
      packages.default = pythonSet.mkVirtualEnv "fluree-py-env" workspace.deps.default;

      devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
            pkgs.ruff
          ];
          env =
            {
              # Prevent uv from managing Python downloads
              UV_PYTHON_DOWNLOADS = "never";
              # Force uv to use nixpkgs Python interpreter
              UV_PYTHON = python.interpreter;
            }
            // lib.optionalAttrs pkgs.stdenv.isLinux {
              # Python libraries often load native shared objects using dlopen(3).
              # Setting LD_LIBRARY_PATH makes the dynamic library loader aware of libraries without using RPATH for lookup.
              # LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
            }; 
          shellHook = ''
            unset PYTHONPATH
          '';
        };
    };
}
