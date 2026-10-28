# CreateDomainFromTemplate API

Creates a library from another one used as a template: the template's policies and rules, members, managers and local groups, the root folder's own settings and access list, the folder tree with each folder's settings and list, and the documents, under a new name. The answer is the new library.

## Why this operation exists

A law firm opening a case, or a team starting a project, does not want an empty library. They keep a **model library** they never work in: the folder structure every case needs, the access lists that say which team sees what, the standard forms and reference documents, the retention-free skeleton. When a new case starts, the library for it is made from the model and the staff find everything in its place from the first day.

infoRouter 8.7 had this on the control panel's *New library* page, as *Use another library as a template*. The 9.0 control panel and the web service API had only `CreateDomain`, which makes an empty library, and the folders, documents, members and lists had to be rebuilt by hand or by a script of a hundred calls. This operation is the one call that does it.

It also does more than the 8.7 page did. That page copied the policies, the folders and the documents and nothing else: the new library had one member, the creator, and an access list naming one of the model's own groups kept the group's id, which means nothing in another library, so the rights granted through it silently stopped working. This operation copies the members, managers and local groups too, and writes any list that names a local group again for the new library's copy of that group.

## Endpoint

```
/srv.asmx/CreateDomainFromTemplate
```

## Methods

- **GET** `/srv.asmx/CreateDomainFromTemplate?authenticationTicket=...&TemplateDomainName=...&DomainName=...&Anonymous=...&Hidden=...&WelcomeMessage=...&IncludeMembers=...&IncludeDocuments=...`
- **POST** `/srv.asmx/CreateDomainFromTemplate` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDomainFromTemplate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `TemplateDomainName` | string | Yes | The library to copy: its name, or `~L` followed by its id. |
| `DomainName` | string | Yes | Name of the new library. The rules of `CreateDomain`: unique (`4090`), at most 128 characters, no special characters (`4000`). |
| `Anonymous` | bool | No | Allows anonymous access to the new library. Left out: the template's setting. |
| `Hidden` | bool | No | Hides the new library from the library list. Left out: the template's setting. |
| `WelcomeMessage` | string | No | Welcome message of the new library. Left out: the template's message. Sent empty: no message. |
| `IncludeMembers` | bool | No | Default `true`: the members, managers and local user groups come across. `false`: the caller is the only member and manager, no local group is made, and the entries of the template's local groups are dropped from the lists. |
| `IncludeDocuments` | bool | No | Default `true`. `false` copies the folder tree, with every folder's settings and access list, and no document: a skeleton. |

The parameter names follow `CreateDomain`, so a form that makes a library can make one from a template with two fields more.

## Response

### Success Response

The new library, as `GetDomain` returns it:

```xml
<response success="true" error="">
  <domain DomainID="1427" DomainName="Case 2026-0142" AnonymousDomain="FALSE" IsArchive="FALSE" IsHidden="TRUE" WelcomeMessage="Welcome to the case library" />
</response>
```

### Multi-status Response

The library was made, but at least one item of the template could not be copied. The answer is `success="false"` with `errorCode="2070"`, the `<domain>` element names the library that exists, and one `<log>` entry says what was refused and why. Everything not in the log was copied.

```xml
<response success="false" error="MultiStatus" errorCode="2070">
  <domain DomainID="1427" DomainName="Case 2026-0142" AnonymousDomain="FALSE" IsArchive="FALSE" IsHidden="TRUE" WelcomeMessage="Welcome to the case library" />
  <log><item>readme.htm</item><error>Document is offline.</error></log>
</response>
```

The library is kept, as the 8.7 page kept it, because a model with one document that happens to be offline is not a reason to make nothing. The caller decides: keep the library and add the missing item by hand, or [DeleteDomain](DeleteDomain.md) it and try again.

### Error Response

Nothing was made:

```xml
<response success="false" error="Library not found" errorCode="4041" />
```

## Required Permissions

