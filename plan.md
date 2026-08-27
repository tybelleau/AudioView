# Audio Asset Browser — Development Plan

## 0. Setup Before Writing Application Code

You already have **Python** and **VS Code** installed. Before starting development, install/update the remaining tools below.

### Required

#### 1. Git

Install Git for Windows if it is not already installed.

After installation, verify:

```powershell
git --version
```

You should also have a GitHub repository created for this project.

#### 2. Python packages

Do **not** install PySide6 globally. The project should use a virtual environment.

After creating the project folder, create the virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
source .venv\Scripts\Activate
```

Then upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install PySide6:

```powershell
pip install PySide6
```

At the beginning of development, PySide6 is the only external Python package that should be required.

#### 3. VS Code Python support

In VS Code, make sure the official **Python** extension from Microsoft is installed.

Select the project's `.venv` interpreter as the Python interpreter.

Use:

```text
Ctrl + Shift + P
→ Python: Select Interpreter
→ select .venv
```

### Not required initially

Do **not** install these yet:

- FFmpeg
- Qt Creator
- PyInstaller
- additional audio libraries
- database software
- web frameworks
- UI frameworks other than PySide6

They may become useful later, but they are not part of the initial development stack.

### Optional later

**PyInstaller** will eventually be used to package the application into a Windows executable. Do not add it until the application is working.

**FFmpeg** should only be introduced if the chosen waveform/audio-decoding approach requires it.

---

# 1. Project Overview

## 1.1 Purpose

The Audio Asset Browser is a Windows desktop application designed to make finding sound effects and other audio assets extremely fast during video editing and sound-design work.

The application is intentionally focused:

> Browse an audio folder, navigate its structure quickly, and immediately preview audio files.

It is **not** intended to be:

- an audio editor
- a DAW
- a music player
- a media-management suite
- a general-purpose file explorer

The application should stay lightweight, fast, visually clean, and keyboard-driven.

---

# 2. Core User Experience

The primary workflow is:

```text
Choose Folder
      ↓
View audio folder structure
      ↓
Navigate with keyboard
      ↓
Select audio file
      ↓
Audio immediately plays
      ↓
Waveform and filename appear
      ↓
Continue navigating
      ↓
Find the right sound
```

The user should not need to repeatedly open individual audio files in another application.

The application should make auditioning many sounds feel similar to browsing assets in a professional creative application.

---

# 3. Technology Stack

| Purpose | Technology |
|---|---|
| Programming language | Python |
| Desktop GUI | PySide6 |
| GUI framework underneath | Qt |
| Audio playback | Qt Multimedia / QMediaPlayer |
| File/directory handling | Python `pathlib` |
| File tree | Qt model/view/tree components |
| Waveform | Custom PySide6/Qt widget |
| Version control | Git |
| Repository | GitHub |
| IDE | VS Code |
| Windows packaging | PyInstaller, later |
| Advanced audio decoding | FFmpeg, only if required later |

The application should remain Python-first. C++ is not required for this project.

---

# 4. V1 Requirements

## 4.1 File Formats

V1 supports:

- `.wav`
- `.mp3`
- `.aac`
- `.m4a`

File extension matching should be case-insensitive.

Examples:

```text
sound.wav
sound.WAV
sound.mp3
sound.MP3
sound.aac
sound.m4a
```

are valid.

Other files should not appear in the application's file tree.

---

# 5. File Section

The left side of the application is the **File Section**.

Its visual behavior should resemble a modern file explorer, particularly the general organization of the VS Code Explorer.

## 5.1 Choose Folder

At the top of the File Section:

```text
[ Choose Folder ]
```

Clicking this opens the native Windows folder-selection dialog.

The selected directory becomes the root of the application's file tree.

Example:

```text
D:\Sound Effects
```

---

## 5.2 Folder Structure

The application recursively examines the selected directory.

Example filesystem:

```text
Sound Effects
├── Ambience
│   ├── Forest
│   │   ├── wind.wav
│   │   └── birds.wav
│   └── City
│       └── traffic.mp3
│
├── Footsteps
│   ├── Concrete
│   │   ├── foot01.wav
│   │   └── foot02.wav
│   └── Dirt
│       └── dirt01.wav
│
└── Misc
    └── notes.txt
