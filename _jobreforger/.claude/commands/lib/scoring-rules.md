# Scoring-Aware Writing Rules

Reference file for resume writing optimization. Read this before writing any resume content.

---

## STEP 0 — INTERNALIZE THE SCORING ENGINE

Every section you write maps to specific weighted components. The weights tell you where to spend your editing budget.

ATS Scorer (8 components, v2.5 rebalanced):

| # | Component | Weight | What Wins | Primary Section |
|---|-----------|--------|-----------|-----------------|
| 1 | Phrase Match | 25% | Exact 2-4 word JD phrases (10.6x callback increase). If JD says "embedded Linux platform", use those exact words. | Bullets |
| 2 | Keyword Match | 20% | Lemmatized exact + synonym match. High-frequency JD nouns in Core Competencies first. | Core Competencies |
| 3 | Weighted Industry Terms | 15% | Domain-specific terms score 3x. Auto-detected from JD domain (clinical, tech, finance, etc.). | Core Competencies, Bullets |
| 4 | Semantic Similarity | 10% | Sentence-transformer cosine sim. Use JD phrasing verbatim — paraphrases score lower. | Summary, Bullets |
| 5 | BM25 Score | 10% | Term frequency x inverse document frequency. Diminishing returns after 2 uses. | Distributed |
| 6 | Job Title Match | 10% | Exact JD title in resume header/summary (10.6x callback data). | Summary, Header |
| 7 | Graph Centrality | 5% | Inferred skill bonus. Related skills present = scorer infers missing adjacent skills. | Core Competencies (strategic adjacency) |
| 8 | Skill Recency | 5% | Exponential decay by year. Recent skills must appear in current/most-recent role. | Most recent role bullets |

HR Scorer (6 factors):

| # | Factor | Weight | What Wins | Primary Section |
|---|--------|--------|-----------|-----------------|
| 1 | Job Fit | 25% | Domain + role alignment. Must hit the auto-detected domain. Domain-defining terms in first 100 words. | Summary (first 100 words) |
| 2 | Experience Fit | 20% | Years match JD minimum +/- 3 yrs (Goldilocks zone). Don't undersell seniority. | Summary sentence 1, dates |
| 3 | Skills Match | 20% | Skill IN ACTION = 2x weight vs. skill listed. "Led medical monitoring" >> "Medical Monitoring" in a list. | Bullets (action verbs) |
| 4 | Impact Signals | 15% | Metric magnitude: $M/$B = +3 pts, multipliers (10x) = +2.5 pts, % = +2 pts, large raw numbers = +1.5 pts. 50%+ of bullets need metrics. | Bullets |
| 5 | Career Trajectory | 10% | Title regression slope must be positive. Senior to Lead to Director = good. Don't bury senior titles. | Job title ordering |
| 6 | Competitive Edge | 10% | Top-tier companies/universities = high prestige. Name them early. | Summary, Education placement |

Domain Bonuses (auto-detected):
- All domain-critical keywords found = +10 ATS pts
- Publications section present (if applicable to domain) = +10 ATS pts
- Readability grade 10-12 = +3 pts (Grade 13+ = -3 penalty — avoid complex sentences, semicolons, nested clauses)

---

## STEP 1 — JD DECONSTRUCTION (complete before writing)

Extract each item below and hold it as your editing blueprint. If you skip this step, your draft will be generic and under-optimized.

1A. Role Classification:
- Role tier: Lead, supporting, or hybrid? Determines seniority framing in summary.
- Management scope: People management required? Cross-functional leadership? Determines verb level in bullets.
- Domain focus: Specific specialty/vertical? Drives domain term selection.

1B. Language Extraction:

| Extract | Purpose | Example |
|---------|---------|---------|
| Top 5 explicit verbs from responsibilities | Drive bullet verb choices | "leads", "authors", "monitors", "coordinates", "reviews" |
| Critical noun phrases (exact 2-4 word phrases) | Reuse verbatim for Phrase Match (25%) | Extract exact multi-word phrases from the JD — these must appear verbatim |
| Hard requirements | Must appear or instant disqualification | Minimum years, degree, certifications, specific system experience |
| Preferred qualifications | High-value differentiators if experience exists | Board certification, specific TA experience, publications |
| Implicit signals | Drives summary framing and bullet emphasis | Scientific rigor? Stakeholder management? Data oversight? Operational speed? |

1C. Ceiling Check:
Does the JD contain non-role boilerplate? (Salary ranges, benefits paragraphs, staffing-agency language, EEO text exceeding 2 sentences)
- If YES: ATS ceiling is ~69-73%. Set expectations. Do NOT over-iterate chasing 75%+ if all domain component weights are at 100%. Max 2 iteration cycles.
- If NO: Standard 75-85% ATS target applies.

