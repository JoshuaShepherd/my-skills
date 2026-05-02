---
name: course-section
description: Create a new course section component following the existing section pattern. Use when adding new content types to courses.
user-invocable: true
allowed-tools: Read, Write, Grep, Glob
---

Create a new course section component for the section type: $0

## Process

1. Read 2-3 existing sections in `src/components/courses/sections/` to understand the pattern (e.g., `ReadingSection.tsx`, `VideoSection.tsx`, `ReflectionSection.tsx`)
2. Read `src/components/courses/sections/SectionContent.tsx` to understand the section registry and how sections are rendered
3. Create the new section at `src/components/courses/sections/$0Section.tsx` following the exact same pattern as existing sections
4. Register it in `SectionContent.tsx` by adding the import and mapping entry

## Rules

- Follow the exact component signature and prop types of existing sections
- Use shadcn/ui components and semantic CSS classes
- Never hardcode tenant-specific text
- Keep the component focused on rendering its content type
