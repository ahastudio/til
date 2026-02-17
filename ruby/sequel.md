# Sequel: The Database Toolkit for Ruby

- http://sequel.jeremyevans.net/
- https://github.com/jeremyevans/sequel

## Association

Association Basics

- http://sequel.jeremyevans.net/rdoc/files/doc/association_basics_rdoc.html

## MS-SQL

TinyTDS - Simple and fast FreeTDS bindings for Ruby using DB-Library

- https://github.com/rails-sqlserver/tiny_tds

Ruby Sequel TinyTDS MS SQL Example

- https://gist.github.com/albertico/af9691562415c415e49b

## Example

```ruby
require 'sequel'
require 'tiny_tds'

DB = Sequel.connect(
  adapter: 'tinytds',
  host: ENV['MSSQL_HOST'],
  port: ENV['MSSQL_PORT'],
  database: ENV['MSSQL_DATABASE'],
  user: ENV['MSSQL_USERNAME'],
  password: ENV['MSSQL_PASSWORD']
)

class Shop < Sequel::Model(:shop)
  set_primary_key :shop_no
  one_to_many :item_groups, key: :shop_no, order: :order_seq
end

class ItemGroup < Sequel::Model(:item_group)
  set_primary_key [:shop_no, :item_group_seq]
  many_to_many :items,
    left_key:  [:shop_no, :item_group_seq],
    right_key: [:shop_no, :item_seq],
    join_table: :shop_item_group_relation,
    order: :order_seq
end

class Item < Sequel::Model(:item)
  set_primary_key [:shop_no, :item_seq]
  one_to_many :option_groups, key: [:shop_no, :item_seq], order: :order_seq
end

class OptionGroup < Sequel::Model(:option_group)
  set_primary_key [:shop_no, :item_seq, :option_group_seq]
  # TODO: one_to_many ...
end
```
