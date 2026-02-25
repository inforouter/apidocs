# DeletePropertySetRowForUser API

Deletes one or more property set rows from the specified infoRouter user.

## Endpoint

```
/srv.asmx/DeletePropertySetRowForUser
```

## Methods

- **GET** `/srv.asmx/DeletePropertySetRowForUser?authenticationTicket=...&userName=...&xmlpset=...`
- **POST** `/srv.asmx/DeletePropertySetRowForUser` (form data)
- **SOAP** Action: `http://tempuri.org/DeletePropertySetRowForUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username of the user whose property set rows will be deleted. |
| `xmlpset` | string | Yes | An XML string identifying the property set rows to delete (see format below). |

### xmlpset Format

The `xmlpset` parameter is an XML string. The root element contains one child element per property set; each property set element contains one child element per row to delete.

```xml
<propertysets>
  <propertyset name="EmployeeInfo">
    <row RowNbr="1" />
  </propertyset>
</propertysets>
```

- The root element name can be anything.
- Each child element must have a `name` attribute matching an existing property set definition name.
- Each grandchild element represents one row to delete. Set `RowNbr` to the row number to delete.
- The `RowNbr` attribute identifies which row to remove. Other attributes are ignored for DELETE operations.

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
GET /srv.asmx/DeletePropertySetRowForUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
  &xmlpset=%3Cpropertysets%3E%3Cpropertyset+name%3D%22EmployeeInfo%22%3E%3Crow+RowNbr%3D%221%22+%2F%3E%3C%2Fpropertyset%3E%3C%2Fpropertysets%3E
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeletePropertySetRowForUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jdoe
&xmlpset=<propertysets><propertyset name="EmployeeInfo"><row RowNbr="1" /></propertyset></propertysets>
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeletePropertySetRowForUser>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:XmlPset>&lt;propertysets&gt;&lt;propertyset name="EmployeeInfo"&gt;&lt;row RowNbr="1" /&gt;&lt;/propertyset&gt;&lt;/propertysets&gt;</tns:XmlPset>
    </tns:DeletePropertySetRowForUser>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Specify the `RowNbr` of the exact row to delete. Use `GetUser` or related APIs to first determine existing row numbers.
- Multiple property sets and rows can be processed in a single call.
- If one property set in the XML fails, the error is logged and the call continues to process remaining entries.
- To add a row, use `AddPropertySetRowForUser`.

---

## Related APIs

- [AddPropertySetRowForUser](AddPropertySetRowForUser.md) - Add a property set row to a user
- [GetUser](GetUser.md) - Get user properties
- [DeletePropertySetRow](DeletePropertySetRow.md) - Delete a property set row from a document or folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Property set not found | A property set named in the XML does not exist. |
| Row not found | The specified `RowNbr` does not exist for this user. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeletePropertySetRowForUser*
