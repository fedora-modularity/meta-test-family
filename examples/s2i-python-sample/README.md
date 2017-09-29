# Source to image example

Contains example how to use `S2I` image testing.

## How to run

 - install (package) prerequisities (source-to-image, curl): `sudo mtf-env-set`
 - run it via Makefile: `sudo make`
 - run test manually: `mtf *.py`
 - or dicrectly via avocado: `avocado run *.py`

## How it works

 - creation of s2i image is based on `config.yaml` file, it contains installation of tools and using `s2i` command for image creation.
 - it contains `default_module` section set to `docker`, so you don't need to set `MODULE=docker` envvar
 - you can redefine start method of config if you would like to pass another port

### Using inheritance of modules
 - It is possible to test more than just one version of s2i container with inheritance.
 - In `config.yaml`, you can define `parent` set to `docker` and then you can define more docker modules and use them via envvar definition `MODULE=your_docker_module`
