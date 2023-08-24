{ pkgs ? import <nixpkgs> {} }:
with pkgs;
mkShell rec {
  name = "sd-env";
  LD_LIBRARY_PATH = lib.makeLibraryPath [ gcc-unwrapped zlib libglvnd glib linuxPackages.nvidia_x11 ];
  buildInputs = [ python39 python39Packages.pip git go ];
}
