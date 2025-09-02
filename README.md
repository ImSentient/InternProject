# InternProject

This project is a Django REST API with a PostgreSQL database, fully containerized using Docker Compose.

## Prerequisites

- Docker  
- Docker Compose  

If Docker is not installed, follow these steps:

### Install Docker
if you haven't installed Docker already, follow their official documentation for your platform here: https://docs.docker.com/engine/



## Docker Setup
Download the repository by running :

```
git clone https://github.com/ImSentient/InternProject.git
```

Then, navigate to the repository and run


```
 docker compose up --build

```


If the docker container pass their health checks (as they should), then you'll now have a local API which you can interact with through http://127.0.0.1:8000/api/

## Design Considerations

- Uses docker containers to isolate both an instance of Django and of PostgreSQL (which has a persistant volume).
- Uses a Docker entrypoint script to auto-migrate Models to DB on build. 
- The Django API is accessible through 127.0.0.1 port 8000, and the PostgreSQL is accessible through port 5432. 
- Transition logic handled in views.py of the api app.
- That's all the major bulletpoints i can think of.

## API Examples
### Server Creation


When a server is inserted and no devices are online (or exist), then status is set to 'error'
```js
POST /api/servers/
{
  "name": "Greg's Server"
}

GET /api/servers/
[
    {
        "id": 1,
        "name": "Greg's Server",
        "subdomain": "gregs-server",
        "status": "error",
        "created_at": "2025-09-02T02:25:52.066513Z",
        "device": None,
    }
]
```
---
### Device Creation

Inserting a new device into the server is extremely easy, as shown below. The example alos shows that when a new server is inserted, it'll be assigned any online device available.
```js
POST /api/devices/
{
  'name': 'victors device', 
  'is_online': true
}

POST /api/servers/
{
  "name": "Greg's Server"
}

GET /api/servers/
[
    {
        "id": 1,
        "name": "Greg's Server",
        "subdomain": "gregs-server",
        "status": "error",
        "created_at": "2025-09-02T02:25:52.066513Z",
        "device": None,
    },
    {
        "id": 2,
        "name": "Greg's Server",
        "subdomain": "gregs-server-2",
        "status": "running",
        "created_at": "2025-09-02T02:25:52.203371Z",
        "device": {
            "id": 1,
            "name": "victors device",
            "is_online": True,
            "last_seen": "2025-09-02T02:25:52.208732Z",
        },
    },
]
```
---
### Changing Server Status
If you happen to have a server which is stuck in an error status, no worries! Send a patch request to the API endpoint of the specific server and it'll acquire an online device as well, assuming there are any availabe.
```js
PATCH /api/servers/1/
{
  'status': 'starting'
}

GET /api/servers/
[
    {
        "id": 2,
        "name": "Greg's Server",
        "subdomain": "gregs-server-2",
        "status": "running",
        "created_at": "2025-09-02T02:25:52.203371Z",
        "device": {
            "id": 1,
            "name": "victors device",
            "is_online": True,
            "last_seen": "2025-09-02T02:25:52.304372Z",
        },
    },
    {
        "id": 1,
        "name": "Greg's Server",
        "subdomain": "gregs-server",
        "status": "running",
        "created_at": "2025-09-02T02:25:52.066513Z",
        "device": {
            "id": 1,
            "name": "victors device",
            "is_online": True,
            "last_seen": "2025-09-02T02:25:52.304372Z",
        },
    },
]
```
---