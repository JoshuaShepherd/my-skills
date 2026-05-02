
Create a new course section component for the section type: $0

## Process

1. Read 2-3 existing sections in `{{COURSE_SECTIONS_DIR}}/` to understand the pattern (e.g., `ReadingSection.tsx`, `VideoSection.tsx`, `ReflectionSection.tsx`)
2. Read `{{COURSE_SECTIONS_DIR}}/SectionContent.tsx` to understand the section registry and how sections are rendered
3. Create the new section at `{{COURSE_SECTIONS_DIR}}/$0Section.tsx` following the exact same pattern as existing sections
4. Register it in `SectionContent.tsx` by adding the import and mapping entry

## Rules

- Follow the exact component signature and prop types of existing sections
- Use shadcn/ui components and semantic CSS classes
- Never hardcode tenant-specific text
- Keep the component focused on rendering its content type
