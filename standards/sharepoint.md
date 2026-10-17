# SharePoint Delivery Standard

## Lists

- Define business entity, columns, data types, required/default values, validation, relationships, and ownership.
- Document expected volume, indexes, views, threshold behavior, versioning, attachments, permissions, retention, and integration contracts.
- Prefer stable internal names and avoid changing field meaning after integrations depend on it.

## Document libraries

- Define content types, metadata, folder policy, versioning, approval, templates, search, permissions, retention, archive, and migration.
- Avoid folder structures that duplicate metadata or create unnecessary inheritance breaks.
- Validate automation against versioning, check-out, required metadata, and large files.

## Modern pages

- Define audience, purpose, owner, page template, web parts, navigation, publishing, accessibility, analytics, and review cadence.
- Validate responsive layouts, headings, link purpose, alternative text, contrast, and keyboard use.

## Required validation

- Schema and internal-name review
- Index and volume test
- Permission matrix and inheritance review
- Retention and versioning decision
- List/library/page integration tests
- Search and navigation
- Accessibility and responsive review
- Backup, recovery, and rollback
- Visual verification of the default view, new-item form, and any consuming page at desktop and phone widths in the shared browser per `visual-verification.md`

