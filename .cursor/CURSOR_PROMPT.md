Cursor assistant prompt — change summary for this project

Use this prompt with Cursor (or any assistant) to generate a concise, actionable summary of changes made to a repository, and to extract the automation/scripts that were added so they can be applied to other projects.

Prompt:

You are a repository assistant. Given this project's working tree and git history, answer the following as clearly and concisely as possible.

1) What did you change in this project?  
   - Provide a short bullet list of the substantive code, docs, and infra edits (files added/modified/deleted) and their purpose.

2) What did you add that was problematic or questionable?  
   - List any additions that might be surprising, unnecessary, or could be reverted, and why.

3) What did you have to fix repeatedly?  
   - Describe items you had to revisit or patch multiple times during the work, including the root causes (e.g., linter conflicts, notebook cell mismatches, kernel issues).

4) List all the automation, CI/CD, Docker, and helper scripts you created.  
   - For each item, include the file path, a one-line description of what it does, and the exact command a user should run to invoke it (host-facing, cross-platform where possible).

5) Suggested checklist to apply the same improvements to another repository.  
   - Short step-by-step checklist the user can follow to replicate these changes in another project (e.g., "add data package, create scripts, add Dockerfile with ipykernel, add CI workflow to run tests + execute notebook, add interactive run scripts").

Constraints:
- Keep each answer concise (2–8 bullets per section).
- When listing commands, prefer Docker-based, OS-agnostic variants.
- For any risky or large changes (e.g., adding TeX to Docker), explicitly note size/cost trade-offs.

Use this prompt as-is with Cursor to inspect this repository and produce the requested summary.

