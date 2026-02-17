# File drag and drop

```html
<div id="upload" ondrop="dropFile(event)" ondragover="allowDrop(event)">
  Drag and drop files.
</div>
<script>
  function dropFile(e) {
    e.preventDefault();
    var dt = e.dataTransfer;
    Array.from(dt.files).forEach((file) => {
      // TODO: ...
      console.log(file);
    });
  }

  function allowDrop(e) {
    e.preventDefault();
  }
</script>
```

<https://developer.mozilla.org/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop>