```

The application should display:

```text
Sound Effects
├── Ambience
│   ├── Forest
│   │   ├── wind.wav
│   │   └── birds.wav
│   └── City
│       └── traffic.mp3
│
├── Footsteps
│   ├── Concrete
│   │   ├── foot01.wav
│   │   └── foot02.wav
│   └── Dirt
│       └── dirt01.wav
```

`Misc` should not appear because it contains no supported audio.

---

## 5.3 Folder Visibility Rule

A folder should be displayed only if it contains at least one supported audio file somewhere inside its hierarchy.

This keeps the tree focused entirely on usable audio assets.

---

# 6. File Tree Navigation

The file tree is the most important part of the application.

## 6.1 Up/Down Navigation

### Up Arrow

Move the selection to the previous visible tree item.

### Down Arrow

Move the selection to the next visible tree item.

The tree behaves like a traditional hierarchical file tree.

Example:

```text
▼ Footsteps
    foot01.wav
    foot02.wav
    foot03.wav
▼ Doors
    door01.wav
    door02.wav
```

Navigation can therefore move:

```text
foot01.wav
    ↓
foot02.wav
    ↓
foot03.wav
    ↓
Doors
    ↓
door01.wav
```

If the selected item is a folder:

- it becomes the selected item
- it does not play audio
- pressing Enter expands/collapses it

---

## 6.2 Enter

When a folder is selected:

```text
Enter → expand
Enter → collapse
```

The folder remains selected.

Audio files do not require Enter to play because selecting them automatically starts playback.

---

## 6.3 Ctrl + Up / Ctrl + Down

These are dedicated folder-navigation shortcuts.

### Ctrl + Up

Navigate to the previous folder.

### Ctrl + Down

Navigate to the next folder.

This should skip individual audio files.

The purpose is fast navigation through large sound libraries.

---

# 7. Audio Playback Behavior

Audio playback is intentionally simple.

## 7.1 Automatic Playback

Whenever an audio file becomes selected:

1. Stop the currently playing audio.
2. Load the newly selected file.
3. Start it from the beginning.
4. Update the filename.
5. Update the waveform.

There must never be overlapping audio.

---

## 7.2 Spacebar

Space controls the currently selected audio file.

```text
Playing → Space → Pause
Paused  → Space → Resume
Stopped → Space → Play from beginning
```

If an audio file finishes, pressing Space should replay it from the beginning.

---

## 7.3 No Looping

V1 does not include looping.

When an audio file reaches its end, playback stops.

---

## 7.4 No Volume Controls

V1 does not provide an application-specific volume control.

The application's audio should use the appropriate system/application audio behavior without adding unnecessary controls.

---

# 8. Play Section

The **Play Section** occupies the lower-right portion of the window.

It contains:

```text
[ Previous ] [ Play/Pause ] [ Next ] [ Progress Bar ]
```

## 8.1 Previous

Select the previous audio file according to the application's audio navigation rules and play it.

## 8.2 Play/Pause

Same behavior as Spacebar.

## 8.3 Next

Select the next audio file according to the application's audio navigation rules and play it.

## 8.4 Progress Bar

The progress bar shows the current playback position.

It should support seeking.

The user can click or drag the position to move through the audio.

---

# 9. View Section

The **View Section** occupies the large upper-right portion of the window.

It contains only useful visual information.

## 9.1 Filename

Display the currently selected audio filename clearly.

Example:

```text
Concrete_Footstep_Heavy_03.wav
```

## 9.2 Waveform

Display a waveform representing the selected audio file.

The waveform should:

- update when the selected file changes
- be visually clear
- scale to the available space
- represent the actual audio
- remain simple and unobtrusive

V1 does not need:

- spectrum analysis
- frequency visualization
- animated effects
- audio meters
- decorative visualizations

---

# 10. Overall Window Layout

The target layout is:

```text
┌─────────────────────────────────────────────────────────────┐
│                         Application                         │
├───────────────────────┬─────────────────────────────────────┤
│                       │                                     │
│     FILE SECTION      │            VIEW SECTION             │
│                       │                                     │
│ [ Choose Folder ]     │         Audio Filename              │
│                       │                                     │
│ ▼ Sound Effects       │                                     │
│   ▼ Footsteps         │             WAVEFORM                │
│     foot01.wav        │                                     │
│     foot02.wav        │                                     │
│     foot03.wav        │                                     │
│   ▼ Doors             │                                     │
│     door01.wav        │                                     │
│                       │                                     │
│                       │                                     │
│                       ├─────────────────────────────────────┤
│                       │            PLAY SECTION             │
│                       │                                     │
│                       │  ◀      ▶      ▶    ─────●──────  │
│                       │ Previous Play   Next    Progress    │
└───────────────────────┴─────────────────────────────────────┘
```

The main sections should be resizable.

The boundary between the File Section and the right-side content should be draggable.

---

# 11. Visual Design

## 11.1 Design Goal

The application should look like a modern creative/developer desktop application.

Design inspiration:

- ChatGPT
- Notion
- VS Code
- modern audio applications

Do not directly copy any proprietary interface. Use their general design principles.

## 11.2 Visual Characteristics

The target aesthetic:

- modern
- dark
- minimal
- professional
- low visual noise
- subtle borders
- restrained accent color
- clean typography
- comfortable spacing
- subtle rounded controls where appropriate

The UI should prioritize speed and clarity over decoration.

---

# 12. Keyboard-First Design

The application should be fully usable for its primary workflow without constantly reaching for the mouse.

V1 shortcuts:

| Shortcut | Function |
|---|---|
| ↑ | Previous tree item |
| ↓ | Next tree item |
| Ctrl + ↑ | Previous folder |
| Ctrl + ↓ | Next folder |
| Enter | Expand/collapse folder |
| Space | Play/pause |
| Previous button | Previous audio |
| Next button | Next audio |
| Play button | Play/pause |
| Progress bar | Seek |

Additional seeking keyboard shortcuts can be added during implementation if they improve the workflow.

---

# 13. Application Architecture

The application should be divided by **responsibility**, not simply by screen section.

Recommended architecture:

```text
Application
│
├── Main Window
│   │
│   ├── File Browser
│   ├── View Panel
│   └── Playback Controls
│
├── File System Manager
│
├── Audio Player
│
└── Waveform Generator
```

## 13.1 Main Window

Responsible for assembling the UI and coordinating major application components.

It should not contain all application logic.

---

## 13.2 File Browser

Responsible for:

- displaying the tree
- folder expansion/collapse
- selection
- keyboard navigation
- Ctrl + Up/Down folder navigation
- communicating selection changes

---

## 13.3 File System Manager

Responsible for:

- selecting a root directory
- recursively scanning directories
- identifying supported audio
- filtering unsupported files
- determining which folders should appear
- providing filesystem information to the File Browser

---

## 13.4 Audio Player

Responsible for:

- loading audio
- playing
- pausing
- stopping
- seeking
- reporting playback position
- reporting playback completion
- ensuring only one audio file plays at a time

Use Qt Multimedia / `QMediaPlayer` as the initial playback solution.

---

## 13.5 View Panel

Responsible for:

- filename display
- waveform display
- updating when selection changes

---

## 13.6 Playback Controls

Responsible for:

- Previous button
- Play/Pause button
- Next button
- progress/seek bar

These controls should communicate with the Audio Player and File Browser rather than independently implementing playback logic.

---

## 13.7 Waveform Generator

Responsible for:

- obtaining audio sample data
- reducing it to a reasonable number of visual points
- providing waveform data to the waveform widget

Waveform generation may require an additional audio-decoding solution depending on what Qt Multimedia provides reliably for the supported formats.

Do not add a decoding dependency until it is actually necessary.

---

# 14. State Management

Do not introduce a separate state-management framework.

The application is small enough to manage state through its main components and Qt signals/slots.

Important state includes:

```text
Current root folder
Current selected tree item
Current selected audio file
Current playback state
Current playback position
Current audio duration
Current waveform data
```

The File Browser should be the source of truth for the current selection.

The general event flow should be:

```text
User navigates tree
        ↓
