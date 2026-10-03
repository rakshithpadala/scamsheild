# ScamShield UI Component Selections

Selected components from shadcn/ui, 21st.dev, and Magic UI for the ScamShield AI frontend architecture.

---

### 1. Hero Background: Animated Grid Pattern
- **Library**: Magic UI
- **Component**: `Animated Grid Pattern` / `Retro Grid`
- **Documentation Link**: [https://magicui.design/docs/components/animated-grid-pattern](https://magicui.design/docs/components/animated-grid-pattern)
- **Role in ScamShield**: Provides a subtle, cyber-defense grid background behind the main hero search area and verdict banner without distracting the user.
- **Key Props**: `numSquares={30}`, `maxOpacity={0.15}`, `duration={3}`.

---

### 2. Threat Gauge: Circular Risk Gauge
- **Library**: 21st.dev / shadcn/ui
- **Component**: `Risk Score Gauge` / `Radial Progress Indicator`
- **Documentation Link**: [https://21st.dev/community/components/gauge](https://21st.dev/community/components/gauge)
- **Role in ScamShield**: Visually renders the scam likelihood score (0 to 100) with dynamic animated color transitions:
  - Green (0–30): Safe
  - Yellow/Orange (31–69): Suspicious
  - Red (70–100): Confirmed Threat / High Risk
- **Key Props**: `value={riskScore}`, `strokeWidth={12}`, `animated={true}`.

---

### 3. Pipeline Stepper: Multi-Stage Analysis Stepper
- **Library**: 21st.dev / shadcn/ui blocks
- **Component**: `Progress Stepper` / `Analysis Pipeline Flow`
- **Documentation Link**: [https://21st.dev/community/components/stepper](https://21st.dev/community/components/stepper)
- **Role in ScamShield**: Displays the multi-agent detection pipeline progression in real time:
  1. Input Sanitization & Tokenization
  2. OCR / Lexical Feature Extraction
  3. Binary Spam Model (XGBoost / LightGBM)
  4. Multi-class Category Classifier (10 Categories)
  5. URL Blacklist & Reputation Lookup
  6. Final Multi-Modal Score Fusion
- **Key Props**: `currentStep={step}`, `status="complete" | "loading" | "error"`.

---

### 4. Copilot Chat Bubble: Interactive Assistant Dialogue
- **Library**: 21st.dev
- **Component**: `Chat Message Bubble`
- **Documentation Link**: [https://21st.dev/community/components/chat-bubble](https://21st.dev/community/components/chat-bubble)
- **Role in ScamShield**: Formats conversational interactions with the Cyber Safety Copilot, rendering verified citation chips (e.g. `[NPCI Circular 2024]`, `[RBI BE(A)WARE]`) and action buttons underneath the assistant's reply.
- **Key Props**: `role="user" | "assistant"`, `citations={sourceChips}`.

---

### 5. Card Hover: Interactive Magic Card
- **Library**: Magic UI
- **Component**: `Magic Card` / `Border Beam`
- **Documentation Link**: [https://magicui.design/docs/components/magic-card](https://magicui.design/docs/components/magic-card)
- **Role in ScamShield**: Highlights scam category cards in Model Lab and Pattern Explorer with subtle gradient borders when hovered, making complex model metrics easily browsable.
- **Key Props**: `gradientColor="#2563eb"`, `gradientOpacity={0.2}`.
