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

## Notes

- This API always returns `success="false"` with `error="OBSELETE"`. No import is performed.
- The endpoint exists solely for backward compatibility with older clients that may call it.
- There is no replacement API for server-side file system imports in the current version.

---
