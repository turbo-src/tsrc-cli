
```
git clone ...
```

Install

```
poetry install
```

Experimental create user

```
python experiments/create_user.py
```

## Enpoints

### create user


status code: 201


```
{'data': {'createUser': '201'}}
```

If user already created.

status code: 200


```
{'data': {'createUser': 'There was an error: SequelizeUniqueConstraintError: Validation error'}}
```

#### Ideal

```
{
    "status": "success",
    "message": "User created successfully",
    "info": {
        "contributor_id": "12345",
        "contriburor_name": "new_user",
        "codehosts: "github"
    }
}
```