# Resume Hub Workspace

## What This Workspace Is

Everything resume and cover letter related. The system works in two layers:
a strong base resume, then tailored versions for specific job applications.

---

## Folder Structure

```
resume-hub/
├── base-resume/        # The master resume — always kept up to date
├── tailored/           # Job-specific resume versions
└── cover-letters/      # Cover letters per application
```

---

## Routing Table

| Task                              | Load These                                              | Skip These                    |
|-----------------------------------|---------------------------------------------------------|-------------------------------|
| Update the base resume            | `base-resume/resume-base.md`                           | tailored/, cover-letters/     |
| Tailor resume for a job           | `base-resume/resume-base.md`, job description          | Other tailored resumes        |
| Write a cover letter              | The tailored resume for this job, job description      | base-resume/, other letters   |
| Review a tailored resume          | The specific tailored file, job description            | Other files                   |

---

## Workflow: Tailoring a Resume

1. **Job description** — Paste or describe the target role
2. **Load base** — Read `base-resume/resume-base.md`
3. **Identify gaps** — What does the JD emphasize that the base resume undersells?
4. **Tailor** — Reorder, reword, and highlight relevant experience
5. **Save** — Write to `tailored/resume-[company]-[role].md`
6. **Cover letter** — Write to `cover-letters/cover-[company]-[role].md`

---

## Workflow: Updating the Base Resume

1. Load `base-resume/resume-base.md`
2. Make updates
3. Save in place — this file is always the current truth

---

## Resume Principles

- Lead with impact, not responsibilities ("Built X that reduced Y by Z%")
- Keep to one page unless 10+ years experience
- Use keywords from job descriptions — ATS systems scan for them
- Quantify everything possible
