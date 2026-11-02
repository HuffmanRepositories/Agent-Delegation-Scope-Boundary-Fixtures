# Scope-boundary taxonomy

- **Authority attenuation:** delegated rights must not exceed the delegator's rights.
- **Action restriction:** read-only, write, or destructive limits survive handoff.
- **Principal identity:** distinguish user, agent application, service, and delegated actor.
- **Resource isolation:** tenant, workspace, project, and resource constraints persist.
- **Nested delegation:** each hop preserves applicable constraints.
- **Sibling isolation:** separate children do not implicitly union their grants.
- **Lifecycle:** expiry and revocation are respected.
- **Approval binding:** approval is bound to the intended action/resource/context.
- **Enforcement point:** downstream tool/API checks remain required.
- **Audit continuity:** records preserve parent-child chain and grant provenance.
- **Fail-closed uncertainty:** missing or ambiguous authority is not treated as permission.

Categories are organizing aids, not a complete threat model.
