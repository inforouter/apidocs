# AddPropertySetRowForUser API

Adds one or more property set rows to the specified infoRouter user. Property sets are custom metadata schemas; each row contains field values for a given property set definition.

## Endpoint

```
/srv.asmx/AddPropertySetRowForUser
```

## Methods

- **GET** `/srv.asmx/AddPropertySetRowForUser?authenticationTicket=...&userName=...&xmlpset=...`
- **POST** `/srv.asmx/AddPropertySetRowForUser` (form data)
- **SOAP** Action: `http://tempuri.org/AddPropertySetRowForUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username of the user to add property set rows to. |
| `xmlpset` | string | Yes | An XML string describing the property set rows to add (see format below). |

### xmlpset Format

The `xmlpset` parameter is an XML string. The root element contains one child element per property set; each property set element contains one child element per row to add.

```xml
<propertysets>
  <propertyset name="EmployeeInfo">
    <row RowNbr="0" Department="Finance" CostCenter="CC001" StartDate="2023-01-15" />
  </propertyset>
  <propertyset name="ContactInfo">
    <row RowNbr="0" PhoneNumber="+1-555-0100" OfficeLocation="Building A" />
  </propertyset>
</propertysets>
```

- The root element name (e.g., `<propertysets>`) can be anything.
- Each child element must have a `name` attribute matching an existing property set definition name.
- Each grandchild element represents one row to add. Set `RowNbr="0"` to add a new row.
- All other attributes on the row element are property set field names and their values.
- The pipe character `|` in field values is automatically escaped.

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response (single error)

```xml
<response success="false" error="Error message" />
```

### Error Response (multiple errors)

```xml
<response success="false" error="[log]">
  <logitem propertyset="PropertySetName" error="Error detail" />
</response>
```

---

## Required Permissions

**System administrator** or a user with permission to manage the target user's property sets.

---

## Example

### GET Request

```
GET /srv.asmx/AddPropertySetRowForUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
  &xmlpset=%3Cpropertysets%3E%3Cpropertyset+name%3D%22EmployeeInfo%22%3E%3Crow+RowNbr%3D%220%22+Department%3D%22Finance%22+%2F%3E%3C%2Fpropertyset%3E%3C%2Fpropertysets%3E
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddPropertySetRowForUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jdoe
&xmlpset=<propertysets><propertyset name="EmployeeInfo"><row RowNbr="0" Department="Finance" CostCenter="CC001" /></propertyset></propertysets>
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddPropertySetRowForUser>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:XmlPset>&lt;propertysets&gt;&lt;propertyset name="EmployeeInfo"&gt;&lt;row RowNbr="0" Department="Finance" /&gt;&lt;/propertyset&gt;&lt;/propertysets&gt;</tns:XmlPset>
    </tns:AddPropertySetRowForUser>
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

Puts a property set row on a user.

```javascript
const xmlpset = `<propertysets>
  <propertyset name="HR_DETAILS">
    <row rownbr="0" COSTCENTRE="4400" />
  </propertyset>
</propertysets>`;

await call('AddPropertySetRowForUser', { authenticationTicket: ticket, userName: 'jsmith', xmlpset });
```

The row comes back on [GetUser](GetUser.md) as a `<propertyrow>` with `RowNbr="1"` and a `<Log>`
recording who applied it. [UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md) can only
rewrite a row that exists, so this is the call that has to come first.

## Notes

- Use `RowNbr="0"` to add a new row. The system assigns the actual row number.
- Multiple property sets and multiple rows can be submitted in a single call.
- If one property set in the XML fails (e.g., not found), the error is logged and the call continues to process remaining property sets.
- To remove a row, use `DeletePropertySetRowForUser`.

---

## Related APIs

- [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) - Delete a property set row from a user
- [GetUser](GetUser.md) - Get user properties
- [AddPropertySetRow](AddPropertySetRow.md) - Add property set rows to a document or folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

The `xmlpset` parameter is a property set document:

```xml
<propertysets>
  <propertyset name="HR_DETAILS">
    <row rownbr="0" COSTCENTRE="4400" />
  </propertyset>
</propertysets>
```

`rownbr="0"` means "a new row" on the add; on the update and the delete it is the `RowNbr` the row
came back with, which starts at 1. The property set must be one defined with
`AppliestoUsers=true`.

On success this operation answers `<response success="true" error=""/>` with **no** `errorCode`
attribute, where most operations answer `errorCode="0"`. The same is true of
[UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md) and
[DeletePropertySetRowForUser](DeletePropertySetRowForUser.md).

---
