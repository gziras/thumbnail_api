Requirements definition

The idea is that we want a web application that will allow a user to search and get a thumbnail of an image
that has been retrieved from Unsplash. In particular our web application should expose a REST API
endpoint that will allow a user to specify a search term of the desired photo to be found at Unsplash.
Optional arguments, can be the preferred orientation of the photo or the color based on which photos will
be filtered out. Only one photo should be picked ( randomly ) and then create the appropriate thumbnail.
After thumbnail generation is finished, the request user should be given a unique link that can be used to
view the thumbnail.

Constraints
- Don’t use any thumbnail functionality already offered by Unsplash.

Implementation should be in Python. A free account at Unsplash is required in order to use it’s API.
Deliverables
- A single compressed file containing the .git repository
- We should be able to verify the functionality using docker-compose