# Real-time AI Translation Platform - Design Guidelines

## Design Approach
**System-Based**: Professional utility application for Finance/Healthcare sectors requiring trust, clarity, and efficiency. Focus on functional excellence with clean aesthetics.

## Color Palette
- Primary: Deep blues and teals
- Neutral: Slate grays
- Accent: Use for active states and status indicators
- Error/Stop: Red tones for "End Conversation" and "Stop" buttons
- Success: Green/teal for active listening states

## Layout Structure

### 1. Avatar Panel (Top 1/3 of viewport)
- Distinct background frame/container to represent video/lip-sync area
- Visual treatment to differentiate from other panels (border, shadow, or subtle background)
- Centered placement with generous padding
- Placeholder that clearly indicates "talking AI avatar" placement

### 2. Transcript Panel (Middle section)
- Scrollable chat-like interface
- Bilingual text display (source and translated language)
- Message bubbles or cards showing translation pairs
- Clear visual distinction between languages
- Timestamp support for each translation entry
- Auto-scroll to latest entry behavior

### 3. Control Area (Bottom - Fixed)
- Fixed positioning at bottom of viewport
- Contains all input controls and mode switchers
- Remains accessible during scroll

## Component Specifications

### Tab Switcher
- Two tabs: "Conversation Mode (Hands-off)" and "Convention Mode (Hands-on)"
- Active tab clearly indicated with color/underline
- Smooth transition between modes

### Mode 1: Conversation Mode (Hands-off)
- Primary button: "Start Conversation" (blue/teal)
- Active state: "End Conversation" (red background)
- Visual indicators for continuous listening (animated pulse, waveform, or VAD visualization)
- Listening state feedback clearly visible

### Mode 2: Convention Mode (Hands-on)
- Primary button: "Speak" (push-to-talk)
- Active state: "Stop" (changes appearance when pressed)
- Clear visual feedback when recording

### Global Controls
- "Clear History" button: Top right corner or discreetly placed in control area
- Text input field: Full-width with send button
- Image upload button: Adjacent to text input
- All controls using Lucide-React icons (Microphone, Stop, Upload, Trash)

## Typography
- Primary font: System font stack for clarity and performance
- Heading hierarchy: Bold weights for mode titles, regular for transcript text
- Font sizes: Larger for active states/buttons, readable sizes for transcript (16px base)

## Spacing System
- Use Tailwind units: 4, 6, 8, 12, 16 for consistent rhythm
- Generous padding in avatar panel (p-8 to p-12)
- Moderate spacing in transcript (p-4 to p-6)
- Compact but touchable controls (p-3 to p-4)

## Icons (Lucide-React)
- Microphone: Primary speaking/recording action
- StopCircle: Stop recording
- Upload/ImagePlus: Image upload
- Trash2: Clear history
- Send: Submit text input
- Volume2/Radio: Listening indicators

## Responsive Behavior
- Desktop: Three-panel layout as specified (1/3, middle, bottom)
- Mobile: Stack panels vertically, maintain fixed bottom controls
- Tablet: Adjust proportions appropriately
- Touch-friendly button sizes (minimum 44px height)

## Visual States
- Default: Clean, professional appearance
- Active listening: Animated indicators, color shifts
- Recording: Visual feedback (pulsing, color change)
- Error: Clear error messaging without disrupting layout
- Loading: Smooth transitions, skeleton states for transcript

## Trustworthiness Elements
- Professional color scheme (deep blues/slate)
- Clean borders and subtle shadows
- No excessive animations
- Clear status indicators
- Readable typography
- Consistent spacing and alignment

## Images
**No hero images required** - This is a utility application focused on functional panels and controls. The avatar panel serves as the visual anchor.

**Avatar Panel Background**: Consider a subtle gradient or pattern to distinguish the video area without competing for attention.