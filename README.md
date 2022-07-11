# WebVPython on Pyodide

This is an embryonic attempt to run WebVPython on Pyodide.

Please use node version 18 or higher.

## To run locally:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version:

```bash
npm run build
```

Preview the production build with `npm run preview`.

To build the vpython package:

```
cd vpython
zip -r ../static/vpython.zip vpython
```
