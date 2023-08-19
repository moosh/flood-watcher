# Running notes

* Run the `open-elevation` server from the open-elevation directory:

        docker run -t -i -v $(pwd)/data:/code/data -p 80:8080 openelevation/ open-elevation


* In general:

        docker run -t -i -v $(pwd)/data:/code/data -p 80:8080 openelevation/open-elevation <your command here>


* The problem with running this docker container was due to the image data not being located properly after unrar'ing. Because of this no tiles were generated and the server struggled on every request to load the full 5-8GB file. All tiles should be at the ./data level, NOT in a subdirectory. Also, it's important for performance that the unrar'ed images are tiled.

* The Madison LIDAR tiles downloaded from https://geodata.wisc.edu/catalog/d7cd592c-bc97-4e16-ac0f-22913e408056 don't appear to contain any data. The TIFF tiles all seem to be 100% white data.