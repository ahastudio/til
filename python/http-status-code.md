# HTTP Status Code

Flask 앱:

```python
from http import HTTPStatus
from app import app

@app.route('/posts', methods=['POST'])
def create_post():
    return '', HTTPStatus.CREATED
```

테스트:

```python
import pytest
from http import HTTPStatus
from app import app

def test_create_post():
    client = app.test_client()
    response = client.post('/posts')
    assert response.status_code == HTTPStatus.CREATED
```

<https://docs.python.org/3/library/http.html#http-status-codes>
