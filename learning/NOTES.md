# Teaching Notes

- Use Matt Pocock's `teach` structure as the teaching baseline.
- The user wants an actual lesson experience, not a long chat explanation reformatted as HTML.
- Each lesson must teach one tightly scoped skill, then drill it through a tight interactive feedback loop.
- Keep lessons browser-readable without requiring a local clone.
- For a project-driven lesson, start from the pinned source code in this repository when it directly demonstrates the concept; use official docs to verify API contracts and semantics.
- Prefer primary sources and cite claims inside lessons.
- Project-driven, just-in-time only: do not pre-generate an Agent curriculum.
- Read `learning-records/` before choosing the next lesson so demonstrated knowledge is not re-taught.
- Reference source code is evidence and a transfer target, not a template to copy mechanically.

- When creating a new lesson, preserve the project Slice sequence exactly:
  `current business Slice → sufficient technical foundation → pinned reference source trace → learning gate → user's Own Design → vibe-coded implementation → tests/eval → understanding check → state update → next Slice`.
- A lesson must stop at the learning gate. Do not use lesson content to pre-decide the project's Own Design, generate implementation, or skip directly to coding.
- Technical foundation must be sufficient for the user to read the pinned source, make the design decision themselves, review generated code, and explain failure boundaries; it should not expand into unrelated curriculum.
- The pinned reference must be part of the teaching path itself, not merely a citation list at the end. Trace the real inputs, objects, control flow, execution path, and relevant failure boundary before asking for transfer to the user's project.

- Reference selection is not inferred ad hoc. The authoritative mapping is `docs/references.md` together with `docs/project-scope.md`. Use the reference already assigned to the current project/stage; do not switch to another pinned project merely because it contains a similarly named concept.
- Before creating a lesson or starting a new Slice, first read the current-stage reference assignment from the repository. If the repository does not clearly assign a reference for that stage, stop and resolve the gap from existing project documents before introducing a new reference.
