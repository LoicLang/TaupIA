# Design System — TaupIA (Vibe 3: Premium / Dark)

## Style
- **Vibe**: Premium / Dark (Vercel / Raycast)
- **Scale**: Refined (compact, elegant)
- **Feel**: Cutting-edge, sophisticated, glassmorphism

## Colors
- **Background**: `#0a0a0a` (near-black)
- **Surface**: `#0f0f0f` (dark surface)
- **Primary**: `#4f46e5` (indigo)
- **Primary light**: `indigo-400` / `indigo-500`
- **Accent**: `#8b5cf6` (purple)
- **Success**: `#10b981` (emerald)
- **Text primary**: `white/90`
- **Text secondary**: `white/50`
- **Text muted**: `white/40`
- **Border**: `white/10`, `white/5`
- **Glass bg**: `white/[0.02]` with `backdrop-blur-md`
- **Glow orbs**: `indigo-600/20`, `blue-600/10` with `blur-[120px]`

## Typography
- **Font**: Inter (sans-serif), system fallback
- **Mono**: JetBrains Mono or system mono
- **Headings**: `font-bold tracking-tight`, gradient text `bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent`
- **Body**: `text-white/50 font-medium`
- **Labels**: `text-[10px]-[11px] font-bold uppercase tracking-wider text-indigo-400`
- **Mono labels**: `text-[11px] font-mono text-white/40`

## Components

### Badges
```tsx
<span className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/20 bg-indigo-500/5 text-[11px] font-bold tracking-[0.15em] uppercase text-indigo-400">
  <span className="relative flex h-2 w-2">
    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
    <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
  </span>
  Label text
</span>
```

### Glass Card
```tsx
<div className="rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1">
  <div className="bg-[#0f0f0f] rounded-xl overflow-hidden border border-white/5">
    {/* content */}
  </div>
</div>
```

### Buttons
Primary (white on dark):
```tsx
<button className="group flex items-center gap-2 px-8 py-3 bg-white text-black font-semibold text-sm rounded-full">
  Label
  <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
</button>
```

Secondary (ghost):
```tsx
<button className="px-8 py-3 text-sm font-medium text-white/70 border border-white/10 rounded-full hover:bg-white/5 transition-all">
  Label
</button>
```

Indigo action:
```tsx
<button className="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-semibold shadow-lg shadow-indigo-500/20 hover:bg-indigo-700 transition-all">
  Label
</button>
```

### Status Pills
```tsx
<div className="px-2 py-1 rounded bg-indigo-500/10 text-[10px] font-mono text-indigo-400 border border-indigo-500/20">
  STATUS
</div>
```

Success:
```tsx
<div className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-[11px] font-medium border border-emerald-500/20">
  Validé
</div>
```

### Input Fields
```tsx
<textarea className="w-full bg-white/[0.03] border border-white/10 rounded-xl px-4 py-3 text-sm text-white/90 placeholder:text-white/30 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 resize-none" />
```

### Window Header Bar
```tsx
<div className="flex items-center justify-between px-6 py-3 border-b border-white/5 bg-white/[0.01]">
  <div className="flex items-center gap-4">
    <div className="flex gap-1.5">
      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
    </div>
    <div className="flex items-center gap-2 text-[11px] font-mono text-white/40">
      <Terminal className="w-3 h-3" />
      filename.tex
    </div>
  </div>
</div>
```

### Grid Background
```tsx
<div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
  <div
    className="absolute inset-0 opacity-[0.15]"
    style={{
      backgroundImage: `linear-gradient(#4f46e5 1px, transparent 1px), linear-gradient(90deg, #4f46e5 1px, transparent 1px)`,
      backgroundSize: "40px 40px",
      maskImage: "radial-gradient(ellipse 60% 50% at 50% 0%, #000 30%, transparent 100%)",
      WebkitMaskImage: "radial-gradient(ellipse 60% 50% at 50% 0%, #000 30%, transparent 100%)",
    }}
  />
  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0a0a0a]/50 to-[#0a0a0a]" />
</div>
```

### Glow Orbs (Background Decoration)
```tsx
<div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
  <div className="absolute -top-[10%] left-[20%] w-[40%] h-[40%] rounded-full bg-indigo-600/20 blur-[120px]" />
  <div className="absolute top-[10%] right-[20%] w-[30%] h-[30%] rounded-full bg-blue-600/10 blur-[100px]" />
</div>
```

### IA Feedback Block
```tsx
<div className="p-4 rounded-lg bg-indigo-600/10 border border-indigo-500/20">
  <div className="flex items-center gap-2 mb-2">
    <Cpu className="w-3 h-3 text-indigo-400" />
    <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">IA Feedback</span>
  </div>
  <p className="text-[11px] text-white/60 leading-relaxed">
    Feedback content...
  </p>
</div>
```

### Skeleton Loading
```tsx
<div className="p-3 rounded-lg bg-white/[0.03] border border-white/5 animate-pulse">
  <div className="h-1.5 w-1/2 bg-white/10 rounded mb-2" />
  <div className="h-1.5 w-full bg-white/5 rounded" />
</div>
```

## Layout Principles
- Dark background (#0a0a0a) with subtle indigo grid pattern
- Glowing orbs for depth and atmosphere
- Glass cards with `backdrop-blur-md` and `border-white/10`
- Rounded corners: `rounded-full` for buttons/pills, `rounded-xl` for cards, `rounded-2xl` for outer containers
- Subtle borders: `border-white/5` to `border-white/10`
- Shadows: `shadow-lg shadow-indigo-500/20` for emphasis elements
- Transitions: `transition-all` on interactive elements
- No emojis
- French text for all UI labels