**System administrator only**, as `CreateDomain`. The right is asked before the template is looked up, so a caller without it learns nothing about which libraries exist.

The copy runs as the caller: the new folders and documents are created, owned and registered by the caller with today's date, as a hand-made copy would be. The caller is a member and a manager of the new library whatever `IncludeMembers` says - a library must keep a member, or nobody could reach it.

## What is copied, and what is not

### Copied

| Item | Notes |
|------|-------|
| Library settings | `Anonymous` and `Hidden` unless sent; the welcome message unless sent; the library rules shown by [GetDomainPolicies](GetDomainPolicies.md) (hide incomplete / unapproved / expired / unpublished, publishing requirements, drag and drop). |
| Policies | Every action policy of [GetDomainPolicies](GetDomainPolicies.md), as the template has it. |
| Property sets listed on the library | The sets a non-public property set definition is made available to; the copied rows need them. |
| Members | Every user and global user group that is a member of the template. `IncludeMembers` only. |
| Managers | Every manager of the template. `IncludeMembers` only. |
| Local user groups | Each group local to the template is made again in the new library, with the same name and the same members. It is a new group with a new id. `IncludeMembers` only. |
| The root folder's settings | Folder rules (disallow new folders, deletions, check-outs...), default and mandatory view, auto-prompt property set, description, classification, file type restrictions, infoRouter Connect preferences, applied property sets, notification subscriptions. |
| The root folder's access list | The template root's own list. Until this operation a new library's root had "everyone may list"; see below for lists naming a local group. |
| The folder tree | Every folder, with its rules, description, classification, file type restrictions, Connect preferences, subscriptions, property set rows and access list, as [Copy](Copy.md) copies a folder. |
| Documents | Every document of every folder and of the root, with all of its versions and files, keywords, description, publishing rules, property set rows and access list, as [Copy](Copy.md) copies a document. `IncludeDocuments` only. |
| Security history | The whole copy is one entry on the new library's root in [GetSecurityChangeLog](GetSecurityChangeLog.md), counting the folders and documents it made, after the entry for the list the library was born with. |

### Not copied

| Item | Why |
|------|-----|
| Retention and disposition schedules, cut-off dates, freezes | A copied folder or document is a new one; a new case gets its own schedule. [Copy](Copy.md) never carries them either. |
| Workflow definitions bound to the template's folders | A workflow definition is an object of its own, with steps, assignees and task definitions. Copying it is a separate operation, not part of this one. |
| Local users of the template | A local user belongs to one library. Such a user is not made again, and is left out of the member list, the managers and the local groups of the new library. |
| Checkouts, tasks, favorites, downloads, associations, saved searches, portals | Working state of the template, not part of a model. |
| The archive flag | The new library is always online, whether the template is archived or not. An archived library is a good template: nobody can change it. |

### Access lists that name a local group

Access lists are shared between the template and the copy, as they are between a folder and its copy: a list is never changed in place, every change makes a new one, so sharing is safe and changing the copy's list later leaves the template's alone.

The one list that cannot be shared is one naming a group **local to the template**. In the new library that group does not count - the permission check only honours the library's own groups and the global groups that are members of it - so the entry would show in the list and grant nothing. Every such list the new library holds is written again for it, with the new library's copy of the group in the old one's place; with `IncludeMembers=false`, where no group was made, the entry is dropped. Lists naming only users, global groups and everyone stay as they are.

## Example

### Make the library for a new case (GET)

```
GET /srv.asmx/CreateDomainFromTemplate?authenticationTicket=abc123-def456&TemplateDomainName=Model+Case&DomainName=Case+2026-0142&WelcomeMessage=Case+2026-0142+Smith+v.+Jones HTTP/1.1
```

### A skeleton with nobody in it (POST)

