# Chapter 35: Project Infrastructure and Coordination System

## 35.1 Introduction: Building Research Infrastructure

Complex research projects require robust infrastructure for coordination, version control, data management, and workflow automation. This chapter documents the technical infrastructure supporting CCA research.

## 35.2 Architecture Overview

### 35.2.1 System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CCA RESEARCH INFRASTRUCTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Google Drive]    [OneDrive]    [GitHub]    [Notion]               │
│       │               │             │           │                   │
│       ├───────────────┼─────────────┼───────────┤                   │
│                       │                                             │
│                  [n8n Hub]                                          │
│                       │                                             │
│       ├───────────────┼─────────────┼───────────┤                   │
│       │               │             │           │                   │
│  [Backup]     [Sync]      [Versioning]    [Automation]              │
│                                                                     │
│  [VS Code]   [Claude Code]   [Antigravity]   [MCPs]                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 35.2.2 Source of Truth Hierarchy

| Level | System | Content |
|-------|--------|---------|
| Primary | OneDrive/Google Drive | Master documents |
| Secondary | GitHub | Code and versioned content |
| Tertiary | Local filesystem | Working copies |
| Coordination | Notion | Task tracking, handoffs |
| Automation | n8n | Workflows and sync |

## 35.3 Cloud Storage Structure

### 35.3.1 Google Drive Organization

```
📁 Tesis_NEXUS/
├── 📁 Manuscrito/
│   ├── thesis_chapter_01.md
│   ├── thesis_chapter_02.md
│   └── ... (all chapters)
├── 📁 Indices/
│   ├── INDICE_TOTAL_SUMADO_PARTE1.md
│   ├── INDICE_TOTAL_SUMADO_PARTE2.md
│   └── INDICE_TOTAL_SUMADO_PARTE3.md
├── 📁 Instrumentos/
│   ├── CCA-CIP_Interview.md
│   ├── SPIA-SS_Screener.md
│   └── RCTT_Triage.md
├── 📁 Datos/ (when collected)
├── 📁 Referencias/
│   └── bibliography.bib
└── 📁 Exports/
    └── TESIS_COMPLETA.docx
```

### 35.3.2 OneDrive Synchronization

Local working directory: `C:\Users\Lenovo\OneDrive\Tesis_NEXUS_Backup\`
- Automatic sync with cloud
- Versioning history available
- Offline access enabled

## 35.4 Version Control with Git

### 35.4.1 Repository Structure

```
tesis-cca/
├── manuscript/
│   └── chapters/
├── instruments/
├── analysis/
│   ├── scripts/
│   └── notebooks/
├── data/ (gitignored if sensitive)
├── docs/
├── .gitignore
├── README.md
└── CHANGELOG.md
```

### 35.4.2 Branching Strategy

| Branch | Purpose | Merge Target |
|--------|---------|--------------|
| main | Stable, reviewed content | - |
| develop | Work in progress | main |
| feature/* | New chapters/features | develop |
| fix/* | Corrections | develop |

### 35.4.3 Commit Conventions

Format: `type(scope): description`

Types:
- `feat`: New content
- `fix`: Corrections
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Restructuring
- `data`: Data updates

Example: `feat(ch25): add falsifiable hypotheses chapter`

## 35.5 Notion Workspace

### 35.5.1 Database Structure

| Database | Purpose | Key Fields |
|----------|---------|------------|
| Tasks | Action tracking | Status, Priority, Assignee, Due |
| Chapters | Content tracking | Status, Word Count, Version |
| Sources | Reference management | Citation, Used In, Status |
| Decisions | Decision log | Decision, Rationale, Date |
| Handoffs | Session continuity | Context, Next Steps, Date |

### 35.5.2 Task Workflow

```
📥 Backlog → 📋 Todo → 🔨 In Progress → 👀 Review → ✅ Done
```

### 35.5.3 Handoff Note Template

```markdown
## Handoff Note - [Date]

### ✅ Completed This Session
- [List of completed items]

### 🔄 In Progress
- [Items started but not finished]

### 📋 Next Steps
- [Prioritized next actions]

### ⚠️ Blockers
- [Any blocking issues]

