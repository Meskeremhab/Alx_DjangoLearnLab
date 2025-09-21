Auth & Permissions:
- TokenAuth + Session/Basic enabled in REST_FRAMEWORK.
- Obtain a token via POST /api/token/ with username/password.
- Default permission IsAuthenticatedOrReadOnly: anonymous can GET, authenticated can POST/PUT/PATCH/DELETE.
- BookViewSet explicitly sets permission_classes and authentication_classes.
