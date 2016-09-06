# NV print queue manager

NVqueue implements a basic FIFO queuing service for print jobs. It supports
multiple queues. 

In addition to basic add / view / list / delete operations for the queues and jobs,
it supports a 'take job' operation that is safe with multiple concurrent requests.

## Installation and test

Tested on OSX 10.10.5 and Ubuntu 16.04.1 using Chrome 51.0.2704.103.

_Creating a new virtual environment is recommended._

    cd /tmp  # (or some other writable directory)
    
    git clone https://github.com/koikoikoi/nvqueue.git
    cd nvqueue
    
    pip install -r requirements.txt
    ./manage.py makemigrations nvqueue
    python manage.py migrate --noinput
    
    # create a superuser if you want to use the Django admin tool at http://localhost:8000/admin/
    # python manage.py createsuperuser 
    
    python manage.py runserver

If running server as documented above, prefix endpoints URLs with `http://127.0.0.1:8000/`.
  
## Notes
API users are not authenticated. All operations are available to any requestor.

## Usage
Test the API from another terminal (using curl, httpie, etc.) or a web browser. For example to list the queues:

    curl http://localhost:8000/queues/ | python -m json.tool

    http  http://localhost:8000/queues/  # using httpie

Note that no queues have been created at this point so the results of this query will be empty.
See below for how to create queues and print jobs.

