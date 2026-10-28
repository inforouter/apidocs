# Questions index

The questions customers, support and the UI developers ask, each pointing at the paragraph that answers it.
Add a question here whenever one is asked and answered; a question with no page yet is listed with *to come*.

## Tasks and workflows

- Can an ordinary user change a task's due date? → [Who may change a task's due date](tasks-due-date.md#who-passes)
- Can the assignee postpone a task? → [Who may change a task's due date](tasks-due-date.md#who-passes)
- Can the person who created a task change its due date? → [Who may change a task's due date](tasks-due-date.md#who-passes)
- Can an administrator change any task's due date? → [Who may change a task's due date](tasks-due-date.md#administrators)
- Who may reassign a task? → [Who may change a task's due date](tasks-due-date.md#reassigning-sets-a-due-date-too)

## Who may do what

- What can a User Manager do with users and groups? → [User Managers](../UserManagersRole.md)
- Who may change an administrator's account? → [Who may change an administrator's account](administrator-account.md)
- Can a User Manager make themselves a library manager? → [Who may change an administrator's account, the exceptions](administrator-account.md#who-passes-and-the-exceptions)
- Why does a library answer "not found" to an administrator who is not a member? → [Which libraries a caller can reach](libraries-reach.md)
- Can a hidden library be opened by name? → [Which libraries a caller can reach](libraries-reach.md#who-reaches-what)
- Why can the last member of a library not be removed? → [Which libraries a caller can reach, membership](libraries-reach.md#membership)
- Which logs can an Audit Manager read? → [Audit Managers](../AuditManagersRole.md)
- Can a Policy Manager change a library's policies? → [Policy Managers](../PolicyManagersRole.md)
- Can an R&D Manager reach a library they are not a member of? → [R&D Managers](../RDManagersRole.md)
- What can a library manager do in their library? → [Library Managers](../LibraryManagersRole.md)
- Can a library manager read the library's policies? → [GetDomainPolicies](../GetDomainPolicies.md)

## Documents

- Why did a Word letter made from a template come back blank after editing? → [Documents made from forms and templates](documents-from-forms.md#since)
- When is a document made from a form rendered again? → [Documents made from forms and templates](documents-from-forms.md#the-rule)
- Can a document be detached from its form later? → [Documents made from forms and templates](documents-from-forms.md#when-the-document-stops-being-a-form-document)
- What does copying a folder or document carry with it? → [Copy](../Copy.md) (*rules page to come*)

## WebDAV

- What happens when Word saves over WebDAV, and why does a rename keep the document's history? → [How WebDAV maps onto documents](webdav.md#what-office-does-when-it-saves)
- Why is a document locked in Word shown as checked out? → [How WebDAV maps onto documents](webdav.md#what-each-verb-does)
- Why does a WebDAV rename onto a locked document answer 423? → [How WebDAV maps onto documents, lock tokens](webdav.md#lock-tokens)
- Why do GET and PROPFIND give the same ETag? → [How WebDAV maps onto documents, ETags](webdav.md#etags)

## Libraries

- How do I make a library from a model library? → [A library made from a model library](library-from-template.md)
- What does a library made from a template copy, and what not? → [A library made from a model library](library-from-template.md#what-comes-across)
- Why are the access lists of a copied library rewritten? → [A library made from a model library, access lists](library-from-template.md#access-lists)
- Why does DeleteDomain say the library contains documents? → [Which libraries a caller can reach, deleting](libraries-reach.md#deleting-a-library)

## Retention and disposition

- Who may apply, remove or freeze a retention schedule? → [Who may change retention and disposition](retention-who-may.md#who-passes)
- Can an R&D Manager set a cut-off date without the right on the document? → [Who may change retention and disposition](retention-who-may.md#who-passes)
- Why does an R&D Manager not see a library? → [Who may change retention and disposition, reach](retention-who-may.md#reach-which-libraries-an-rd-manager-sees)
- How is a transfer-to-agency task completed? → [Who may change retention and disposition, transfer](retention-who-may.md#transfer-to-an-agency)

## Audit logs

- Who can read a document's SOX or ISO log? → [Which logs exist, and who reads each](audit-logs-who-reads.md#logs-about-items)
- Can an Audit Manager see who viewed a document? → [Which logs exist, and who reads each, logs about users](audit-logs-who-reads.md#logs-about-users)
- Can a library manager read the security changes of their library? → [Which logs exist, and who reads each](audit-logs-who-reads.md#logs-about-items)

## Conventions

- What do the errorCode numbers mean? → [How an answer is read](conventions.md#the-bands)
- What does errorCode 2070 mean? → [How an answer is read, MultiStatus](conventions.md#multistatus)
- Why does a call with no ticket answer 4030 and not 4010? → [How an answer is read, things that surprise](conventions.md#things-that-surprise)

## Connect

- How do I know whether a value Connect extracted has been reviewed? → [Values Connect extracted](connect-review-state.md#what-a-row-says)
- How do I list the documents with values still to review? → [Values Connect extracted, finding the documents](connect-review-state.md#finding-the-documents-still-to-review)
