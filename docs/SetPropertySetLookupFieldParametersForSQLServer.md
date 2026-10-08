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
| `sqlSentence` | string | Yes | SQL `SELECT` statement to execute. May contain the placeholder `<%=VALUE%>`, which is replaced with the `OptionFilter` value of `GetPropertySetFieldOptions`, and may return several columns. See [Filtering the lookup and returning several columns](#filtering-the-lookup-and-returning-several-columns). |

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
wins. The control type **is** checked: a field that is not a `LOOKUP` is refused `4000`. Until 9.0 a
`TEXT BOX` accepted parameters and a file was written for it, and then nothing ever read them,
because the definition only reports `<lookupparams>` for a field whose control type is `LOOKUP`.

## Filtering the lookup and returning several columns

The SQL sentence can take what the user has typed, and can return more than one column. This is the
usual set-up for a type-ahead lookup: the user types a few letters, the client calls
[GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) with them as `OptionFilter`, and gets back
the matching rows with every column of the query.

### How to write the SQL

Write `<%=VALUE%>` where the typed text belongs. When the options are asked for, the server replaces
it with the `OptionFilter` value and runs the sentence.

```sql
SELECT TOP 50
       StateCode AS CODE,
       StateName AS NAME,
       Region    AS REGION
FROM   dbo.States
WHERE  StateName LIKE '<%=VALUE%>%'
ORDER  BY StateName
```

| Rule | Why |
|------|-----|
| The placeholder is exactly `<%=VALUE%>`, in upper case. | It is matched as written; `<%=value%>` is left in the sentence as ordinary text, so the filter is not applied and nothing matches. |
| Always put it **inside a single-quoted string**: `'<%=VALUE%>%'`. | The text is pasted into the sentence, not sent as a query parameter. The server doubles any single quote in it, which keeps it inside the string and nowhere else. |
| It may appear more than once. | Every occurrence is replaced with the same text. |
| Limit the rows (`TOP 50` here). | An empty `OptionFilter` leaves `LIKE '%'`, which matches every row. |
| Give every column a name with `AS`, using letters, digits and underscores only. | Each column name becomes an attribute name on `<option>`. A name with a space in it is not a valid attribute name and the call fails with `4200`. |
| Give every column a different name. | Two columns with the same name end up as one attribute. |

A `%` or `_` typed by the user is not escaped, so it works as a `LIKE` wildcard. A sentence without the
placeholder ignores `OptionFilter` and always returns the same rows.

### Saving it

Send the call as a **POST**. In form data the sentence is URL-encoded like any other value: the
placeholder becomes `%3C%25%3DVALUE%25%3E` and the `%` after it becomes `%25`.

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForSQLServer HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ADDRESS&FieldName=STATE&SQLSERVER_ServerName=dbserver.example.com&SQLSERVER_UserName=ir_reader&SQLSERVER_Password=secret&SQLSERVER_DataBasename=RefData&sqlSentence=SELECT+TOP+50+StateCode+AS+CODE%2C+StateName+AS+NAME%2C+Region+AS+REGION+FROM+dbo.States+WHERE+StateName+LIKE+%27%3C%25%3DVALUE%25%3E%25%27+ORDER+BY+StateName
```

From JavaScript, `URLSearchParams` does the encoding:

```javascript
await fetch('/srv.asmx/SetPropertySetLookupFieldParametersForSQLServer', {
  method: 'POST',
  body: new URLSearchParams({
    authenticationTicket: ticket,
    PropertySetName: 'ADDRESS',
    FieldName: 'STATE',
    SQLSERVER_ServerName: 'dbserver.example.com',
    SQLSERVER_UserName: 'ir_reader',
    SQLSERVER_Password: 'secret',
    SQLSERVER_DataBasename: 'RefData',
    sqlSentence: "SELECT TOP 50 StateCode AS CODE, StateName AS NAME, Region AS REGION FROM dbo.States WHERE StateName LIKE '<%=VALUE%>%' ORDER BY StateName"
  })
});
```

Over SOAP the sentence travels inside XML, so the angle brackets of the placeholder must be escaped
as `&lt;` and `&gt;` (or the whole sentence wrapped in `<![CDATA[ ... ]]>`):

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetPropertySetLookupFieldParametersForSQLServer xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c</AuthenticationTicket>
      <PropertySetName>ADDRESS</PropertySetName>
      <FieldName>STATE</FieldName>
      <SQLSERVER_ServerName>dbserver.example.com</SQLSERVER_ServerName>
      <SQLSERVER_UserName>ir_reader</SQLSERVER_UserName>
      <SQLSERVER_Password>secret</SQLSERVER_Password>
      <SQLSERVER_DataBasename>RefData</SQLSERVER_DataBasename>
      <sqlSentence>SELECT TOP 50 StateCode AS CODE, StateName AS NAME, Region AS REGION FROM dbo.States WHERE StateName LIKE '&lt;%=VALUE%&gt;%' ORDER BY StateName</sqlSentence>
    </SetPropertySetLookupFieldParametersForSQLServer>
  </soap:Body>
</soap:Envelope>
```

[GetPropertySetDefinition](GetPropertySetDefinition.md) reads the sentence back the same way, escaped
because it is XML; the value itself is unchanged:

```xml
<lookupparams looktype="database">
  <dbconnectionparams dbtype="SQLSERVER" servername="dbserver.example.com" username="ir_reader"
                      password="****" databasename="RefData" />
  <sqlsentence>SELECT TOP 50 StateCode AS CODE, StateName AS NAME, Region AS REGION FROM dbo.States WHERE StateName LIKE '&lt;%=VALUE%&gt;%' ORDER BY StateName</sqlsentence>
</lookupparams>
```

### Asking for the filtered options

```
GET /srv.asmx/GetPropertySetFieldOptions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ADDRESS
    &PropertyFieldName=STATE
    &OptionFilter=Te
HTTP/1.1
Host: yourserver
```

With `OptionFilter=Te` the condition that runs is `LIKE 'Te%'`. Each row is one `<option>`, and each
column of the query is an attribute named after it:

```xml
<response success="true" error="">
  <options>
    <option CODE="TN" NAME="Tennessee" REGION="South" />
    <option CODE="TX" NAME="Texas" REGION="South" />
  </options>
</response>
```

| `OptionFilter` | Condition that runs | Result |
|----------------|---------------------|--------|
| `Te` | `LIKE 'Te%'` | the rows whose name starts with "Te" |
| *(empty)* | `LIKE '%'` | every row, up to the limit in the sentence |
| `O'B` | `LIKE 'O''B%'` | the quote is doubled, so "O'Brien" is searched for |

The server returns every column and attaches no meaning to them: which attribute is stored as the
field's value and which are only shown is decided by the client. A column that is null in the database
comes back as an empty attribute.

SQL Server keeps the case of an alias as written, so `AS Name` comes back as the attribute `Name`. Whether `LIKE` ignores case depends on the column's collation.

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