An easy way to explore the API is to visit  [http://localhost:8000/](http://localhost:8000/) with a browser. All resources are hyperlinked so 
navigating is not hard. You can also create queues and print jobs.


## Test

You can also test the installation by running the included simple test that creates a queue and verifies that it 
is added to the database and is returned with a GET request.

`python manage.py test`

## Example

All examples use the httpie command line tool.

**Create a new print queue:**

    http post http://localhost:8000/queues/ name='NVPro 1'
    
**Example Response:**

```
{
    "created": "2016-09-06T02:54:45.406474Z", 
    "id": 1, 
    "name": "NVPro 1", 
    "printjobs": [], 
    "url": "http://localhost:8000/queues/1/"
}
```

You can now view the updated list of queues at [http://localhost:8000/queues/](http://localhost:8000/queues/).

If you try to create another queue with the same name you should get this response:

```
{
    "name": [
        "queue with this name already exists."
    ]
}
```


**Add a print job to the new queue:**

     http post http://localhost:8000/printjobs/ user='me' filename='foo.text' queue='http://localhost:8000/queues/1/'
    
**Example Response:**
     
<pre>
{
    "created": "2016-09-06T14:37:38.637047Z", 
    "filename": "foo.text", 
    "id": 1, 
    "printer": "", 
    "queue": "http://localhost:8000/queues/1/", 
    "state": "waiting", 
    "url": "http://localhost:8000/printjobs/3/", 
    "user": "me"
}
</pre>


**Fetch the next job by a print service:**

In this example it is assumed that the service has the queue name and must look up the corresponding queue id to take the next job. 

Get queue ID by name:

    http get http://localhost:8000/queues/queue_by_name/?name='NVPro 1'

<pre>
{
    "id": 1, 
    "name": "NVPro 1", 
    "url": "http://localhost:8000/queues/1/"
}
</pre>

Get next available job if any:

http post http://localhost:8000/queues/1/take_job/ printer='NVpro 1'

<pre>
{
    "filename": "file.txt", 
    "id": 1, 
    "name": "", 
    "printer": "NVpro 1", 
    "queue": 1, 
    "state": "printing", 
    "user": "me"
}
</pre>

If there are no available jobs:

HTTP 404

<pre>
{
    "detail": "no more jobs."
}
</pre>


## API endpoints

### Overview

| Endpoint           |Method  | Description                 |params              | Return Statuses    |
|--------------------|--------|-----------------------------|--------------------|--------------------|
| /                  |`GET`   | Returns base endpoints      |                    | 200                |
| /queues/           |`GET`   | View queues                 |                    | 200                |
|                    |`POST`  | Add queue                   | name               | 201, 400           |
| /queues/queue_by_name/|`GET`| Get queue by name           | name               | 200, 404           |
| /queues/_q_id_/    |`GET`   | View queue                  | name               | 200, 201, 404      |
|                    |`PUT`   | Update queue                | name               | 200, 201, 404      |
|                    |`DELETE`| Delete queue                |                    | 200, 201, 404      |
| /queues/_q_id_/take_job/|`POST`| Take job (for printers)  | printer name       | 202, 404           |
| /printjobs/        |`GET`   | View print jobs             |                    | 200                |
|                    |`POST`  | Create print job            | filename           | 201, 400           |
|                    |        |  - could also be impl. on queues|                 |                    |
| /printjobs/_id_    |`GET`   | View print job              |                    | 200, 404           |
|                    |`PUT`   | Update print job            | filename           | 200, 404           |
|                    |`DELETE`| Delete job                  |                    | 200, 404           |

Note: In all cases. _HTTP 405 Method not allowed_ is possible.


### API Details

Sample result output is provided for some endpoints.

---
#### Root API Endpoint

Returns API endpoints for queues and print jobs.

**URL:** /

**Methods:** `GET`

**URL Params:** None 

**Data Params:** None 

**Response:** 

200 OK

<pre>
{
    "printjobs": "http://localhost:8000/printjobs/", 
    "queues": "http://localhost:8000/queues/"
}
</pre>

---
#### Queues

  View and add print queues.

**URL:**

  /queues/
  
  /queues/queue_by_name/  # convenience function to find queue by queue name

**Methods**
  
`GET` | `POST`
  
**URL Params**

Required for queue_by_name: `name`

**Success Responses**
 
`GET http://localhost:8000/queues/queue_by_name/?name='NVPro 1'` 
  
Code: 200 OK
  
<pre>
    [
     {
        "id": 1,
        "created": "2016-11-03T20:33:46.200017Z",
        "name": "Queue One"
     },
     {
        "id": 2,
        "created": "2016-11-03T20:47:44.883442Z",
        "name": "Queue Two"
     }
    ]
</pre>

`GET queue_by_name`

Code: 200 OK
  
<pre>
{
    "id": 7, 
    "name": "NVPro 1"
}
</pre>

`POST`

Code: HTTP 201 Created
     
<pre>
    {
        "id": 3,
        "created": "2016-11-04T22:07:44.663632Z",
        "name": "Queue Three",
        "printjobs": []
    }
</pre>
        
**Error Response:**

**Code:** HTTP 400 Bad Request
     
<pre>
    {
        "name": [
            "This field may not be blank."
        ]
    }
</pre>
        
**URL Params**

Required for take_job: `printer`

**Success Response:**

  `GET`
  Code: 200 OK     

  `POST`
  Code: 201 Created     
  
<pre>
  {
    "id": 5,
    "created": "2016-09-04T02:59:07.459088Z",
    "user": "me",
    "printer": "",
    "queue": "http://localhost:8000/queues/1/?format=api"
  }
</pre>


---
#### Specific Queue

View / update / delete an individual print queue. Note that deleting a queue
will delete all of its associated print jobs.

Also provides a function for taking a job for printing.

**URL**

/queues/_id_/

/queues/_id_/take_job/

**Methods**

`GET` | `DELETE` | `POST` | `PUT`
  
**Data Params:**

Required for take_job: `printer`

**Success Response**

  `GET /queues/1/`
  
  Code: 200 OK     

<pre>
{
    "created": "2016-09-03T20:33:46.200017Z", 
    "id": 1, 
    "name": "Printer One", 
    "printjobs": [
        "http://localhost:8000/printjobs/5/"
    ], 
    "url": "http://localhost:8000/queues/1/"
}
</pre>
 
  `POST` /queues/5/take_job/ data: printer=foo
  
  Code: 201 Created

  <pre>
  {
    "filename": "file.txt", 
    "id": 10, 
    "name": "", 
    "printer": "foo", 
    "queue": 5, 
    "state": "printing", 
    "user": "User 1"
  }
  </pre>


---
#### Print jobs

  View and add print jobs.

**URL:**

  /printjobs/

**Methods**
  
`GET` | `POST` | `PUT`

**Success Responses:**
 
`GET` 
  
Code: 200 OK
  
<pre>
  [
    {
        "id": 10,
        "created": "2016-09-05T14:27:15.799203Z",
        "user": "User 1",
        "filename": "file.txt",
        "printer": "Printer 1",
        "queue": "http://localhost:8000/queues/5/",
        "state": "printing",
        "url": "http://localhost:8000/printjobs/10/"
    }
  ]
</pre>
    
`POST`

Code: HTTP 201 Created
     
<pre>
  {
    "id": 11,
    "created": "2016-09-05T14:31:11.669716Z",
    "user": "User 2",
    "filename": "file2.txt",
    "printer": "",
    "queue": "http://localhost:8000/queues/5/",
    "state": "waiting",
    "url": "http://localhost:8000/printjobs/11/"
  }
</pre>


---
#### Specific Print Job

View / update / delete an individual print job.

**URL**

/printjobs/_id_/

**Methods**

`GET` | `DELETE` | `POST` | `PUT`
  
**Success Response**

  `GET`
  Code: 200 OK     
  
<pre>
  [
    {
        "created": "2016-09-05T14:31:11.669716Z", 
        "filename": "file2.txt", 
        "id": 11, 
        "printer": "", 
        "queue": "http://localhost:8000/queues/5/", 
        "state": "waiting", 
        "url": "http://localhost:8000/printjobs/11/", 
        "user": "User 2"
    }
   ]
</pre>
   
  `POST` (add job)
  Code: 201 Created     

<pre>
{
    "id": 11,
    "created": "2016-09-05T14:31:11.669716Z",
    "user": "User 2",
    "filename": "file2.txt",
    "printer": "",
    "queue": "http://localhost:8000/queues/5/",
    "state": "waiting",
    "url": "http://localhost:8000/printjobs/11/"
}
</pre>
