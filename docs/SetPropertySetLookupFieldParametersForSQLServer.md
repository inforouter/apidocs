# SetPropertySetLookupFieldParametersForSQLServer API

Configures a `LOOKUP` field in a custom property set to query an external **SQL Server** database. After calling this API the field will execute the specified SQL sentence against the SQL Server instance whenever [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) is called for it.

## Endpoint

```
/srv.asmx/SetPropertySetLookupFieldParametersForSQLServer
```

## Methods

- **GET** `/srv.asmx/SetPropertySetLookupFieldParametersForSQLServer?authenticationTicket=...&PropertySetName=...&FieldName=...&...`
- **POST** `/srv.asmx/SetPropertySetLookupFieldParametersForSQLServer` (form data)
- **SOAP** Action: `http://tempuri.org/SetPropertySetLookupFieldParametersForSQLServer`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set that owns the field. |
| `FieldName` | string | Yes | Internal name of the `LOOKUP` field to configure. |
| `SQLSERVER_ServerName` | string | Yes | Hostname or IP address (and optional instance name, e.g. `server\INSTANCE`) of the SQL Server. |
| `SQLSERVER_UserName` | string | Yes | SQL Server login name used to connect. |
| `SQLSERVER_Password` | string | Yes | Password for the SQL Server login. |
| `SQLSERVER_DataBasename` | string | Yes | Name of the SQL Server database to query. |
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
GET /srv.asmx/SetPropertySetLookupFieldParametersForSQLServer
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=PROJECTMETA
    &FieldName=CATEGORY
    &SQLSERVER_ServerName=dbserver.example.com
    &SQLSERVER_UserName=ir_reader
    &SQLSERVER_Password=secret
    &SQLSERVER_DataBasename=project_db
    &sqlSentence=SELECT+CategoryCode,CategoryName+FROM+dbo.Categories+ORDER+BY+CategoryName
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForSQLServer HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=PROJECTMETA&FieldName=CATEGORY&SQLSERVER_ServerName=dbserver.example.com&SQLSERVER_UserName=ir_reader&SQLSERVER_Password=secret&SQLSERVER_DataBasename=project_db&sqlSentence=SELECT+CategoryCode%2CCategoryName+FROM+dbo.Categories+ORDER+BY+CategoryName
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

Points a field at a SQL Server query. The parameters are written to
`config/lookup_<propertySetId>_<FIELDNAME>.xml` and **the connection is never tested**, so a server
that does not exist and a sentence that is not SQL are both accepted.

```javascript
await call('SetPropertySetLookupFieldParametersForSQLServer', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  FieldName: 'SUPPLIER',
  SQLSERVER_ServerName: 'sqlbox',
  SQLSERVER_UserName: 'reader',
  SQLSERVER_Password: 'secret',
  SQLSERVER_DataBasename: 'Vendors',
  sqlSentence: 'SELECT NAME FROM SUPPLIERS ORDER BY NAME'
});
```

`GetPropertySetDefinition` reads them back with the password masked as `****`:

```xml
<lookupparams looktype="database">
  <dbconnectionparams dbtype="SQLSERVER" servername="sqlbox" username="reader"
                      password="****" databasename="Vendors" />
  <sqlsentence>SELECT NAME FROM SUPPLIERS ORDER BY NAME</sqlsentence>
</lookupparams>
```

The three setters overwrite one another - a field has one set of lookup parameters and the last call
wins. The control type is not checked either: a `TEXT BOX` accepts parameters, and then nothing ever
reads them, because the definition only reports `<lookupparams>` for a field whose control type is
`LOOKUP`.

## Notes

- The target field **must have control type `LOOKUP`**. Calling this API on a field with any other control type (TEXT BOX, COMBO BOX, etc.) returns an error.
- Connection parameters (server name, credentials, database) and the SQL sentence are stored in a configuration XML file on the infoRouter server: `lookup_<propertySetId>_<FieldName>.xml`.
- **Passwords are stored encrypted**. They are never returned in plain text by read APIs such as [GetPropertySetDefinition](GetPropertySetDefinition.md) (shown as `****`).
- The `SQLSERVER_ServerName` parameter accepts SQL Server instance notation: e.g. `myserver\SQLEXPRESS` for named instances.
- There is no port number parameter for SQL Server -" the default SQL Server port (1433) is used, or the port is resolved via SQL Browser for named instances.
- To test the lookup configuration, call [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) after saving the parameters.
- To configure a LOOKUP field for MySQL, use [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md). For Oracle, use [SetPropertySetLookupFieldParametersForORACLE](SetPropertySetLookupFieldParametersForORACLE.md).

## Related APIs

- [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md) -" Configure a LOOKUP field to query MySQL.
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