Tree selection changes
        ↓
Selection-changed signal
        ↓
Main application responds
        ├── Audio Player → play selected audio
        ├── View Panel → update filename
        └── Waveform → update waveform
```

This keeps responsibilities separated.

---

# 15. Important PySide6 Concepts to Learn

You do not need to learn all of Qt before starting.

Learn these concepts as the project requires them.

## Phase 1

- `QApplication`
- `QMainWindow`
- widgets
- layouts
- signals and slots

## Phase 2

- `QTreeView`
- Qt models
- selection models
- model/view architecture

## Phase 3

- keyboard events
- Qt key constants
- event handling

## Phase 4

- `QMediaPlayer`
- `QAudioOutput`
- playback signals
- media position/duration

## Phase 5

- custom widgets
- `paintEvent()`
- `QPainter`

## Phase 6

- Qt Style Sheets
- fonts
- spacing
- borders
- colors
- hover/selected states

The goal is to learn PySide6 **while building the application**, rather than attempting to learn the entire framework first.

---

# 16. Development Process

Do not attempt to build the whole application at once.

Every milestone should produce a working application.

The recommended order is below.

---

# Phase 1 — Project Initialization

## Goal

Create a clean Python project and verify that PySide6 works.

### Tasks

- Create project directory.
- Initialize Git.
- Connect to GitHub.
- Create `.gitignore`.
- Create `.venv`.
- Install PySide6.
- Configure VS Code to use `.venv`.
- Create the smallest possible PySide6 application.
- Open a window.
- Close the window successfully.

### Success Criteria

You can run:

```powershell
python main.py
```

and a PySide6 window opens.

### Git checkpoint

Commit the working initial project.

---

# Phase 2 — Learn Basic Qt Window Structure

## Goal

Understand how a PySide6 application is structured.

Build a basic:

```text
QApplication
     ↓
