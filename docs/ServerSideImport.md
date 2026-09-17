# ServerSideImport API

> **Obsolete:** This API has been retired and is no longer functional. All calls return an error regardless of the parameters supplied. Do not use this API in new integrations.

Previously intended to import folders and documents located on the server's file system into an infoRouter path. This functionality has been removed and the endpoint is retained only for backward compatibility.

## Endpoint

```

/srv.asmx/ServerSideImport

```

## Methods

- **GET** `/srv.asmx/ServerSideImport?AuthenticationTicket=...&BaseServerSidePath=...&Items=...&TargetIRPath=...`

- **POST** `/srv.asmx/ServerSideImport` (form data)

- **SOAP** Action: `http://tempuri.org/ServerSideImport`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | " | Authentication ticket. Ignored " all calls fail before authentication is checked. |
| `BaseServerSidePath` | string | " | (Obsolete) Base path on the server file system. |
| `Items` | string | " | (Obsolete) Items to import. |
| `TargetIRPath` | string | " | (Obsolete) Destination infoRouter path. |

---

## Response

All calls return the following error response:

```xml

<response success="false" error="OBSELETE" />

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

> **This operation is obsolete and does nothing.** Every call is answered `4000` with a message saying
> so. It is still routed, so a client written against an older version gets an answer it can read
> rather than a 404, but there is no version of the call that works.

The answer is the single untranslated word `OBSELETE`, spelled that way. Import documents with
[UploadDocument](UploadDocument.md) or [UploadZip](UploadZip.md) instead.

## Notes

- This API always returns `success="false"` with `error="OBSELETE"`. No import is performed.

- The endpoint exists solely for backward compatibility with older clients that may call it.

- There is no replacement API for server-side file system imports in the current version.

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4000` | every call: the message is the untranslated literal "OBSELETE" |