---

## STEP 2 — SECTION-BY-SECTION OPTIMIZATION

Each section targets specific scoring components. The component targets are listed so you know exactly why you're making each choice.

### PROFESSIONAL SUMMARY
Targets: Phrase Match (25%), Job Fit (25%), BM25 (10%), Semantic Similarity (10%), Job Title Match (10%)

| Sentence | Purpose | Rule |
|----------|---------|------|
| 1 | Identity + seniority + domain | "[Title descriptor] with [X] years in [domain/specialty]" |
| 2 | JD phrase injection | Use 2-3 exact JD noun phrases naturally in one sentence |
| 3 | Top differentiator | Include highest-magnitude metric available |
| 4 | Forward-looking alignment | Match JD mission or company therapeutic focus |

Constraints: Max 4 lines. Readability grade 10-12. No semicolons, no nested clauses. Domain-defining terms must appear within the first 100 words of the resume (Job Fit trigger).

### CORE COMPETENCIES
Targets: Phrase Match (25%), Keyword Match (20%), Weighted Industry Terms (15%), Graph Centrality (5%)

Layout: 12-14 items in a 3-column grid.

Priority order for item selection:
1. Exact JD multi-word phrases (Phrase Match — 25%, highest ATS weight)
2. Exact JD keyword matches (Keyword Match — 20%)
3. Domain-critical terms not in JD but expected by scorer for the detected domain (Industry Terms — 15%)
4. Strategic adjacency terms that trigger inferred skills (Graph Centrality — 5%)
5. Transferable skills only if slots remain

Rule: Each keyword gets its 1 counted appearance here. Do NOT repeat in bullets unless demonstrating it in action (which counts as a different scoring signal — Skills Match).

### PROFESSIONAL EXPERIENCE — BULLETS
Targets: Phrase Match (25%), Skills Match (20%, action = 2x), Impact Signals (15%), Semantic Similarity (10%)

The Action Formula:
```
[JD verb at L3+] + [exact JD noun phrase] + resulting in + [metric with magnitude]
```

Verb Hierarchy (use L3+ for 70%+ of bullets):

| Level | Label | Verbs | Usage Target |
|-------|-------|-------|--------------|
| L4 | Transformative | Pioneered, Architected, Instituted, Generated, Secured | 1-2 bullets max (signature achievements) |
| L3 | Directive | Spearheaded, Directed, Championed, Orchestrated, Established | Primary verb level (40-50% of bullets) |
| L2 | Managerial | Led, Managed, Oversaw, Coordinated, Supervised | Supporting bullets (20-30%) |
| L1 | Contributory | Reviewed, Monitored, Assisted, Supported, Participated | Minimize (10% or less) |
| L0 | AVOID | "Responsible for", "Helped", "Worked on" | Never use |

Metric Magnitude Targets:

| Magnitude Type | Score Bonus | Minimum Requirement |
|----------------|-------------|---------------------|
| $M / $B values | +3 pts | Include in at least 2 bullets |
| Multipliers (10x, 3x) | +2.5 pts | Include where truthful |
| Percentages | +2 pts | Use liberally |
| Large raw numbers | +1.5 pts | Fallback when $ or % unavailable |

50%+ of all bullets must contain a quantified metric.

Phrase Insertion Strategy (Phrase Match — 25%, highest ATS weight):
Extract exact 2-4 word noun phrases from the JD and insert them verbatim in bullets where the candidate has matching experience. The scorer rewards exact phrase matches, not paraphrases. Prioritize phrases from the JD's core responsibilities and required qualifications sections.

### PUBLICATIONS (if present in master resume)
Targets: Domain Bonus (+10 ATS), Competitive Edge (10%)
Rule: Keep EXACTLY as in master resume. The section's existence is worth +10 ATS points. Zero edits. Only include this section if the master resume contains publications.

### EDUCATION
Targets: Competitive Edge (10%), Experience Fit (20%)
Rule: Keep EXACTLY as in master resume. Top-tier institution = high prestige multiplier. Do not bury.

### CERTIFICATIONS & LICENSURE
Rule: Keep EXACTLY as in master resume. Zero edits.

### PROFESSIONAL MEMBERSHIPS
Rule: Keep EXACTLY as in master resume. Zero edits.

---

## RESUME STRUCTURE (ATS/Workday Compliant)

