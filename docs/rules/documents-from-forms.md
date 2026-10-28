# Documents made from forms and templates

A document can be made by filling an HTML form, with or without a Word or PDF template behind it. The document
remembers the form it came from. This page says what that link does, when the document is rendered again, and
when it stops being a form document.

## The rule

A document made with [SaveFilledForm](../SaveFilledForm.md) keeps a **link to its form template**. The link
means two things: [EditFilledForm](../EditFilledForm.md) can open the form again with the stored values, and
submitting the form again through SaveFilledForm renders a **new version** from the template with the new
values. Nothing else re-renders it. A new version that arrives as a **file** - a save from Word over WebDAV, an
upload, a check-in from the apps, the import tool - is stored as sent, and the link stays.

## What is rendered

| The form says | The document is |
|---|---|
| No `render-with` | The form's HTML with the values filled in, a `.htm` document |
| `render-with` a `.docx` | The Word template with its `{{placeholders}}` filled from the values, a `.docx` document |
| `render-with` a `.pdf` | The PDF form with its fields filled, a `.pdf` document |
| `templatePath=999` | A blank page with the values, for a form with no template of its own |

A placeholder the form does not supply is left blank. Names are matched without regard to case.

## When the document stops being a form document

Pass `detachDocumentFromTemplate=true` to SaveFilledForm and the document is rendered as usual, then left an
**ordinary document**: the link and the dynamic-content flag are removed in the same save. EditFilledForm then
refuses it, and it is subject to the library's maximum document size on later versions, from which form
documents are exempt. The form data stays with the version as history. There is no operation to detach a
document later; make the choice at save time. A copy of a linked document is linked too.

## What a new version by file does

Nothing to the link, and nothing to the file: it is stored as the user sent it. A letter made from the Word
letterhead, opened in Word, edited and saved is the edited letter.

## What the server answers

| Situation | Answer |
|---|---|
| The template document cannot be found or is offline | `4041` / `4230` |
| A Word or PDF template that cannot be filled (a block opened and never closed, a broken form) | `5000` naming `WordFunctions.FillWordTemplate` or the PDF function; nothing is created |
| EditFilledForm on a detached or plain document | `4000`, not a filled form |

## For developers

- Operations: [SaveFilledForm](../SaveFilledForm.md), [EditFilledForm](../EditFilledForm.md),
  [UploadDocument](../UploadDocument.md) and its variants, WebDAV PUT.
- The rule: `DocumentPublishOperation.RunAsync` (`IRNET/Operations/Document/DocumentPublishOperation.cs`):
  the template branch runs only when the new version carries form data and no file. Rendering:
  `ContentMan`, `WordFunctions.FillWordTemplate`, `PdfFunctions.FillPdfForm`.
- Tests: `SaveFilledFormWordTemplateApiTests` (including the upload of an edited letter over a rendered one),
  `FieldFormTemplateApiTests`, `DocumentBatch5ApiTests`.

## Since

- **9.0.200 (2026-10-28):** a new version by file is stored as sent. Until then every new version of a linked
  document was rendered again from the template with whatever form data came along, which for a file is none:
  a Word letter saved from Word came back as the template with empty fields. 8.7 had the same rule, but only
  HTML and PDF templates, so it was rarely met.
- **9.0:** Word (`.docx`) templates are filled like PDF ones; `detachDocumentFromTemplate` added.
