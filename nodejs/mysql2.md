# Node MySQL 2
https://github.com/sidorares/node-mysql2

## Promise

```javascript
async function main() {
  const  mysql = require('mysql2/promise');
  const connection = await mysql.createConnection({
    host:'localhost', user: 'root', database: 'test',
  });
  const sql = 'SELECT * FROM users WHERE name=?';
  const values = ['John Smith'];
  const [results, fields] = await connection.execute(sql, values);
}
```