```
[FULL NAME, CREDENTIALS]
[City, State ZIP] | [Phone] | [Email]
[LinkedIn URL]

_______________________________________________________________________________
PROFESSIONAL SUMMARY

[4 sentences per Step 2 rules — NOT a keyword dump]

_______________________________________________________________________________
CORE COMPETENCIES

[12-14 JD-relevant keywords — PRIMARY keyword location]
[Keyword 1]    [Keyword 2]    [Keyword 3]

_______________________________________________________________________________
PROFESSIONAL EXPERIENCE

[EXACT TITLE] | [EXACT COMPANY] | [Location]
[Month Year] - [Present/End Date]

[L3+ Verb] [JD noun phrase] [STAR context + action], achieving [quantified metric]

_______________________________________________________________________________
EDUCATION

[EXACT from master resume]

_______________________________________________________________________________
CERTIFICATIONS & LICENSURE

[EXACT from master resume]

_______________________________________________________________________________
PUBLICATIONS

[EXACT from master resume — NO keyword additions]

_______________________________________________________________________________
PROFESSIONAL MEMBERSHIPS

[EXACT from master resume]
```

ATS FORMAT RULES:
- NO columns, tables, text boxes, graphics, icons, headers/footers
- YES ALL-CAPS headers, bullet points, horizontal lines (___)
- Font: Calibri/Arial, 10-12pt body, 14-16pt name
- Contact info in MAIN BODY
- Job format: "TITLE | COMPANY | Location" (Workday pattern)
- Do NOT use ** in .md files — DOCX generator handles bold formatting

## EXPERIENCE BULLET DISTRIBUTION
- Current role: 4-6 bullets (strongest metrics, most detail)
- Recent relevant roles: 3-4 bullets each
- Older relevant roles: 2-3 bullets each
- Very old roles (10+ years): 1-2 bullets
- RULE: Every role from the master resume must appear. Never skip a role to save space. Condense bullets, not roles.

---

## WRITING RULES (Apply to EVERY bullet)

Read the full writing rules from `.claude/commands/writing-coach.md`. Apply Rules 1-14 to every bullet and section. Key rules summary:

Rule 1 (So What?): Every bullet must show impact, not just activity
Rule 2 (6-Second): Front-load value in first 3 words of each bullet
Rule 3 (Deadwood): Strip "Responsible for", "Successfully", "Various", "Helped", "Assisted"
Rule 4 (Metrics): 50%+ of bullets must contain quantified metrics (plain text, no ** bold)
Rule 5 (Verbs L3+): 70%+ verbs at Directive/Strategic/Transformative level
Rule 6 (Architecture): Use Impact Lead, Challenge-Action-Result, or Scope-Authority structures
Rule 7 (Burstiness): Vary bullet lengths: SHORT (6-10), MEDIUM (11-18), LONG (19-28 words)
Rule 8 (Parallel): Consistent grammar patterns within each role
Rule 9 (Summary Hook): Open with identity + authority, close with differentiator
Rule 10 (Authenticity): Every bullet must pass the "Could they discuss this in an interview?" test
Rule 11 (Anti-Cliche): FORBIDDEN: Spearheaded, Leveraged, Utilized, Facilitated. USE: Led, Directed, Built, Drove, Cut, Grew
Rule 12 (Grammatical Variety): Min 2 bullets per job block NOT starting with an action verb
Rule 13 (Texture): One real-world specific detail per job block (named tool, regulation, constraint)
Rule 14 (Summary Anti-Cliche): NEVER write "proven track record", "passionate about", "dynamic professional"

Tone: Senior professional — authoritative and evidence-based, NOT junior coordinator.

---

## QUICK REFERENCE — SCORING CHEAT SHEET

Fastest levers by gap type:

| Problem | Fastest Fix | Weight Moved |
|---------|-------------|--------------|
| ATS low, phrases missing | Insert exact JD multi-word phrases into bullets | 25% (highest ATS weight) |
| ATS low, keywords missing | Add to Core Competencies | 20% |
| ATS low, no title match | Add JD title to Summary | 10% |
| HR low, skills listed not demonstrated | Convert list items to action bullets | 20% (2x multiplier) |
| HR low, no metrics | Add metrics to 50%+ of bullets | 15% |
| HR low, weak opening | Rewrite Summary sentence 1 with domain identity | 25% |
| Both low, domain terms missing | Add domain-critical keywords | 15% ATS + 25% HR (Job Fit) |

Component coverage by section:

| Section | ATS Components Hit | HR Factors Hit |
|---------|-------------------|----------------|
| Summary | Semantic (10%), BM25 (10%), Job Title (10%) | Job Fit (25%), Experience (20%), Edge (10%) |
| Core Competencies | Keyword (20%), Industry (15%), Graph (5%) | — |
| Bullets | Phrase (25%), Semantic (10%), Recency (5%) | Skills (20%), Impact (15%), Trajectory (10%) |
| Publications | Domain bonus (+10) | Edge (10%) |
| Education | — | Edge (10%), Experience (20%) |
