# USFCA Class Schedule API

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List All Classes

**Definition**

`GET /classes`

**Response**

- `200 OK` on success

```json
[
    {
        "ID": "40804",
        "title": "Introduction to Computer Science I",
        "department": "CS",
        "course_num": "110",
        "section_num": "01",
        "actual": "20",
        "capacity": "23",
        "instructor": "Jeffrey Alain Johnson"
    }
]
```

### Registering a new class

**Definition**

`POST /classes`

**Arguments**

- `"ID":integer` a globally unique identifier for this class
- `"title":string` course title
- `"department":string` education division for this class
- `"course_num":integer` course number for this class
- `"section_num":integer` section number for this class
- `"actual":integer` number of students enrolled
- `"capacity":integer` max number of students allowed to enroll
- `"instructor":string` instructor for the class

If a class with the given ID already exists, the existing class will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "ID": "40804",
    "title": "Introduction to Computer Science I",
    "department": "CS",
    "course_num": "110",
    "section_num": "01",
    "actual": "20",
    "capacity": "23",
    "instructor": "Jeffrey Alain Johnson"
}
```

## Lookup class details

`GET /classes/<ID>`

**Response**

- `404 Not Found` if the class does not exist
- `200 OK` on success

```json
{
    "ID": "40804",
    "title": "Introduction to Computer Science I",
    "department": "CS",
    "course_num": "110",
    "section_num": "01",
    "actual": "20",
    "capacity": "23",
    "instructor": "Jeffrey Alain Johnson"
}
```

## Delete a class

**Definition**

`DELETE /classes/<ID>`

**Response**

- `404 Not Found` if the class does not exist
- `204 No Content` on success
