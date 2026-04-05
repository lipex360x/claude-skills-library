# Update Checklist

For each changed file in `git diff main..HEAD`, evaluate every category below. If a category matches, note the target document and the specific section to update.

## architecture.md categories

### Routes / Endpoints
- New API routes or pages added?
- Existing routes renamed or removed?
- Route parameters or query params changed?

**Target section:** Routes, API, or Endpoints section.

### Patterns / Architecture
- New design patterns introduced (middleware, decorators, factories)?
- Existing patterns changed or replaced?
- New abstraction layers added?

**Target section:** Patterns or Architecture section.

### Schema / Data model
- Database schema changes (new tables, columns, relations)?
- API request/response shapes changed?
- New types or interfaces that represent data structures?

**Target section:** Schema, Data model, or Types section.

### Flows / Pipelines
- New data flows between layers?
- Processing pipelines added or modified?
- Event chains or message flows changed?

**Target section:** Key flows section.

### Directory structure
- New directories created?
- Files moved to different locations?
- New entry points added?

**Target section:** Directory structure or Project layout section.

### Dependencies
- New external dependencies added?
- Existing dependencies upgraded with breaking changes?
- New internal module dependencies?

**Target section:** Dependencies or External dependencies section.

### Config / Environment
- New environment variables required?
- Configuration files added or modified?
- Feature flags introduced?

**Target section:** Config section.

### Scripts / Commands
- New scripts added (build, deploy, dev, test)?
- Existing script behavior changed?
- New CLI commands or flags?

**Target section:** Scripts section.

## project.md categories (rare -- flag for review)

### Domain concepts
- New business entities or value objects introduced?
- Existing domain terms redefined?

### Business rules
- New constraints or validation rules added?
- Existing rules modified or removed?

### User roles / Permissions
- New user roles or auth levels?
- Permission boundaries changed?

### Scope boundaries
- Features explicitly excluded or deprecated?
- Project purpose or target audience shifted?
