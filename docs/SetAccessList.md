# SetAccessList API

Sets the access list (security permissions) for the document or folder at the specified path.

## Endpoint

```
/srv.asmx/SetAccessList
```

## Methods

- **GET** `/srv.asmx/SetAccessList?authenticationTicket=...&Path=...&AccessListXML=...&ApplyToTree=...`
- **POST** `/srv.asmx/SetAccessList` (form data)
- **SOAP** Action: `http://tempuri.org/SetAccessList`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |
| `AccessListXML` | string | Yes | XML string describing the new access list. See format below. |
| `ApplyToTree` | bool | Yes | If `true` and the path is a folder, applies the access list recursively to all subfolders and documents. Ignored for documents. |

### AccessListXML Format

The `AccessListXML` parameter must be a valid XML string with the following structure:

```xml
<AccessList>
  <!-- Optional: Anonymous access -->
  <Anonymous Right="0" />

  <!-- Optional: All domain members -->
  <DomainMembers Right="2" />

  <!-- Zero or more user groups -->
  <UserGroup DomainName="Finance" GroupName="Managers" Right="6" />
  <UserGroup DomainName="" GroupName="AllStaff" Right="4" />

  <!-- Zero or more individual users -->
  <User UserName="jsmith" Right="5" />
</AccessList>
```

### Right Values

| Right | Description |
|-------|-------------|
| `0` | No Access |
| `1` | List |
| `2` | Read |
| `3` | Add |
| `4` | Add & Read |
| `5` | Change |
| `6` | Full Control |

- **Global user groups** have an empty `DomainName` attribute or omit it entirely.
- Omitting `<Anonymous>` or `<DomainMembers>` leaves those entries unchanged or set to no access.
- Right values outside the range 0-"6 are clamped: values below 0 are treated as 0, values above 6 are treated as 6.

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**Change security permission** (ActionId 11) on the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/SetAccessList
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &AccessListXML=<AccessList><DomainMembers Right="2"/><UserGroup DomainName="Finance" GroupName="Managers" Right="6"/></AccessList>
  &ApplyToTree=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetAccessList HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&AccessListXML=<AccessList><DomainMembers Right="2"/><UserGroup DomainName="Finance" GroupName="Managers" Right="6"/></AccessList>
&ApplyToTree=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetAccessList>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:AccessListXML>
        <![CDATA[
        <AccessList>
          <DomainMembers Right="2" />
          <UserGroup DomainName="Finance" GroupName="Managers" Right="6" />
          <User UserName="jsmith" Right="5" />
        </AccessList>
        ]]>
      </tns:AccessListXML>
      <tns:ApplyToTree>false</tns:ApplyToTree>
    </tns:SetAccessList>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Setting the access list on a document ignores the `ApplyToTree` parameter.
- The `ApplyToTree` parameter only applies when the path points to a **folder**.
- To revert to inherited security from the parent folder, use `ApplyInheritedAccessList` instead.
- To read the current access list, use `GetAccessList`.
- URL-encode the `AccessListXML` value when passing via GET or form POST.

---

## Related APIs

- [GetAccessList](GetAccessList.md) - Retrieve the current access list
- [GetAccessListHistory](GetAccessListHistory.md) - Retrieve the access list history
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Revert to inherited security
- [GetOwner](GetOwner.md) - Get the owner of a document or folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Access denied | The calling user lacks permission to change security on this item. |
| Invalid XML | The `AccessListXML` parameter is not valid XML or has no root element. |
| `SystemError:...` | An unexpected server-side error occurred. |

---