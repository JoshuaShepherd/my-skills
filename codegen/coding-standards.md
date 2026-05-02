---
name: coding-standards
description: "Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. Covers naming, immutability, error handling, async patterns, type safety, testing, and code smells."
user-invocable: true
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Agent
---

Apply coding standards to: $ARGUMENTS

---

# Coding Standards & Best Practices

Universal coding standards for all projects.

## Code Quality Principles

### 1. Readability First
- Code is read far more than written
- Use clear variable and function names
- Prefer self-documenting code over comments
- Maintain consistent formatting

### 2. KISS (Keep It Simple)
- Use the simplest solution
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract shared logic into functions
- Build reusable components
- Share utility functions across modules

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generalization
- Start simple, refactor when needed

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// Good: descriptive names
const searchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// Bad: unclear names
const q = 'election'
const flag = true
const x = 1000
```

### Function Naming

```typescript
// Good: verb-noun pattern
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// Bad: unclear or noun-only
async function market(id: string) { }
function similarity(a, b) { }
```

### Immutability (Critical)

```typescript
// Always use spread operator
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]

// Never mutate directly
user.name = 'New Name'  // Bad
items.push(newItem)     // Bad
```

### Error Handling

```typescript
// Good: complete error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}
```

### Async/Await Best Practices

```typescript
// Good: parallel when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// Bad: unnecessary sequential
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### Type Safety

```typescript
// Good: proper types
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> { }

// Bad: using 'any'
function getMarket(id: any): Promise<any> { }
```

## React Best Practices

### Component Structure

```typescript
// Good: typed function component
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children, onClick, disabled = false, variant = 'primary'
}: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled} className={`btn btn-${variant}`}>
      {children}
    </button>
  )
}
```

### State Updates

```typescript
const [count, setCount] = useState(0)

// Good: functional update based on previous state
setCount(prev => prev + 1)

// Bad: direct reference (stale in async contexts)
setCount(count + 1)
```

### Conditional Rendering

```typescript
// Good: clear conditionals
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}

// Bad: ternary hell
{isLoading ? <Spinner /> : error ? <ErrorMessage error={error} /> : data ? <DataDisplay data={data} /> : null}
```

## API Design Standards

### REST Conventions

```
GET    /api/markets              # List all
GET    /api/markets/:id          # Get one
POST   /api/markets              # Create
PUT    /api/markets/:id          # Full update
PATCH  /api/markets/:id          # Partial update
DELETE /api/markets/:id          # Delete

# Filtering via query params
GET /api/markets?status=active&limit=10&offset=0
```

### Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: { total: number; page: number; limit: number }
}
```

### Input Validation (Zod)

```typescript
import { z } from 'zod'

const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1)
})

export async function POST(request: Request) {
  const body = await request.json()
  try {
    const validated = CreateMarketSchema.parse(body)
    // proceed with validated data
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      }, { status: 400 })
    }
  }
}
```

## File Organization

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   └── (auth)/            # Route groups
├── components/            # React components
│   ├── ui/               # Generic UI
│   ├── forms/            # Forms
│   └── layouts/          # Layouts
├── hooks/                # Custom React hooks
├── lib/                  # Utils and config
├── types/                # TypeScript types
└── styles/              # Global styles
```

### File Naming

```
components/Button.tsx          # PascalCase for components
hooks/useAuth.ts              # camelCase with 'use' prefix for hooks
lib/formatDate.ts             # camelCase for utilities
types/market.types.ts         # camelCase with .types suffix
```

## Comments

```typescript
// Good: explain "why", not "what"
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)

// Intentional mutation here for performance with large arrays
items.push(newItem)

// Bad: stating the obvious
// Increment counter by 1
count++
```

## Testing (AAA Pattern)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})

// Good test names
test('returns empty array when no markets match query', () => { })
test('throws error when API key is missing', () => { })

// Bad test names
test('works', () => { })
test('test search', () => { })
```

## Code Smells to Watch For

### 1. Long Functions
```typescript
// Bad: 50+ line functions. Split them.
function processData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### 2. Deep Nesting
```typescript
// Bad: 5+ levels. Use early returns instead.
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return
// do work
```

### 3. Magic Numbers
```typescript
// Bad: unexplained numbers
if (retryCount > 3) { }

// Good: named constants
const MAX_RETRIES = 3
if (retryCount > MAX_RETRIES) { }
```

**Remember**: Code quality is non-negotiable. Clear, maintainable code enables fast development and confident refactoring.