```
POST /srv.asmx/CreateDomainFromTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&TemplateDomainName=Model+Case&DomainName=Case+2026-0143&IncludeMembers=false&IncludeDocuments=false
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateDomainFromTemplate"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateDomainFromTemplate xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <TemplateDomainName>Model Case</TemplateDomainName>
      <DomainName>Case 2026-0142</DomainName>
      <Hidden>false</Hidden>
      <WelcomeMessage>Case 2026-0142 Smith v. Jones</WelcomeMessage>
      <IncludeMembers>true</IncludeMembers>
      <IncludeDocuments>true</IncludeDocuments>
    </CreateDomainFromTemplate>
  </soap:Body>
</soap:Envelope>
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

Makes the library and reads its id from the answer.

```javascript
const made = await call('CreateDomainFromTemplate', {
  authenticationTicket: ticket,
  TemplateDomainName: 'Model Case',
  DomainName: 'Case 2026-0142',
  WelcomeMessage: 'Case 2026-0142 Smith v. Jones'
});
const libraryId = made.querySelector('domain').getAttribute('DomainID');
```

**MultiStatus is not a failure to branch away from.** With `errorCode="2070"` the library exists; read `<domain>` for it and the `<log>` entries for what was left out. A caller that wants all or nothing deletes the library when the log is not empty:

```javascript
const response = await fetch(`/srv.asmx/CreateDomainFromTemplate?${new URLSearchParams({
  authenticationTicket: ticket, TemplateDomainName: 'Model Case', DomainName: 'Case 2026-0142'
})}`);
const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

if (root.getAttribute('errorCode') === '2070') {
  const refused = [...root.querySelectorAll('log')].map(l => l.querySelector('item').textContent);
  await call('DeleteDomain', { authenticationTicket: ticket, DomainName: 'Case 2026-0142' });
  throw new Error(`not copied: ${refused.join(', ')}`);
}
```

## Notes

- **The library itself is one transaction; the tree is not.** The library row, rules, policies, members, groups, managers and the root's settings and list are made together or not at all. The folders and documents are copied one by one, each its own transaction as `Copy` works, so a large model does not hold the database for the whole copy and one refused item does not undo the rest. That is what makes `2070` possible, and why the library stays when it happens.
- **Documents are copied in the request**, with every version and its files. A model library is meant to be small - forms, templates, a few reference documents - and the copy takes as long as copying those with `Copy` would. There is no size limit.
- **A saved template is still a template.** Nothing marks a library as a model; any library can be the template, including an archived one. Keep the model out of the daily work and it stays a model.
- **Calling it twice makes two libraries**, as long as the names differ. The template is read, never written: its members, lists, folders and documents are what they were.
- Subscriptions and access list entries of the template's users and global groups keep working in the new library, because those are the same users and groups. The template's local groups are the ones made again.

The rule in plain words: [A library made from a model library](rules/library-from-template.md).

## Related APIs

- [CreateDomain](CreateDomain.md) - Make an empty library
- [DeleteDomain](DeleteDomain.md) - The undo of a copy that answered `2070`
- [Copy](Copy.md) - What copying a folder or a document carries, which this operation does per item
- [GetDomainPolicies](GetDomainPolicies.md) - The rules and policies that come across
- [GetDomainMembers](GetDomainMembers.md), [GetManagers](GetManagers.md), [GetDomainGroups](GetDomainGroups.md) - Who came across
- [GetAccessList](GetAccessList.md) - The lists, with the new library's groups in them
- [GetSecurityChangeLog](GetSecurityChangeLog.md) - The copy as one security change on the new root

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown. With no ticket at all the call runs as the anonymous user and is refused the right, `4030` |
| `4030` | the caller is not a system administrator; asked before the template is looked up |
| `4041` | no library of the template name, or `~L` with an id that is not a library |
| `4000` | `DomainName` carries a character a library name may not, or the template is a user recycle bin library |
| `4090` | a library named `DomainName` already exists |
| `6000` | the licensed library count is reached |
| `2070` | the library was made but at least one item was refused; read the `<log>` entries |
| `HTTP 400` | `TemplateDomainName` or `DomainName` was empty; refused by model binding, so there is no error document |
