# compiler sanity smoke test for the Base Runtime docker image

The internal workings of this test are as follows:

1. Create a temporary directory.
2. Copy the `hello.sh` script from this resource directory into the temporary directory and make sure it is executable.
3. Place a gzipped tarball of `hello.c` and `Makefile` from this resource directory into the temporary directory with the name `hello.tgz`.
   e.g.,  
   `$ tar czf /tmp/random/hello.tgz hello.c Makefile`
4. Run the docker container binding the temporary directory as `/mnt` and run `/mnt/hello.sh`.  
   e.g.,  
   `$ docker run -v /tmp/random:/mnt:z --rm base-runtime /bin/bash -c /mnt/hello.sh`
5. Clean up the temporary directory upon completion.


