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
        "instructor": "Jeffrey Alain Johnson",
        "time": "9:55 am - 11:40 am",
        "days": "TR"
    },
    {
        "ID": "40805",
        "title": "Introduction to Computer Science I",
        "department": "CS",
        "course_num": "110",
        "section_num": "02",
        "instructor": "Beste Yuksel",
        "time": "4:35 pm - 6:20 pm",
        "days": "TR"
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
- `"instructor":string` instructor for the class
- `"time":string` time this class meets
- `"days":string` days this class meets

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
    "instructor": "Jeffrey Alain Johnson",
    "time": "9:55 am - 11:40 am",
    "days": "TR"
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
    "instructor": "Jeffrey Alain Johnson",
    "time": "9:55 am - 11:40 am",
    "days": "TR"
}
```

## Delete a class

**Definition**

`DELETE /classes/<ID>`

**Response**

- `404 Not Found` if the class does not exist
- `204 No Content` on success
