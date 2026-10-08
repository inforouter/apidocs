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
| `MYSQL_PortNumber` | string | Yes | TCP port number the MySQL server listens on, 1 to 65535. Anything else is refused `4000`. It cannot be left empty: the parameter is declared without a question mark, so model binding refuses an empty one with HTTP 400. Send `3306` for the default. |
| `MYSQL_UserName` | string | Yes | MySQL user account name used to connect. |
| `MYSQL_Password` | string | Yes | Password for the MySQL user account. |
| `MYSQL_DataBasename` | string | Yes | Name of the MySQL database to query. |
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

The MySQL form. `MYSQL_PortNumber` is a **string**, and a value that is not a port number from 1
to 65535 is refused `4000`. Until 9.0 it was silently replaced with `3306`, so a typo became a
working-looking configuration against the wrong port.

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

## Filtering the lookup and returning several columns

The SQL sentence can take what the user has typed, and can return more than one column. This is the
usual set-up for a type-ahead lookup: the user types a few letters, the client calls
[GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) with them as `OptionFilter`, and gets back
the matching rows with every column of the query.

### How to write the SQL

Write `<%=VALUE%>` where the typed text belongs. When the options are asked for, the server replaces
it with the `OptionFilter` value and runs the sentence.

```sql
SELECT state_code AS CODE,
       state_name AS NAME,
       region     AS REGION
FROM   states
WHERE  state_name LIKE '<%=VALUE%>%'
ORDER  BY state_name
LIMIT  50
```

| Rule | Why |
|------|-----|
| The placeholder is exactly `<%=VALUE%>`, in upper case. | It is matched as written; `<%=value%>` is left in the sentence as ordinary text, so the filter is not applied and nothing matches. |
| Always put it **inside a single-quoted string**: `'<%=VALUE%>%'`. | The text is pasted into the sentence, not sent as a query parameter. The server doubles any single quote in it, which keeps it inside the string and nowhere else. |
| It may appear more than once. | Every occurrence is replaced with the same text. |
| Limit the rows (`LIMIT 50` here). | An empty `OptionFilter` leaves `LIKE '%'`, which matches every row. |
| Give every column a name with `AS`, using letters, digits and underscores only. | Each column name becomes an attribute name on `<option>`. A name with a space in it is not a valid attribute name and the call fails with `4200`. |
| Give every column a different name. | Two columns with the same name end up as one attribute. |

A `%` or `_` typed by the user is not escaped, so it works as a `LIKE` wildcard. A sentence without the
placeholder ignores `OptionFilter` and always returns the same rows.

### Saving it

Send the call as a **POST**. In form data the sentence is URL-encoded like any other value: the
placeholder becomes `%3C%25%3DVALUE%25%3E` and the `%` after it becomes `%25`.

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForMYSQL HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ADDRESS&FieldName=STATE&MYSQL_ServerName=mysql.example.com&MYSQL_PortNumber=3306&MYSQL_UserName=ir_reader&MYSQL_Password=secret&MYSQL_DataBasename=refdata&sqlSentence=SELECT+state_code+AS+CODE%2C+state_name+AS+NAME%2C+region+AS+REGION+FROM+states+WHERE+state_name+LIKE+%27%3C%25%3DVALUE%25%3E%25%27+ORDER+BY+state_name+LIMIT+50
```

From JavaScript, `URLSearchParams` does the encoding:

```javascript
await fetch('/srv.asmx/SetPropertySetLookupFieldParametersForMYSQL', {
  method: 'POST',
  body: new URLSearchParams({
    authenticationTicket: ticket,
    PropertySetName: 'ADDRESS',
    FieldName: 'STATE',
    MYSQL_ServerName: 'mysql.example.com',
    MYSQL_PortNumber: '3306',
    MYSQL_UserName: 'ir_reader',
    MYSQL_Password: 'secret',
    MYSQL_DataBasename: 'refdata',
    sqlSentence: "SELECT state_code AS CODE, state_name AS NAME, region AS REGION FROM states WHERE state_name LIKE '<%=VALUE%>%' ORDER BY state_name LIMIT 50"
  })
});
```

Over SOAP the sentence travels inside XML, so the angle brackets of the placeholder must be escaped
as `&lt;` and `&gt;` (or the whole sentence wrapped in `<![CDATA[ ... ]]>`):

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetPropertySetLookupFieldParametersForMYSQL xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c</AuthenticationTicket>
      <PropertySetName>ADDRESS</PropertySetName>
      <FieldName>STATE</FieldName>
      <MYSQL_ServerName>mysql.example.com</MYSQL_ServerName>
      <MYSQL_PortNumber>3306</MYSQL_PortNumber>
      <MYSQL_UserName>ir_reader</MYSQL_UserName>
      <MYSQL_Password>secret</MYSQL_Password>
      <MYSQL_DataBasename>refdata</MYSQL_DataBasename>
      <sqlSentence>SELECT state_code AS CODE, state_name AS NAME, region AS REGION FROM states WHERE state_name LIKE '&lt;%=VALUE%&gt;%' ORDER BY state_name LIMIT 50</sqlSentence>
    </SetPropertySetLookupFieldParametersForMYSQL>
  </soap:Body>
</soap:Envelope>
```

[GetPropertySetDefinition](GetPropertySetDefinition.md) reads the sentence back the same way, escaped
because it is XML; the value itself is unchanged:

```xml
<lookupparams looktype="database">
  <dbconnectionparams dbtype="MYSQL" servername="mysql.example.com" portnumber="3306"
                      username="ir_reader" password="****" database="refdata" />
  <sqlsentence>SELECT state_code AS CODE, state_name AS NAME, region AS REGION FROM states WHERE state_name LIKE '&lt;%=VALUE%&gt;%' ORDER BY state_name LIMIT 50</sqlsentence>
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

MySQL keeps the case of an alias as written, so `AS Name` comes back as the attribute `Name`. Whether `LIKE` ignores case depends on the column's collation.

## Notes

- The target field **must have control type `LOOKUP`**. Calling this API on a field with any other control type (TEXT BOX, COMBO BOX, etc.) returns an error.
- Connection parameters (server name, port, credentials, database) and the SQL sentence are stored in a configuration XML file on the infoRouter server: `lookup_<propertySetId>_<FieldName>.xml`.
- **Passwords are stored encrypted**. They are never returned in plain text by read APIs such as [GetPropertySetDefinition](GetPropertySetDefinition.md) (shown as `****`).
- `MYSQL_PortNumber` must be a number from 1 to 65535. Send `3306` for the MySQL default; an empty value is refused by model binding before the operation runs.
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
