# `collection_radio_buttons`

여러 개 중 하나를 선택해야 할 경우, 라디오 버튼을 사용할 수 있다.

반복적으로 `radio_button`과 `label`을 사용하는 코드:

```ruby
<% Tag.all.each do |tag| %>
  <%= f.radio_button :tag_id, tag.id %>
  <%= f.label :tag_id, tage.name, value: tag.id %>
<% end %>
```

특정 모델을 활용해 간단히 표현하고 싶다면 `collection` 메서드를 사용할 수 있다.

```ruby
<%= f.collection_radio_buttons :tag_id, Tag.all, :id, :name %>
```

각 아이템을 `div` 태그 등으로 감싸는 것 같은 변화를 주고 싶다면 block을 사용하면 된다.

```ruby
<%= f.collection_radio_buttons :tag_id, Tag.all, :id, :name do |item_form| %>
  <div class="tag">
    <%= item_form.radio_button %>
    <%= item_form.label %>
  </div>
<% end %>
```

---

- http://api.rubyonrails.org/classes/ActionView/Helpers/FormHelper.html#method-i-radio_button
- http://api.rubyonrails.org/classes/ActionView/Helpers/FormBuilder.html#method-i-radio_button
- http://api.rubyonrails.org/classes/ActionView/Helpers/FormBuilder.html#method-i-collection_radio_buttons
- https://github.com/rails/rails/blob/master/actionview/lib/action_view/helpers/tags/collection_helpers.rb
