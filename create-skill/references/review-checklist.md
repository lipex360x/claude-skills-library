# Skill Review Checklist

Validate every item before finalizing a skill. Present results to the user.

## Description

- [ ] Is it pushy enough? Does it include trigger contexts, not just a summary?
- [ ] Does it answer WHAT the skill does AND WHEN it should activate?
- [ ] Does it include the "even if they don't explicitly say X" pattern where appropriate?

## SKILL.md body

- [ ] Under 500 lines? Detail extracted to references/?
- [ ] Instructions use imperative form? ("Extract X", not "You should extract X")
- [ ] Constraints are reasoned ("because X") rather than rigid ("ALWAYS/NEVER")?
- [ ] Steps are numbered with clear headers for major phases?
- [ ] Output formats defined with concrete examples?

## Quality

- [ ] Quality expectations repeated at multiple key points, not just stated once?
- [ ] Specific anti-patterns named, not just generic "make it good"?
- [ ] Refinement step included ("polish, don't add")?

## Subagents (if applicable)

- [ ] Each agent prompt includes ALL necessary context (specs, rules, quality standards)?
- [ ] Tool access is explicit — which tools for parent, which for subagents?
- [ ] Two-phase build if agents depend on setup completing first?
- [ ] Race conditions identified and mitigated?

## Structure

- [ ] Directory follows the standard layout (SKILL.md, references/, templates/)?
- [ ] References are one level deep (no reference chains)?
- [ ] Large references (>300 lines) have a table of contents?
- [ ] Skill is fully self-contained (no cross-skill dependencies)?
