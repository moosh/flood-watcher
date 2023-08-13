Running the open=elevation Server

Run from the open-elevation directory:

docker run -t -i -v $(pwd)/data:/code/data -p 80:8080 openelevation/open-elevation

This command:

    Maps $(pwd)/data (your data directory) to /code/data within the container
    Exposes port 80 to forward to the container's port 8080
    Runs the default command, which is the server at port 8080

You should now be able to go to http://localhost for all your open-route needs.


In general:

docker run -t -i -v $(pwd)/data:/code/data -p 80:8080 openelevation/open-elevation <your command here>