QMainWindow
     ↓
Central Widget
     ↓
Layout
```

Learn:

- widgets
- layouts
- parent/child relationships
- signals and slots

Do not worry about making it beautiful yet.

### Success Criteria

You understand:

- what creates the application
- what creates the window
- where widgets live
- how layouts position widgets
- how a button emits an event

---

# Phase 3 — Build the Three-Section Layout

## Goal

Create the basic application structure.

Implement:

```text
File Section | View Section
              -------------
              Play Section
```

Use Qt layouts/splitters so the sections resize correctly.

Add temporary placeholder labels/buttons.

### Success Criteria

The application visually resembles the wireframe.

No audio functionality yet.

---

# Phase 4 — Build the File Tree

## Goal

Get the filesystem into the application.

Implement:

- Choose Folder button
- native folder dialog
- root directory selection
- recursive directory scanning
- supported-file filtering
- folder filtering
- tree display

At this stage, use test folders containing fake/simple audio files if necessary.

### Success Criteria

You can select:

```text
D:\Sound Effects
```

and see its valid folder/audio structure.

Unsupported files are invisible.

Folders without supported audio are invisible.

---

# Phase 5 — Implement Tree Selection

## Goal

Make the tree behave correctly before adding audio.

Implement:

- selecting files
- selecting folders
- folder expansion
- folder collapsing
- Enter behavior
- selection state

Test with:

```text
Folder
├── File
├── File
└── Subfolder
    └── File
```

### Success Criteria

You can navigate the tree with the mouse and understand exactly what the selected item is.

---

# Phase 6 — Implement Keyboard Navigation

## Goal

Make the application keyboard-driven.

Implement:

- Up
- Down
- Ctrl + Up
- Ctrl + Down
- Enter

Be careful not to fight Qt's native tree behavior unnecessarily.

First understand what `QTreeView` already does.

Then override only the behavior needed for this application's workflow.

### Success Criteria

You can navigate a large tree quickly without the mouse.

This is a major milestone.

---

# Phase 7 — Implement Audio Playback

## Goal

Make selecting an audio file automatically play it.

Start with Qt Multimedia.

Implement:

- load audio
- play
- stop
- pause
- resume
- automatic playback
- stop old audio when selection changes
- no overlapping playback

### Success Criteria

This works:

```text
↓
sound01.wav → plays

↓
sound02.wav → sound01 stops, sound02 plays

