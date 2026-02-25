# GetDocumentReadLogHistory API

Returns the complete read/view log history for a **single specified user** on a document. Each entry records one time the user opened or accessed a specific version of the document. This is the per-user variant of `GetDocumentViewLog`: instead of returning all users' access history for a document, it narrows results to the given `UserID`. Use this API to audit whether a specific person has read a particular document and when.

## Endpoint

```
/srv.asmx/GetDocumentReadLogHistory
```

## Methods

- **GET** `/srv.asmx/GetDocumentReadLogHistory?AuthenticationTicket=...&Path=...&UserID=...`
- **POST** `/srv.asmx/GetDocumentReadLogHistory` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentReadLogHistory`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). The path must resolve to an existing document. |
| `UserID` | int | Yes | Internal infoRouter user ID of the person whose view history to return. Obtain this value from `GetUser`, `GetAllUsers`, or similar user lookup APIs. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<ViewLog>` element with zero or more `<Version>` child elements -" one per time the specified user accessed a version of the document. Entries span both the current view log and historical read log.

```xml
<response success="true" error="">
  <ViewLog>
    <Version
      Number="2000000"
      UserID="12"
      Viewer="John Smith"
      ViewDate="2024-06-15T10:30:00.000Z" />
    <Version
      Number="2000000"
      UserID="12"
      Viewer="John Smith"
      ViewDate="2024-06-10T08:45:00.000Z" />
    <Version
      Number="1000000"
      UserID="12"
      Viewer="John Smith"
      ViewDate="2024-05-01T09:15:00.000Z" />
  </ViewLog>
</response>
```

### Version Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `Number` | int | External version number of the document version that was accessed. Version 1 = `1000000`, Version 2 = `2000000`, etc. |
| `UserID` | int | Internal user ID of the person who accessed the document (always the same as the `UserID` parameter). |
| `Viewer` | string | Full name of the user who accessed the document. |
| `ViewDate` | string | UTC date and time of the access event in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty string if not recorded. |

### No Entries Response

When the specified user has never accessed the document, or the document has no view log for that user:

```xml
<response success="true" error="">
  <ViewLog />
</response>
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have at least **read access** to the document AND must have the **`DocumentReadViewLog`** permission on the document. This permission is typically granted to document owners, domain managers, and system administrators. Regular read-only users cannot retrieve the view log unless explicitly granted the `DocumentReadViewLog` permission.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentReadLogHistory
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
  &UserID=12
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentReadLogHistory HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
&UserID=12
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentReadLogHistory>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
      <tns:UserID>12</tns:UserID>
    </tns:GetDocumentReadLogHistory>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Single User Filter**: Unlike `GetDocumentViewLog` which returns access history for all users, this API returns entries for one specific user only. The filter is applied after the full log is retrieved -" the permission check is the same as `GetDocumentViewLog`.
- **All Versions Included**: Access events for every version of the document are returned, not just the current (published) version.
- **UserID Must Be Valid**: The `UserID` must be the numeric internal ID of an existing infoRouter user. If the user has never accessed the document, an empty `<ViewLog />` is returned (not an error).
- **ViewDate UTC**: All `ViewDate` timestamps are returned in UTC ISO 8601 format. An empty string indicates that the access date was not recorded.
- **Version Number Format**: The `Number` attribute uses the external version format where version 1 = `1000000`, version 2 = `2000000`, etc.
- **Document Path Only**: This API only accepts document paths. Passing a folder path returns a "Document not found" error.
- **How to Get UserID**: Use `GetUser`, `GetAllUsers`, or `GetAllUsers1` to look up a user's internal `UserID` by username.

---

## Related APIs

- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the full view/access log for a document for all users
- [GetUserViewLog](GetUserViewLog.md) - Get all documents read by a specific user
- [GetUserViewLog1](GetUserViewLog1.md) - Get all documents read by a specific user within a date range
- [GetUser](GetUser.md) - Look up a user's internal ID by username

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | The specified `Path` does not resolve to an existing document. |
| `Insufficient rights.` | The calling user does not have the `DocumentReadViewLog` permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
