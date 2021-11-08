
Permissions API - A DRF API to showcase use of custom permissions and roles
=======

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

### Users (for authentication)

```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "bio": "I work at statefarm",
    "image": null
  }
}
```
### Profile
```source-json
{
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false
  }
}
```
### Single note
```source-json
{
    "note": {
        "id": 2,
        "author": {
            "id": 1,
            "email": "danielmutuba12it@gmail.com",
            "username": "DanielMutuba12",
            "role": "admin"
        },
        "body": "string",
        "tagList": [
            "string"
        ],
        "created_at_date": "2021-11-08T05:20:56.690973+00:00",
        "description": "string",
        "slug": "string-2",
        "title": "string",
        "updated_at_date": "2021-11-08T05:31:37.780620+00:00",
        "like": 0,
        "dislike": 0
    }
}
```
### Multiple Notes
```source-json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "author": {
                "id": 1,
                "email": "danielmutuba12it@gmail.com",
                "username": "DanielMutuba12",
                "role": "admin"
            },
            "body": "string",
            "tagList": [
                "string"
            ],
            "created_at_date": "2021-11-08T05:20:56.690973+00:00",
            "description": "string",
            "slug": "string-2",
            "title": "string",
            "updated_at_date": "2021-11-08T05:31:37.780620+00:00",
            "like": 0,
            "dislike": 0
        },
        {
            "id": 1,
            "author": {
                "id": 1,
                "email": "danielmutuba12it@gmail.com",
                "username": "DanielMutuba12",
                "role": "admin"
            },
            "body": "string",
            "tagList": [
                "string"
            ],
            "created_at_date": "2021-11-08T05:16:33.565813+00:00",
            "description": "string",
            "slug": "string",
            "title": "string",
            "updated_at_date": "2021-11-08T05:16:33.565843+00:00",
            "like": 0,
            "dislike": 0
        }
    ]
}
```

### Errors and Status Codes
If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "body": [
      "can't be empty"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request


Endpoints:
----------

### Authentication:

`POST /api/users/login`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /api/users/signup`

Example request body:

```source-json
{
  "user":{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `username`, `password`

### Create a role

`POST /api/roles`

Authentication required, and current user must have a permission to create roles

### Update User

`POST /api/roles`

Example request body:

```source-json
{
  "name": "string",
  "permissions": [
    "string"
  ]
}
```

Authentication required, returns a Role

Accepted fields: `email`, `username`, `password`, `image`, `bio`



### Update available role

`POST /api/roles/{id}/update`

Authentication required, and current user must have a permission to create roles

### Update User

`POST /api/roles/{id}/update`

Example request body:

```source-json
{
  "name": "string"
}
```

### List available roles

`POST /roles/list/`

Authentication required, and current user must have a permission to create roles

### Update User

`POST /api/roles/list`

Example response body:

```source-json
{
  "id": 0,
  "name": "string",
  "permissions": [
    {
      "id": 0,
      "name": "string",
      "role": "string"
    }
  ]
}
```


### Create a permission

`POST /api/roles/{id}`

Example response body:

```source-json
{
  "name": [
    "string"
  ]
}
```
Takes a list of permissions as an array. It needs a role id.



### Create a user with a role (assign)

`POST /api/admin/users/create`

Example response body:

```source-json
{
  "email": "user@example.com",
  "username": "string",
  "password": "string",
  "role": "string"
}
```
The request requires a user to have permissios to create a user. 



### Update user details

`POST /api/admin/users/{id}/update`

Example response body:

```source-json
{
  "email": "user@example.com",
  "username": "string",
  "password": "string",
  "role": "string"
}
```
The request requires a user to have permissios to create a user.


### List Notes

`GET /api/notes/list/`

Returns most recent notes globally by default, provide `tag`, `author` or `favorited` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of notes (default is 20):

`?limit=20`

Offset/skip number of notes (default is 0):

`?offset=0`


### Get Article

`GET /api/notes/:id`

No authentication required, will return single article

### Create Note

`POST /api/notes`

Example request body:

```source-json
{
  "body": "string",
  "tagList": [
    "string"
  ],
  "description": "string",
  "slug": "string",
  "title": "string"
}
```

Authentication required, will return note

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Note

`PUT /api/notes/:id`

Example request body:

```source-json
{
  "body": "string",
  "tagList": [
    "string"
  ],
  "description": "string",
  "slug": "string",
  "title": "string"
}
```

Authentication required, returns the Note

Optional fields: `title`, `description`, `body`

The `id` also gets updated when the `title` is changed

### Delete Note

`DELETE /api/notes/:id`

Authentication required

```