↓
sound03.wav → sound02 stops, sound03 plays
```

---

# Phase 8 — Implement Play Controls

## Goal

Add the Play Section.

Implement:

- Previous
- Play/Pause
- Next
- playback progress
- seeking

Connect buttons to the same underlying application logic used by keyboard controls.

Avoid duplicating playback logic.

For example:

```text
Space
  ↓
play_pause()

Play button
  ↓
play_pause()
```

Both should call the same operation.

### Success Criteria

Mouse and keyboard controls produce the same behavior.

---

# Phase 9 — Implement Waveform Generation

## Goal

Display a waveform for the selected audio.

First determine the most reliable way to obtain audio sample data for:

- WAV
- MP3
- AAC
- M4A

Do not assume the playback API also provides waveform sample data.

If necessary, evaluate an audio-decoding library or FFmpeg.

The waveform pipeline should conceptually be:

```text
Selected audio file
        ↓
Decode/read samples
        ↓
Reduce samples
        ↓
Waveform data
        ↓
Custom waveform widget
        ↓
QPainter renders waveform
```

### Success Criteria

Selecting different audio files produces their corresponding waveforms.

---

# Phase 10 — Implement the View Section

## Goal

Combine the selected filename and waveform into the final View Section.

Implement:

- filename
- waveform
- appropriate spacing
- resizing behavior
- empty state when nothing is selected

Example empty state:

```text
Choose a folder to begin
```

or an appropriately minimal equivalent.

### Success Criteria

The View Section always reflects the current selection.

---

# Phase 11 — UI Styling

## Goal

Turn the functional prototype into the intended application.

Only after functionality is working should substantial styling begin.

Implement:

- dark theme
- typography
- spacing
- panel colors
- borders
- selected tree item
- hover states
- buttons
- scrollbar styling
- progress bar
- waveform appearance
- separators
- window proportions

Use Qt Style Sheets where appropriate.

### Design rule

If an element does not improve usability, remove it.

---

# Phase 12 — Keyboard Workflow Refinement

Test the application as though you were actually editing a video.

Use a large real sound library.

Test:

```text
↑
↓
Ctrl + ↑
Ctrl + ↓
Enter
Space
Previous
Next
Seeking
```

Look for:

- unnecessary pauses
- accidental playback
- selection confusion
- navigation that feels slow
- keyboard conflicts
- unexpected folder behavior

This phase is about making the application **fast**, not adding features.

---

# Phase 13 — Real-World Audio Testing

Use real files from your sound library.

Test:

- short WAV
- long WAV
- MP3
- AAC
- M4A
- mono
- stereo
- very quiet audio
- very loud audio
- unusual filenames
- spaces in filenames
- special characters
- large folders
- deeply nested folders
- empty folders
- folders with only unsupported files
- corrupted/unsupported audio

Document any failures before deciding how to solve them.

---

# Phase 14 — Performance Testing

The application is intended for browsing potentially large sound libraries.

Test:

- hundreds of files
- thousands of files
- many nested folders
- large audio files
- rapid keyboard navigation

Pay particular attention to waveform generation.

The application should not freeze every time the user selects a file.

If waveform generation becomes expensive, move that work away from the UI thread using Qt's threading/task mechanisms.

### Success Criteria

Rapid ↑/↓ navigation remains responsive.

---

# Phase 15 — Error Handling

Add clear handling for situations such as:

- folder cannot be read
- audio cannot be loaded
- unsupported codec
- corrupted audio
- waveform cannot be generated
- selected file disappears
- permission errors

Errors should not crash the application.

The UI should communicate problems without becoming cluttered.

---

# Phase 16 — Code Organization Cleanup

Once functionality is complete:

- remove experimental code
- remove duplicate logic
- rename unclear variables/classes
- separate responsibilities
- simplify overly complicated methods
- add useful comments/docstrings
- ensure imports are clean
- verify Git history

Do not refactor everything prematurely.

Refactor after the application's actual behavior is understood.

---

# Phase 17 — Testing

Create a repeatable test checklist.

Test every requirement from this document.

At minimum:

### Files

- [ ] Choose Folder works
- [ ] WAV appears
- [ ] MP3 appears
- [ ] AAC appears
- [ ] M4A appears
- [ ] Unsupported files are hidden
- [ ] Empty/invalid folders are hidden
- [ ] Nested folders display correctly

### Navigation

- [ ] Up works
- [ ] Down works
- [ ] Ctrl + Up works
- [ ] Ctrl + Down works
- [ ] Enter expands folders
- [ ] Enter collapses folders

### Playback

- [ ] Selecting audio automatically plays it
- [ ] Selecting another audio stops the previous audio
- [ ] Audio never overlaps
- [ ] Space pauses
- [ ] Space resumes
- [ ] Space replays finished audio
- [ ] No looping occurs
- [ ] Previous works
- [ ] Next works
- [ ] Progress updates
- [ ] Seeking works

### Visualization

- [ ] Filename updates
- [ ] Waveform updates
- [ ] Waveform corresponds to selected audio

### UI

- [ ] File section is on the left
- [ ] View section is above playback
- [ ] Playback section is bottom-right
- [ ] Sections resize correctly
- [ ] UI remains usable at different window sizes
- [ ] Styling is consistent

### Stability

- [ ] Application doesn't crash when changing folders
- [ ] Application doesn't crash on invalid files
- [ ] Rapid navigation doesn't break playback
- [ ] Large folders remain usable

---

# Phase 18 — Packaging for Windows

Only after V1 is stable.

Install PyInstaller:

```powershell
pip install pyinstaller
```

Create a Windows build.

Test the executable on a machine/environment where Python is not required.

Verify:

- application launches
- PySide6 dependencies are included
- audio playback works
- waveform generation works
- folder selection works
- no development files are required

The final goal is a user-friendly executable such as:

```text
AudioAssetBrowser.exe
```

---

# 19. Git Strategy

Commit after meaningful milestones.

Suggested commits:

```text
Initial project setup
Create PySide6 application window
Build main application layout
Implement folder selection
Implement filesystem tree
Implement tree navigation
Implement keyboard navigation
Implement audio playback
Implement playback controls
Implement waveform generation
Implement view section
Add application styling
Improve performance
Add error handling
Prepare Windows build
Release V1
```

Do not wait until the end to commit.

If a later change breaks something, Git should make it possible to return to a known-working version.

---

# 20. Recommended Project Structure

Start simple and allow the structure to grow naturally.

A likely final structure:

```text
audio-asset-browser/
│
├── src/
│   └── audio_browser/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── app/
│       │   └── application.py
│       │
│       ├── ui/
│       │   ├── main_window.py
│       │   ├── file_browser.py
│       │   ├── view_panel.py
│       │   ├── playback_controls.py
│       │   └── waveform_widget.py
│       │
│       ├── audio/
│       │   ├── audio_player.py
│       │   └── waveform_generator.py
│       │
│       └── filesystem/
│           └── file_system_manager.py
│
├── tests/
│
├── assets/
│
├── .gitignore
├── README.md
├── requirements.txt
└── plan.md
```

Do not create every file immediately.

Create modules when there is enough functionality to justify separating them.

---

# 21. Design Principles to Follow Throughout Development

## Principle 1 — Build functionality before aesthetics

First make it work.

Then make it fast.

Then make it look good.

---

## Principle 2 — Keep the core workflow extremely short

The ideal workflow is:

```text
↓
hear sound
↓
↓
hear next sound
↓
↓
hear next sound
```

Do not add UI steps between these actions.

---

## Principle 3 — Keyboard first

The primary workflow should be optimized for keyboard navigation.

Mouse interaction is secondary.

---

## Principle 4 — Avoid unnecessary dependencies

Every dependency increases complexity.

Start with:

```text
Python
PySide6
```

Add something only when the application actually needs it.

---

## Principle 5 — Don't overengineer

This is a relatively small desktop application.

Use clean separation of responsibilities, but don't create dozens of abstractions just for the sake of architecture.

---

## Principle 6 — Qt's built-in functionality comes first

Before writing custom behavior, determine whether Qt already provides it.

This is particularly important for:

- file dialogs
- tree views
- layouts
- keyboard events
- media playback
- buttons
- progress bars

---

## Principle 7 — Keep UI logic separate from application logic

For example, the button should not contain the entire audio-playing implementation.

Prefer:

```text
Button
   ↓