### 💡 Notes for Next Session
- [Context or decisions to remember]
```

## 35.6 Automation with n8n

### 35.6.1 Available Workflows

| # | Workflow | Trigger | Action |
|---|----------|---------|--------|
| 01 | Daily Backup | Schedule (2 AM) | Backup Drive to local |
| 02 | Conversation Sync | Webhook | Save chat to Drive |
| 03 | Chapter Monitor | File change | Update tracking |
| 04 | Word Count | Manual | Count all chapters |
| 05 | Reference Check | Manual | Verify citations |

### 35.6.2 Webhook Endpoints

```
https://localhost:5678/webhook/conversation-sync
https://localhost:5678/webhook/chapter-update
https://localhost:5678/webhook/backup-now
```

### 35.6.3 Required Credentials

| Service | Credential Type | Status |
|---------|-----------------|--------|
| Google Drive | OAuth2 | Pending Client Secret |
| GitHub | Personal Access Token | Pending |
| Notion | Integration Token | Pending |

## 35.7 IDE Configuration

### 35.7.1 VS Code Setup

**Extensions**:
- Markdown All in One
- Claude Code Extension
- GitLens
- APA Reference Manager
- Word Count

**Settings** (in settings.json):
```json
{
  "editor.wordWrap": "on",
  "markdown.preview.fontSize": 14,
  "files.autoSave": "afterDelay"
}
```

### 35.7.2 Claude Code Integration

Script: `start_claude_code.ps1`
```powershell
$nodePath = "C:\Users\Lenovo\AppData\Local\ms-playwright-go\1.50.1"
$env:Path = "$nodePath;$env:Path"
claude
```

## 35.8 Data Management

### 35.8.1 Sensitive Data Handling

| Data Type | Storage | Encryption | Retention |
|-----------|---------|------------|-----------|
| Participant identifiers | Not stored | N/A | N/A |
| Audio recordings | Local encrypted drive | AES-256 | Per ethics approval |
| Assessment results | Pseudonymized | At rest | Per retention policy |
| Analysis outputs | Cloud (aggregated) | At rest | Permanent |

### 35.8.2 Backup Strategy

| Type | Frequency | Destination | Retention |
|------|-----------|-------------|-----------|
| Continuous | Real-time | OneDrive | 30 days version history |
| Daily | 2 AM | Google Drive | 90 days |
| Weekly | Sunday | External drive | 1 year |
| Milestone | At major version | Multiple locations | Permanent |

### 35.8.3 Recovery Procedures

File: `EMERGENCY_PROMPTS.md` contains:
- Universal recovery prompt
- Context restoration steps
- Priority task resumption

## 35.9 Collaboration Protocols

### 35.9.1 AI Assistance Disclosure

Per APA guidelines:
- All AI assistance documented
- AI-generated content reviewed and modified
- Responsibility remains with human author

### 35.9.2 Multi-AI Coordination

| AI | Role | Strengths |
|----|------|-----------|
| Claude | Primary development | Complex writing, code |
| ChatGPT | Research, brainstorming | Broad knowledge |
| Gemini | Cross-reference, verification | Google integration |
| Local LLMs | Offline tasks | Privacy |

### 35.9.3 Handoff Between AIs

Standard handoff includes:
- Summary of previous work
- Current state of files
- Pending tasks prioritized
- Decisions made and rationale

## 35.10 Quality Assurance

### 35.10.1 Content Review Checklist

- [ ] APA 7 format compliance
- [ ] Citations complete and formatted
- [ ] Tables numbered and titled
- [ ] Figures captioned
- [ ] Cross-references correct
- [ ] Acronyms defined first use
- [ ] Word count within limits

### 35.10.2 Technical Review Checklist

- [ ] Code runs without errors
- [ ] Data files accessible
- [ ] Links functional
- [ ] Versions synchronized

## 35.11 Conclusion: Infrastructure Enables Research

Robust infrastructure:
- Prevents data loss
- Enables collaboration
- Maintains version history
- Automates repetitive tasks
- Ensures reproducibility

The time invested in infrastructure pays dividends in research productivity and reliability.

---
**Status**: Draft - v1.0
**Word Count**: ~1,500 words
**Integration**: All project management and technical chapters
