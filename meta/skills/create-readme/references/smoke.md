# :dash: smoke

[![NPM version](https://img.shields.io/npm/v/smoke.svg)](https://www.npmjs.com/package/smoke)
[![Build Status](https://github.com/sinedied/smoke/workflows/build/badge.svg)](https://github.com/sinedied/smoke/actions)
![Node version](https://img.shields.io/node/v/smoke.svg)
[![XO code style](https://img.shields.io/badge/code_style-XO-5ed9c7.svg)](https://github.com/sindresorhus/xo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Simple yet powerful file-based mock server with recording abilities

![demo](https://user-images.githubusercontent.com/593151/49312821-9f2cc680-f4e5-11e8-900a-117120c38422.gif)

Just drop a bunch of (JSON) files in a folder and you're ready to go!

### Basic mock example
1. Start the server: `smoke`
2. Create a file named `get_api#hello.json`:
    ```json
    {
      "message": "hello world!"
    }
    ```
3. Test the mock: `curl http://localhost:3000/api/hello`

### Features

**Smoke** is a file-based, convention over configuration mock server that can fill your API mocking needs without any
complex setup. Yet, it supports many advanced features and dynamic mocks for almost any situation:

- Generate mocks quickly by recording responses from an existing server
- Use folders and file names to describe API routes and REST methods
- Use templates to generate responses based on input queries and route parameters
- Add / edit / remove mocks without restarting the server
- Generate mocks with JavaScript for more complex responses
- Define different mock sets to simulate various scenarii (errors...), with fallback
- Customize headers and status code if needed, automatically detect content-type if not specified
- Add custom middlewares to modify requests/responses
- Mock only specific requests and proxy the rest to an existing server
- Supports CORS (cross-origin resource-sharing)

## Installation

```bash
npm install -g smoke
```

## Usage

See [some example mocks](test/mocks) to quickly get a grasp of the syntax and possibilities.

CLI usage is quite straightforward you can just run `smoke` unless you want to add some options:
```
Usage: smoke [<mocks_folder>] [options]

Base options:
  -p, --port <num>                  Server port           [default: 3000]
  -h, --host <host>                 Server host           [default: "localhost"]
  -s, --set <name>                  Mocks set to use      [default: none]
  -n, --not-found <glob>            Mocks for 404 errors  [default: "404.*"]
  -i, --ignore <glob>               Files to ignore       [default: none]
  -k, --hooks <file>                Middleware hooks      [default: none]
  -x, --proxy <host>                Fallback proxy if no mock found
  -o, --allow-cors [all|<hosts>]    Enable CORS requests  [default: none]
  --https                           Enable secure request serving with HTTPS [default: false]
  -l, --logs                        Enable server logs
  -v, --version                     Show version
  --help                            Show help

Mock recording:
  -r, --record <host>               Proxy & record requests if no mock found
  -c, --collection <file>           Save to single file mock collection
  -d, --depth <N>                   Folder depth for mocks  [default: 1]
  -a, --save-headers                Save response headers
  -q, --save-query                  Save query parameters
```

### File naming

**General format:** `methods_api#route#@routeParam$queryParam=value.__set.extension`

The path and file name of the mock is used to determinate:

#### Supported HTTP methods
Optionally prefix your file by the HTTP method supported followed by an underscore (for example `get_`).
You can specify multiple methods at once using a `+` to separate them (for example `post+put_`);
If no method is specified, the mock will be used for any HTTP method.

#### Server route and named route parameters
Use any combination of folders or hash-separated components to specify the server route.

For example `api/example/get_hello.json` is equivalent to `get_api#example#hello.json` and will respond to
`GET api/example/hello` requests.

Additionaly, any route component can be defined as a route parameter by prefixing the name with `@`, for example
`api#resource#@id.json` will match `GET api/resource/1` and expose `1` as the value for the `id` parameter that can be
used in dynamic mocks (templates or JavaScript).

#### Query parameters
You can further discriminate mocks by adding query parameters to match after defining the route, using a `$` (instead
of the regular `?`) like you would specify them in a request.

For example `get_api#hello$who=john.json` will match the request `api/get_hello?who=john.json`.

Multiple query parameters to match can be added with `&`, for example `get_api#hello$who=john&greet=hi.json`.
Any specified query parameter in the file name must be matched (in any order) by the request, but the opposite is not
needed.

Note that special characters must be URL-encoded, for example use `get_api#hello$who=john%20doe.json` to set the
parameter `who` with the value `john doe`.

> Tip: If you need to URL-encode a string, just run `node -p "encodeURIComponent('some string')"` in a terminal.

#### Content type
The file extension will determine the content type of the response if it's not already specified in a
[custom header](#custom-status-and-headers).

Files with no extension will use the default MIME type `application/octet-stream`.

You can have multiple mocks with the same API route and different file extensions, the server will then use the best
mock depending of the [`Accept` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept) of the
request.

#### Mock set
You can optionally specify a mock set before the file extension by using a `__set-name` suffix after the file name.

For example `get_api#hello__error.json` will only be used if you start the server with the `error` set enabled:
`smoke --set error`.

If you do not specify a mock set on your file name, it will be considered as the default mock for the specified route
and will be used as a fallback if no mock with this set matched.

#### Templates
If you add an underscore `_` after the file extension, the mock will be processed as a template before being sent to
the client. Templates works only on text-based formats.

For example `get_hello.html_` or `get_hello.json_` will be treated as templates.

Every template can use an implicit context object that have these properties defined:
- `method`: the HTTP method of the request (ex: `'GET'`, `'POST'`)
- `query`: map with query parameters that were part of the request URL.
- `params`: map containing matched route parameters.
- `headers`: map containing request headers
- `body`: the request body. JSON bodies are automatically parsed.
- `files`: if the request includes `multipart/form-data`, this will be the array of uploaded files

##### Template syntax

- `{{ }}` interpolates data in place
- `{{{ }}}` escapes HTML special chars from interpolated string
- `<{ }>` evaluates JavaScript to generate data

### Custom status and headers

By default all mocks responses are sent with a status code `200` (OK), or `204` (No content) if a mock file is empty.

You can customize the response status and (optionally) headers with JSON and JavaScript files:
```js
{
  "statusCode": 400,
  "body": {
    "error": "Bad request"
  },
  "headers": {
    "Content-Type": "text/plain"
  }
}
```

### Mock formats

Any file format is supported for mocks. Text formats can be processed as templates by adding an underscore to the file extension.

#### JavaScript mocks

Define dynamic mocks using `.js` extension. Module exports a function taking input data and returns the response body or an object with status code, headers and body.

### Fallback proxy

Use `--proxy <host>` to proxy every request for which a mock does not exist.

### Mock recording

Use `--record <host>` to proxy and record responses as mock files.

### Middleware hooks

Hook on Express middleware to modify requests/responses using `--hooks <file>`.

## Enabling CORS

Pass hosts to `-o` or `--allow-cors`. Accepts `all` for `*` or comma-separated host list.

### Single file mock collection

Regroup multiple mocks in `.mocks.js` files. Convert between formats with `smoke-conv`.

## Migration from v1/v2/v3 to v4

Default module format changed from CommonJS to ES modules. Rename `*.js` to `.cjs` for backward compatibility.

> [!NOTE]
> If you try to record new mocks into an existing collection in CommonJS format, the result will be saved into a new collection in ES modules format.