Application action
   ↓
Audio Player
```

This makes future changes much easier.

---

# 22. V1 Feature Freeze

The first release should contain exactly the following core feature set:

### File Browser

- Choose Folder
- Recursive folder tree
- Filesystem hierarchy
- Supported audio filtering
- WAV
- MP3
- AAC
- M4A
- Folder filtering
- Folder expansion/collapse

### Navigation

- Mouse selection
- Up/Down
- Ctrl + Up/Down folder navigation
- Enter folder expansion/collapse

### Playback

- Automatic playback on audio selection
- Play
- Pause
- Resume
- Replay
- Previous
- Next
- Stop previous audio when changing selection
- No overlapping playback
- No looping
- Seeking

### Visualization

- Filename
- Waveform

### UI

- File Section
- View Section
- Play Section
- Resizable layout
- Modern dark styling

Nothing else is required for V1.

---

# 23. Post-V1 Roadmap

Future features should be added only after V1 is stable.

Potential V2/V3 features:

## Search

Search filenames and potentially folder names.

## Rename

Rename audio files directly from the application.

## Favorites

Add a favorite mechanism and a virtual Favorites section.

## Additional formats

Add formats based on actual use.

## Remember previous session

Remember:

- last root folder
- expanded folders
- selected audio file
- potentially window size

## Advanced waveform features

Potentially:

- playback position overlay
- waveform zoom
- larger waveform interaction

Do not implement these during V1 unless the core requirements change.

---

# 24. How to Use This Plan

This document is the project's reference point.

When making development decisions, ask:

1. Does this help the core audio-browsing workflow?
2. Is it required for V1?
3. Does Qt already provide a solution?
4. Can the feature be implemented without making the architecture unnecessarily complicated?
5. Will it make rapid audio navigation faster or easier?

If the answer is no, defer the feature.

Requirements can change during development. If a better solution is discovered, update this plan rather than letting the implementation and documentation diverge.

---

# 25. Final Development Sequence

The complete sequence is:

```text
1. Install/update tools
        ↓
