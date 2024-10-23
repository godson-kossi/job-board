# API Endpoints

## I. Adverts

### 1. Get all job adverts
>**[GET]** `/api/advert/`  

**Response:**
- **[200]** (application/json)
  ```json
  {
    "adverts":[
      {
        "key": "<integer>",
        "title": "<string>",
        "company": "<string>",
        "salary": "<integer>",
        "contract": "<literal[FX, PX, AS, TJ, IS]>",
        "duration": "<integer>",
        "competences": "<string>",
        "short_desc": "<string>",
        "long_desc": "<string>"
      },
      ...
    ]
  }
  ```

### 2. Create a new job advert
>**[POST]** `/api/advert/`  

**Permissions**: _Company_   

**Request:**  
(application/json)  
```json
{
  "title": "<string>",
  "company": "<string>",
  "salary": "<integer>",
  "contract": "<literal[FX, PX, AS, TJ, IS]>",
  "duration": "<integer>",
  "competences": "<string>",
  "short_desc": "<string>",
  "long_desc": "<string>"
}
```
**Response:**
- **[201]** _Created_
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_

### 3. Get a job advert
>**[GET]** `/api/advert/{id}`  
`{id}` _Advert ID._  

**Response:**
- **[200]** (application/json)
    ```json
    {
      "title": "<string>",
      "company": "<string>",
      "salary": "<integer>",
      "contract": "<literal[FX, PX, AS, TJ, IS]>",
      "duration": "<integer>",
      "competences": "<string>",
      "short_description": "<string>",
      "long_description": "<string>"
    }
    ```
- **[404]** _Not found_

### 4. Delete a job advert
>**[DELETE]** `/api/advert/{id}`  
`{id}` _Advert ID_ 

**Permissions**: _Company_   

**Response:**
- **[200]** _Done_
- **[401]** _Unauthorized_
- **[404]** _Not found_

### 5. Update a job advert
>**[PATCH]** `/api/advert/{id}`  
`{id}` _Advert ID_

**Permissions**: _Company_

**Request:**  
(application/json)  
  ```json
  { "<key>": "<value>", ... }
  ```

**Response:**
- **[200]** _Done_
- **[401]** _Unauthorized_
- **[404]** _Not found_
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_

### 6. Apply for a job
>**[POST]** `/api/advert/{id}/apply`  
`{id}` _Advert ID._

**Request:**  
(application/json)
```json
{
  "firstname": "<string>",
  "lastname": "<string>",
  "email": "<string>",
  "phone_number": "<string>",
  "degree": "<string>",
  "birthdate": "<string>"
}
```
**Response:**
- **[200]** _Done_
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[404]** _Not found_

### 7. Get Applications
>**[PATCH]** `/api/advert/{id}/apps`  
`{id}` _Advert ID_  

**Permissions**: _Company_

**Response:**
- **[200]** (application/json)
    ```json
      {
      "apps":[
        {
          "firstname": "<string>",
          "lastname": "<string>",
          "email": "<string>",
          "password": "<string>",
          "phone_number": "<string>",
          "degree": "<string>",
          "birthdate": "<string>"
        },
        ...
      ]
    }
    ```
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_
- **[404]** _Not found_

## II. Users

### 1. Authenticate user
>**[POST]** `/api/user/authenticate`  

**Request:**  
(application/json)  
```json
{ "email": "<string>", "password": "<string>" }
```

**Response:**
- **[200]** (application/json) (Cookie)
    ```json
    { "authToken": "<string", "userId": "int>" }
    ```
- **[401]** (application/json)
    ```json
    { "error": "<string>" }
    ```

### 2. Register a new user
>**[POST]** `/api/user/register`  

**Request:**  
(application/json)  
_Applicant User :_
```json

{
  "type": 0,
  "firstname": "<string>",
  "lastname": "<string>",
  "email": "<string>",
  "password": "<string>",
  "phone_number": "<string>",
  "degree": "<string>",
  "birthdate": "<string>"
}
```
**OR**  
_Company User :_
```json
{
  "type": 1,
  "name": "<string>",
  "email": "<string>",
  "password": "<string>",
  "address": "<string>",
  "phone_number": "<string>",
}
```

**Response:**
- **[200]** _Done_
- **[400]** (application/json)
  ```json
  { "error": "<string>" }
  ```
- **[404]** _Not found_

### 3. Get user details
>**[GET]** `/api/user/`  

**Response:**
- **[200]** (application/json)  
  _Applicant User :_
  ```json
  
  {
    "type": 0,
    "firstname": "<string>",
    "lastname": "<string>",
    "email": "<string>",
    "phone_number": "<string>",
    "degree": "<string>",
    "birthdate": "<string>"
  }
  ```
  **OR**  
  _Company User :_
  ```json
  {
    "type": 1,
    "name": "<string>",
    "email": "<string>",
    "address": "<string>",
    "phone_number": "<string>",
  }
  ```
- **[401]** _Unauthorized_

### 4. Disconnect user
>**[DELETE]** `/api/user/`  

**Response:**
- **[200]** _Done_
- **[401]** _Unauthorized_

### 5. Update user details
>**[PATCH]** `/api/user/`  

**Request:** (application/json)  
```json
{ "<key>": "<value>", ... }
```
**Response:**
- **[200]** _Done_
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** _Unauthorized_
- **[404]** _Not found_


## III. ADMINISTRATION

### 1. Verify Admin Account
>**[GET]** `/api/admin`  

**Permissions**: _Admin_

**Response:**
- **[200]** _Ok_
- **[401]** _Unauthorized_
- **[403]** _Forbidden_

### 2. Register a new user
>**[POST]** `/api/user/register`  

**Permissions**: _Admin_   

**Request:**  
(application/json)
```json
{
  "firstname": "<string>",
  "lastname": "<string>",
  "email": "<string>",
  "password": "<string>",
  "phone_number": "<string>",
  "degree": "<string>",
  "birthdate": "<string>",
  "permissions": "<int>"
}
```

**Response:**
- **[201]** _Created_
- **[400]** (application/json)
  ```json
  { "error": "<string>" }
  ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_
- **[404]** _Not found_

### 3. Get user details
>**[GET]** `/api/user/`  

**Permissions**: _Admin_

**Response:**
- **[200]** (application/json)
    ```json
    {
      "email": "<string>",
      "firstname": "<string>",
      "lastname": "<string>",
      "phone_number": "<string>",
      "degree": "<string>",
      "birthdate": "<string>"
    }
    ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_
- **[404]** _Not found_

### 4. Delete user account
>**[DELETE]** `/api/user/`  

**Permissions**: _Admin_

**Response:**
- **[200]** _Done_
- **[401]** _Unauthorized_
- **[403]** _Forbidden_
- **[404]** _Not found_

### 5. Update user details
>**[PATCH]** `/api/user/`  

**Permissions**: _Admin_

**Request:**  
(application/json)
```json
{ "<key>": "<value>", ... }
```
**Response:**
- **[200]** _Done_
- **[400]** (application/json)
    ```json
    { "error": "<string>" }
    ```
- **[401]** _Unauthorized_
- **[403]** _Forbidden_
- **[404]** _Not found_

