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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| Field not found | No field with the specified `FieldName` exists in the property set. |
| Invalid field type | The specified field is not a `LOOKUP` control type. |
