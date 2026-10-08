# SetPropertySetLookupFieldParametersForORACLE API

Intended to configure a `LOOKUP` field in a custom property set to query an external
**Oracle** database, so that the field executes the specified SQL sentence whenever
[GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) is called for it.

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

```javascript
await call('SetPropertySetLookupFieldParametersForORACLE', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  FieldName: 'SUPPLIER',
  ORACLE_ServiceName: 'ORCL',
  ORACLE_UserName: 'reader',
  ORACLE_Password: 'secret',
  sqlSentence: 'SELECT NAME FROM SUPPLIERS ORDER BY NAME'
});
```

What `GetPropertySetDefinition` reports afterwards - note `dbtype`, `servername` and the empty
`databasename`:

```xml
<dbconnectionparams dbtype="SQLSERVER" servername="ORCL" username="reader"
                    password="****" databasename="" />
```

The call itself answers `success="true"`, so nothing tells the caller. The connection is never
tested at save time either.

## Filtering the lookup and returning several columns

The SQL sentence can take what the user has typed, and can return more than one column. This is the
usual set-up for a type-ahead lookup: the user types a few letters, the client calls
[GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) with them as `OptionFilter`, and gets back
the matching rows with every column of the query.

### How to write the SQL

Write `<%=VALUE%>` where the typed text belongs. When the options are asked for, the server replaces
it with the `OptionFilter` value and runs the sentence.

```sql
SELECT STATE_CODE AS CODE,
       STATE_NAME AS NAME,
       REGION     AS REGION
FROM   STATES
WHERE  STATE_NAME LIKE '<%=VALUE%>%'
ORDER  BY STATE_NAME
FETCH  FIRST 50 ROWS ONLY
```

| Rule | Why |
|------|-----|
| The placeholder is exactly `<%=VALUE%>`, in upper case. | It is matched as written; `<%=value%>` is left in the sentence as ordinary text, so the filter is not applied and nothing matches. |
| Always put it **inside a single-quoted string**: `'<%=VALUE%>%'`. | The text is pasted into the sentence, not sent as a query parameter. The server doubles any single quote in it, which keeps it inside the string and nowhere else. |
| It may appear more than once. | Every occurrence is replaced with the same text. |
| Limit the rows (`FETCH FIRST 50 ROWS ONLY` here, Oracle 12c and later). | An empty `OptionFilter` leaves `LIKE '%'`, which matches every row. |
| Give every column a name with `AS`, using letters, digits and underscores only. | Each column name becomes an attribute name on `<option>`. A name with a space in it is not a valid attribute name and the call fails with `4200`. |
| Give every column a different name. | Two columns with the same name end up as one attribute. |

A `%` or `_` typed by the user is not escaped, so it works as a `LIKE` wildcard. A sentence without the
placeholder ignores `OptionFilter` and always returns the same rows.

### Saving it

Send the call as a **POST**. In form data the sentence is URL-encoded like any other value: the
placeholder becomes `%3C%25%3DVALUE%25%3E` and the `%` after it becomes `%25`.

```
POST /srv.asmx/SetPropertySetLookupFieldParametersForORACLE HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ADDRESS&FieldName=STATE&ORACLE_ServiceName=ORCL&ORACLE_UserName=ir_reader&ORACLE_Password=secret&sqlSentence=SELECT+STATE_CODE+AS+CODE%2C+STATE_NAME+AS+NAME%2C+REGION+AS+REGION+FROM+STATES+WHERE+STATE_NAME+LIKE+%27%3C%25%3DVALUE%25%3E%25%27+ORDER+BY+STATE_NAME+FETCH+FIRST+50+ROWS+ONLY
```

From JavaScript, `URLSearchParams` does the encoding:

```javascript
await fetch('/srv.asmx/SetPropertySetLookupFieldParametersForORACLE', {
  method: 'POST',
  body: new URLSearchParams({
    authenticationTicket: ticket,
    PropertySetName: 'ADDRESS',
    FieldName: 'STATE',
    ORACLE_ServiceName: 'ORCL',
    ORACLE_UserName: 'ir_reader',
    ORACLE_Password: 'secret',
    sqlSentence: "SELECT STATE_CODE AS CODE, STATE_NAME AS NAME, REGION AS REGION FROM STATES WHERE STATE_NAME LIKE '<%=VALUE%>%' ORDER BY STATE_NAME FETCH FIRST 50 ROWS ONLY"
  })
});
```

Over SOAP the sentence travels inside XML, so the angle brackets of the placeholder must be escaped
as `&lt;` and `&gt;` (or the whole sentence wrapped in `<![CDATA[ ... ]]>`):

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetPropertySetLookupFieldParametersForORACLE xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c</AuthenticationTicket>
      <PropertySetName>ADDRESS</PropertySetName>
      <FieldName>STATE</FieldName>
      <ORACLE_ServiceName>ORCL</ORACLE_ServiceName>
      <ORACLE_UserName>ir_reader</ORACLE_UserName>
      <ORACLE_Password>secret</ORACLE_Password>
      <sqlSentence>SELECT STATE_CODE AS CODE, STATE_NAME AS NAME, REGION AS REGION FROM STATES WHERE STATE_NAME LIKE '&lt;%=VALUE%&gt;%' ORDER BY STATE_NAME FETCH FIRST 50 ROWS ONLY</sqlSentence>
    </SetPropertySetLookupFieldParametersForORACLE>
  </soap:Body>
</soap:Envelope>
```

[GetPropertySetDefinition](GetPropertySetDefinition.md) reads the sentence back the same way, escaped
because it is XML; the value itself is unchanged:

```xml
<lookupparams looktype="database">
  <dbconnectionparams ... password="****" />
  <sqlsentence>SELECT STATE_CODE AS CODE, STATE_NAME AS NAME, REGION AS REGION FROM STATES WHERE STATE_NAME LIKE '&lt;%=VALUE%&gt;%' ORDER BY STATE_NAME FETCH FIRST 50 ROWS ONLY</sqlsentence>
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

Oracle returns the name of an unquoted column or alias in upper case, so `AS Name` comes back as the attribute `NAME`. Do not end the sentence with a semicolon. `LIKE` is case-sensitive in Oracle; to ignore case write `WHERE UPPER(STATE_NAME) LIKE UPPER('<%=VALUE%>%')`.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no set by that name, or the set has no such field |
| `4200` | the caller is not a system administrator - the message says so, the code does not |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
