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
- Right values outside the range 0 to 6 are refused with `4000` naming the value, and nothing is written. They used to be clamped, which turned a typo like `Right="66"` into a grant of full control.

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

Replaces the access list on a folder or a document, and stops it inheriting one.

```javascript
await call('SetAccessList', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports',
  AccessListXML:
    '<AccessList>' +
      '<DomainMembers Right="2" />' +
      '<UserGroup DomainName="" GroupName="AllStaff" Right="4" />' +
      '<User UserName="jsmith" Right="5" />' +
    '</AccessList>',
  ApplyToTree: false
});

// Then read it back - see the warning below.
const written = await call('GetAccessList', { authenticationTicket: ticket, Path: '/Finance/Reports' });
```

**It replaces the whole list.** Anything not named is gone, so read the current list with
[GetAccessList](GetAccessList.md) and send it back with the changes. `<AccessList />` is a valid list
meaning "nobody explicitly", and `ApplyToTree=true` writes the same list down the whole subtree.

> **A holder it cannot find is refused.** A user name nobody has, or a group that does not
> exist, is answered `4041` and **nothing at all is written** - the access list is not applied
> in part. Check the names before sending, and read the list back if you want to be sure.

Malformed `AccessListXML` is refused properly with `4000` here - unlike several other XML parameters
in this API, which let the exception out as an HTTP 500.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path - including one the caller may not see |
| `4030` | the caller may not change security on this item |
| `4000` | `AccessListXML` is not well-formed XML |
| `none` | a user or group that cannot be found is dropped without a word, and the call still succeeds |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Access denied | The calling user lacks permission to change security on this item. |
| Invalid XML | The `AccessListXML` parameter is not valid XML or has no root element. |
| `SystemError:...` | An unexpected server-side error occurred. |

---