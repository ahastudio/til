# Visual Studio Code User and Workspace Settings

<https://code.visualstudio.com/docs/getstarted/settings>

## JSON configuration file

Command Palette (`⇧⌘P`) > `Preferences: Open Settings (JSON)`

```json
{
    "telemetry.enableTelemetry": false,
    "window.newWindowDimensions": "offset",
    "workbench.startupEditor": "none",

    "editor.tabCompletion": "on",

    "editor.tabSize": 2,
    "editor.rulers": [
        80
    ],
    "editor.minimap.enabled": false,

    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },

    // ...(후략)...
}
```
