# HTTParty

https://github.com/jnunemaker/httparty

REST API Client 만들 때 쓰면 편한 라이브러리.

간단한 GET 예제:

```ruby
posts = HTTParty.get(
  'http://jsonplaceholder.typicode.com/posts',
  query: {
    userId: 1
  }
)

posts.each do |post|
  puts post.inspect
end
```

API Sample: [JSONPlaceholder - Fake online REST API for developers](http://jsonplaceholder.typicode.com/)
