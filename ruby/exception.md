# Exception Handling

<https://docs.ruby-lang.org/en/3.3/syntax/exceptions_rdoc.html>

> If you are inside a method, you do not need to use `begin` or `end`
> unless you wish to limit the scope of rescued exceptions.

```ruby
def set_user
  @user = User.find(params[:id])
rescue ActiveRecord::RecordNotFound
  # ...
end
```
