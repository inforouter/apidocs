# AssociationTypes API

Returns the list of association types defined in the system. Each association type has a forward name (used when the current item is the source of the association) and a reverse name (used when the current item is the target). Use this API to populate association type drop-downs, validate `AssociationTypeID` values before calling [AssociateDocument](AssociateDocument.md), or display human-readable type names alongside association data returned by the `Associated*` APIs.

## Endpoint

```
/srv.asmx/AssociationTypes
```

## Methods

- **GET** `/srv.asmx/AssociationTypes?AuthenticationTicket=...`
- **POST** `/srv.asmx/AssociationTypes` (form data)
- **SOAP** Action: `http://tempuri.org/AssociationTypes`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

The response contains a `<response success="true">` root element with an `<AssociationTypes>` child element containing one `<AssociationType>` element per defined type. Types are returned ordered by `AssociationTypeID`.

```xml
<response success="true">
  <AssociationTypes>
    <AssociationType
        AssociationTypeID="0"
        AssociationTypeName="Related"
        ReverseNameTypeName="Related" />
    <AssociationType
        AssociationTypeID="1"
        AssociationTypeName="Rendition"
        ReverseNameTypeName="Rendition Of" />
    <AssociationType
        AssociationTypeID="2"
        AssociationTypeName="Copy"
        ReverseNameTypeName="Copy Of" />
    <AssociationType
        AssociationTypeID="3"
        AssociationTypeName="Parent"
        ReverseNameTypeName="Child" />
    <AssociationType
        AssociationTypeID="4"
        AssociationTypeName="Derivation"
        ReverseNameTypeName="Derived From" />
  </AssociationTypes>
</response>
```

### AssociationType Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `AssociationTypeID` | int | Numeric ID of the association type. This is the value used in `AssociationTypeID` parameters of the `Associate*` APIs. |
| `AssociationTypeName` | string | Localised display name used when the current item is the **source** of the association (forward direction). |
| `ReverseNameTypeName` | string | Localised display name used when the current item is the **target** of the association (reverse direction, i.e. `IsReverseAssociation="TRUE"`). |

### Standard AssociationTypeID Values

| ID | Forward Name | Reverse Name | Description |
|----|-------------|--------------|-------------|
| `0` | Related | Related | General bidirectional relationship. |
| `1` | Rendition | Rendition Of | Target is an alternate format of the source. |
| `2` | Copy | Copy Of | Target is a copy of the source. |
| `3` | Parent | Child | Source is the parent; target is the child. |
| `4` | Derivation | Derived From | Target is derived from the source. |

> **Note:** The exact localised display names depend on the language configured for the authenticated user's session and may differ from the examples above.

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

---

## Required Permissions

Any authenticated user can call this API. No elevated permissions are required.

---

## Example

### GET Request

```
GET /srv.asmx/AssociationTypes
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociationTypes HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociationTypes>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:AssociationTypes>
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

Lists the kinds of link an association can be. There are five and there is no operation that adds
one.

```javascript
const root = await call('AssociationTypes', { authenticationTicket: ticket });

for (const type of root.querySelectorAll('AssociationType')) {
  console.log(type.getAttribute('AssociationTypeID'),
              type.getAttribute('AssociationTypeName'),      // how the near end reads it
              type.getAttribute('ReverseNameTypeName'));     // how the far end reads it
}
```

| `AssociationTypeID` | Near end | Far end |
|---:|---|---|
| `0` | Related | Related |
| `1` | Rendition | Rendition |
| `2` | Copy of | Original copy |
| `3` | Parent document | Child document |
| `4` | Derived from | Derivation of this document |

The two names are why an association has a direction: the same link reads one way from the item it
was made on and the other way from the item it points at.

## Notes

- **Localised names**: `AssociationTypeName` and `ReverseNameTypeName` are looked up from resource strings using the IDs stored in the `ASSOCIATIONTYPES` database table. The actual text returned depends on the language of the authenticated session.
- **Forward vs. reverse names**: Use `AssociationTypeName` to label an association when the queried item is the source (e.g. "This document is a **Rendition** of another"). Use `ReverseNameTypeName` when the queried item is the target -" i.e. when `IsReverseAssociation="TRUE"` in `AssociatedDocuments` or `AssociatedFoldersAndDocuments` results (e.g. "This document is a **Rendition Of** another").
- **Fixed type IDs**: The `AssociationTypeID` values (0-"4) correspond to the `enum_IR.AssociationTypes` enumeration and are fixed in the system. Only the display names are configurable via localisation.
- **Folder associations**: Folder associations always use type `0` (Related) regardless of `AssociationTypeID` supplied. Only document-to-document associations support all five types.
- **Ordered result**: Types are returned ordered by `AssociationTypeID` ascending.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association from a document to another document or folder
- [AssociateFolder](AssociateFolder.md) - Create an association from a folder to another document or folder
- [AssociatedDocuments](AssociatedDocuments.md) - Get the list of documents associated with a document or folder
- [AssociatedFolders](AssociatedFolders.md) - Get the list of folders associated with a document or folder
- [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md) - Get all associated items of a document or folder
- [RemoveAssociation](RemoveAssociation.md) - Remove an existing association between two items

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
