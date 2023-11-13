# fastapi-pdp-blog

#### Run the local develop server:

    docker-compose up -d --build
  
##### Server will bind in address [http://fastapi.localhost:8009](http://fastapi.localhost:8009).



#### For running the app without docker:

```
cd app
uvicorn app:app --host 0.0.0.0 --port 8009 --reload
```

### Migration commands:
#### After creating models, import that model inside models/__init__.py file, then run migration command 
Create migrations file:
```
alembic revision -m "Put message here ..." --autogenerate
```

Migrate:
```
alembic upgrade head
```

Run formatting before making a commit
```
cd app && flake8 . && isort . black .
```

Run tests before making commit
```
cd app && python -m pytest
```