# DeleteDownloadHandler API

Deletes a download handler and discards its associated temporary file on the server. Use this to clean up after a chunked download is complete or if the download session is cancelled before all chunks are retrieved.

## Endpoint

```

/srv.asmx/DeleteDownloadHandler

```

## Methods

- **GET** `/srv.asmx/DeleteDownloadHandler?authenticationTicket=...&DownloadHandler=...`

- **POST** `/srv.asmx/DeleteDownloadHandler` (form data)

- **SOAP** Action: `http://tempuri.org/DeleteDownloadHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DownloadHandler` | string (GUID) | Yes | The handler GUID returned by `GetDownloadHandler`, `GetDownloadHandlerByVersion`, or `DownloadZipWithHandler`. Must be a valid GUID string. |

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="Error message" />

```

---

## Required Permissions

Any authenticated user may call this API. The handler is resolved by GUID -" only the handler file path associated with the current user's session is deleted.

---

## Chunked Download Workflow

Download handlers are used in chunked download scenarios to stage large files server-side before the client retrieves them in pieces:

1. **`GetDownloadHandler`** (or `GetDownloadHandlerByVersion` / `DownloadZipWithHandler`) -" Prepare the file and obtain a handler GUID.

2. **`DownloadFileChunk`** -" Download the file content in sequential chunks using the handler GUID.

3. **`DeleteDownloadHandler`** -" Clean up the handler and its temporary file once all chunks are downloaded or if the download is abandoned.

---

## Example

### GET Request

```

GET /srv.asmx/DeleteDownloadHandler

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &DownloadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DeleteDownloadHandler HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&DownloadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DeleteDownloadHandler>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:DownloadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:DownloadHandler>

    </tns:DeleteDownloadHandler>

  </soap:Body>

</soap:Envelope>

```

---

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Ends a download and lets the server discard the staged archive.

```javascript
try {
  // ... read chunks ...
} finally {
  await call('DeleteDownloadHandler', {
    authenticationTicket: ticket,
    DownloadHandler: handler
  });
}
```

Deleting the same handler twice is a success, not a `4041` - the operation is safe to call in a
`finally`. A value that is not a GUID is refused before anything is looked up, with the untranslated
literal `bad Request`, which reads the same in every language and matches no other message in the
API.

Reading a chunk after the handler is deleted is `4000`, the same as for a handler that never existed.

## Notes

- If the handler's temporary file does not exist (e.g. already cleaned up), the call still returns success -" no error is raised.

- Passing a string that is not a valid GUID format returns an error immediately without performing any authentication check.

- Always call `DeleteDownloadHandler` after finishing a chunked download to free temporary server storage, even if the download was not fully completed.

---

## Related APIs

- [GetDownloadHandler](GetDownloadHandler.md) - Prepare a document for chunked download and obtain a handler GUID

- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Prepare a specific document version for chunked download

- [DownloadZipWithHandler](DownloadZipWithHandler.md) - Prepare a zip archive of folders and documents for chunked download

- [DownloadFileChunk](DownloadFileChunk.md) - Download a chunk of a file using a handler

- [DeleteUploadHandler](DeleteUploadHandler.md) - Delete an upload handler and discard its staged data

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `DownloadHandler` is not a GUID: "bad Request" |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `bad Request` | `DownloadHandler` is not a valid GUID string. |

---

