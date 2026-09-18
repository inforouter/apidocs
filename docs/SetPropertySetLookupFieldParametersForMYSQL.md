# SetPropertySetLookupFieldParametersForMYSQL API

Configures a `LOOKUP` field in a custom property set to query an external **MySQL** database. After calling this API the field will execute the specified SQL sentence against the MySQL server whenever [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) is called for it.

## Endpoint

```
/srv.asmx/SetPropertySetLookupFieldParametersForMYSQL
```

## Methods

- **GET** `/srv.asmx/SetPropertySetLookupFieldParametersForMYSQL?authenticationTicket=...&PropertySetName=...&FieldName=...&...`
- **POST** `/srv.asmx/SetPropertySetLookupFieldParametersForMYSQL` (form data)
- **SOAP** Action: `http://tempuri.org/SetPropertySetLookupFieldParametersForMYSQL`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set that owns the field. |
| `FieldName` | string | Yes | Internal name of the `LOOKUP` field to configure. |
| `MYSQL_ServerName` | string | Yes | Hostname or IP address of the MySQL server. |
| `MYSQL_PortNumber` | string | Yes | TCP port number the MySQL server listens on. If empty or non-numeric, defaults to `3306`. |
| `MYSQL_UserName` | string | Yes | MySQL user account name used to connect. |
| `MYSQL_Password` | string | Yes | Password for the MySQL user account. |
| `MYSQL_DataBasename` | string | Yes | Name of the MySQL database to query. |
| `sqlSentence` | string | Yes | SQL `SELECT` statement to execute. May include a filter placeholder used by the `OptionFilter` parameter of `GetPropertySetFieldOptions`. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

**System Administrator** only. Non-admin callers receive an access denied error.

## Example

### GET Request

```
GET /srv.asmx/SetPropertySetLookupFieldParametersForMYSQL
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=PROJECTMETA
    &FieldName=CATEGORY
    &MYSQL_ServerName=db.example.com
    &MYSQL_PortNumber=3306
    &MYSQL_UserName=ir_reader
    &MYSQL_Password=secret
    &MYSQL_DataBasename=project_db
    &sqlSentence=SELECT+CategoryCode,CategoryName+FROM+categories+ORDER+BY+CategoryName
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForMYSQL HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=PROJECTMETA&FieldName=CATEGORY&MYSQL_ServerName=db.example.com&MYSQL_PortNumber=3306&MYSQL_UserName=ir_reader&MYSQL_Password=secret&MYSQL_DataBasename=project_db&sqlSentence=SELECT+CategoryCode%2CCategoryName+FROM+categories+ORDER+BY+CategoryName
```

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

The MySQL form. `MYSQL_PortNumber` is a **string**: a value that is not a number is replaced with
`3306` rather than refused.

```javascript
await call('SetPropertySetLookupFieldParametersForMYSQL', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  FieldName: 'SUPPLIER',
  MYSQL_ServerName: 'mysqlbox',
  MYSQL_PortNumber: '3307',
  MYSQL_UserName: 'reader',
  MYSQL_Password: 'secret',
  MYSQL_DataBasename: 'vendors',
  sqlSentence: 'SELECT NAME FROM SUPPLIERS ORDER BY NAME'
});
```

Read back, the database name is under `database` where the SQL Server form puts it under
`databasename`:

```xml
<dbconnectionparams dbtype="MYSQL" servername="mysqlbox" portnumber="3307"
                    username="reader" password="****" database="vendors" />
```

The connection is never tested at save time, and the three setters overwrite one another.

## Notes

- The target field **must have control type `LOOKUP`**. Calling this API on a field with any other control type (TEXT BOX, COMBO BOX, etc.) returns an error.
- Connection parameters (server name, port, credentials, database) and the SQL sentence are stored in a configuration XML file on the infoRouter server: `lookup_<propertySetId>_<FieldName>.xml`.
- **Passwords are stored encrypted**. They are never returned in plain text by read APIs such as [GetPropertySetDefinition](GetPropertySetDefinition.md) (shown as `****`).
- If `MYSQL_PortNumber` is empty or cannot be parsed as a number, the port defaults to `3306`.
- To test the lookup configuration, call [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) after saving the parameters.
- To configure a LOOKUP field for SQL Server, use [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md). For Oracle, use [SetPropertySetLookupFieldParametersForORACLE](SetPropertySetLookupFieldParametersForORACLE.md).

## Related APIs

- [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md) -" Configure a LOOKUP field to query SQL Server.
- [SetPropertySetLookupFieldParametersForORACLE](SetPropertySetLookupFieldParametersForORACLE.md) -" Configure a LOOKUP field to query Oracle.
- [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) -" Execute the lookup query and return results.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full property set definition including field metadata.
- [AddPropertySetField](AddPropertySetField.md) -" Add a new field to a property set.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no set by that name, or the set has no such field |
| `4200` | the caller is not a system administrator - the message says so, the code does not |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