2. Create Git repository/project
        ↓
3. Create Python virtual environment
        ↓
4. Install PySide6
        ↓
5. Verify basic PySide6 window
        ↓
6. Learn basic Qt widgets/layouts/signals
        ↓
7. Build three-section window
        ↓
8. Build folder-selection workflow
        ↓
9. Build filesystem tree
        ↓
10. Filter folders/files
        ↓
11. Implement tree selection
        ↓
12. Implement ↑ / ↓
        ↓
13. Implement Enter
        ↓
14. Implement Ctrl + ↑ / ↓
        ↓
15. Implement audio playback
        ↓
16. Implement automatic playback
        ↓
17. Implement Space play/pause
        ↓
18. Implement Previous/Next
        ↓
19. Implement progress + seeking
        ↓
20. Implement waveform generation
        ↓
21. Implement waveform widget
        ↓
22. Finish View Section
        ↓
23. Apply final UI styling
        ↓
24. Test with real sound libraries
        ↓
25. Optimize performance
        ↓
26. Add error handling
        ↓
27. Clean/refactor code
        ↓
28. Run complete V1 test pass
        ↓
29. Package with PyInstaller
        ↓
30. Test Windows executable
        ↓
31. Release V1
```

# 26. Definition of Done

V1 is complete when a user can:

1. Launch the application.
2. Choose a folder containing audio assets.
3. See its relevant folder hierarchy.
4. See only supported audio files.
5. Navigate the tree with ↑/↓.
6. Navigate folders with Ctrl + ↑/↓.
7. Expand/collapse folders with Enter.
8. Select an audio file and immediately hear it.
9. Automatically stop the previous sound when navigating.
10. Play/pause with Space.
11. Use Previous/Next controls.
12. Seek through audio.
13. See the selected filename.
14. See a waveform representing the selected audio.
15. Rapidly audition a large collection of sounds without opening individual files.
16. Use the application comfortably as part of a real video-editing/sound-design workflow.

At that point, the application has fulfilled its original purpose.
