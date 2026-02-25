# SetPropertySetLookupFieldParametersForORACLE API

Configures a `LOOKUP` field in a custom property set to query an external **Oracle** database. After calling this API the field will execute the specified SQL sentence against the Oracle server whenever [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) is called for it.

## Endpoint

```
/srv.asmx/SetPropertySetLookupFieldParametersForORACLE
```

## Methods

- **GET** `/srv.asmx/SetPropertySetLookupFieldParametersForORACLE?authenticationTicket=...&PropertySetName=...&FieldName=...&...`
- **POST** `/srv.asmx/SetPropertySetLookupFieldParametersForORACLE` (form data)
- **SOAP** Action: `http://tempuri.org/SetPropertySetLookupFieldParametersForORACLE`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set that owns the field. |
| `FieldName` | string | Yes | Internal name of the `LOOKUP` field to configure. |
| `ORACLE_ServiceName` | string | Yes | Oracle service name (TNS alias or Easy Connect string) used to identify the Oracle database instance. |
| `ORACLE_UserName` | string | Yes | Oracle user account name used to connect. |
| `ORACLE_Password` | string | Yes | Password for the Oracle user account. |
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
GET /srv.asmx/SetPropertySetLookupFieldParametersForORACLE
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=PROJECTMETA
    &FieldName=DEPARTMENT
    &ORACLE_ServiceName=ORCL
    &ORACLE_UserName=ir_reader
    &ORACLE_Password=secret
    &sqlSentence=SELECT+DEPT_CODE,DEPT_NAME+FROM+DEPARTMENTS+ORDER+BY+DEPT_NAME
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForORACLE HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=PROJECTMETA&FieldName=DEPARTMENT&ORACLE_ServiceName=ORCL&ORACLE_UserName=ir_reader&ORACLE_Password=secret&sqlSentence=SELECT+DEPT_CODE%2CDEPT_NAME+FROM+DEPARTMENTS+ORDER+BY+DEPT_NAME
```

## Notes

- The target field **must have control type `LOOKUP`**. Calling this API on a field with any other control type (TEXT BOX, COMBO BOX, etc.) returns an error.
- Connection parameters (service name, credentials) and the SQL sentence are stored in a configuration XML file on the infoRouter server: `lookup_<propertySetId>_<FieldName>.xml`.
- **Passwords are stored encrypted**. They are never returned in plain text by read APIs such as [GetPropertySetDefinition](GetPropertySetDefinition.md) (shown as `****`).
- Oracle connections use the **service name** (not a server host name or port number). The service name is the TNS alias or Easy Connect string configured in the Oracle listener.
- There is no separate `DatabaseName` parameter for Oracle -" the service name identifies both the host and database instance.
- To test the lookup configuration, call [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) after saving the parameters.
- To configure a LOOKUP field for MySQL, use [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md). For SQL Server, use [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md).

## Related APIs

- [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md) -" Configure a LOOKUP field to query MySQL.
- [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md) -" Configure a LOOKUP field to query SQL Server.
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
