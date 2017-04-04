# reconstructor decorator

DB에서 가져올 땐 생성자가 실행되지 않음. `@reconstructor` decorator 사용.

```python
from sqlalchemy import orm

class MyMappedClass(object):
    def __init__(self, data):
        self.data = data
        # we need stuff on all instances, but not in the database.
        self.stuff = []

    @orm.reconstructor
    def init_on_load(self):
        self.stuff = []
```

(코드 출처: http://docs.sqlalchemy.org/en/latest/orm/constructors.html)
