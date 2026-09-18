# MaintenanceBeat API

> ----- **This API is obsolete and no longer functional.** The method body has been fully commented out. Calling this endpoint does nothing and returns no response. It is retained in the API surface for backward compatibility only. Do not use this API in new integrations.

Previously, this endpoint was intended to be called by infoRouter's internal maintenance scheduler to trigger server-side self-maintenance tasks such as index cleanup, session expiry, and background job execution. These maintenance operations are now managed automatically by the server's built-in background service infrastructure without requiring an external HTTP trigger.

## Endpoint

```

/srv.asmx/MaintenanceBeat

```

## Methods

- **GET** `/srv.asmx/MaintenanceBeat`

- **POST** `/srv.asmx/MaintenanceBeat` (form data)

- **SOAP** Action: `http://tempuri.org/MaintenanceBeat`

## Parameters

This API accepts no parameters. The `CancellationToken` it receives internally is injected by the ASP.NET Core framework and is not a caller-supplied argument.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | " | " | No parameters are accepted. |

---

## Response

This endpoint returns **no response body**. The HTTP response is always `200 OK` with an empty body, regardless of whether the call succeeded or failed, because the implementation is a no-op.

---

## Required Permissions

No authentication ticket is required. This endpoint was intended for internal system use only and has no access control.

---

## Example

### GET Request

```

GET /srv.asmx/MaintenanceBeat HTTP/1.1

```

**Response:** `200 OK` with empty body.

### POST Request

```

POST /srv.asmx/MaintenanceBeat HTTP/1.1

Content-Length: 0

```

**Response:** `200 OK` with empty body.

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:MaintenanceBeat />

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

Obsolete. It does nothing and answers nothing.

```javascript
// Answers HTTP 200 with an empty body - not XML, so do not parse it.
await fetch('/srv.asmx/MaintenanceBeat');
```

It used to start the server's self-maintenance run. That work is a background service now and the
method body has been commented out; the endpoint stays on the contract so that a client which
still calls it goes on getting the same nothing it has always got. It takes no ticket and no
parameters.

## Notes

- **Fully obsolete**: The implementation was commented out as of infoRouter 8.1 and later. Calling this endpoint has no effect whatsoever.

- **No response body**: Unlike all other infoRouter APIs, `MaintenanceBeat` returns `void`. There is no XML response, no success/failure indicator, and no error element.

- **No parameters**: The endpoint takes no caller-supplied parameters.

- **System use only**: This endpoint was never intended for use by external integrations or third-party clients. It was an internal scheduling hook.

- **Replacement**: Server maintenance is now handled automatically. There is no replacement API for this functionality.

---

## Related APIs

*(None " this is a standalone obsolete endpoint with no functional equivalent.)*

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `*none*` | this operation always answers HTTP 200 with an empty body - there is no response document, successful or otherwise |

This API returns no error codes. The endpoint always returns HTTP `200 OK` with an empty body.
