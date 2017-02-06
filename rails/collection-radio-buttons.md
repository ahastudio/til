# `collection_radio_buttons`

여러 개 중 하나를 선택해야 할 경우, 라디오 버튼을 사용할 수 있다.

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

---

- http://api.rubyonrails.org/classes/ActionView/Helpers/FormHelper.html#method-i-radio_button
- http://api.rubyonrails.org/classes/ActionView/Helpers/FormBuilder.html#method-i-radio_button
- http://api.rubyonrails.org/classes/ActionView/Helpers/FormBuilder.html#method-i-collection_radio_buttons
