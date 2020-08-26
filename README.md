# ThumpAV

Thump is a free VJ studio / generative visuals rig, built in TouchDesigner. It intends to encourage improvosation while providing tools for continuous streaming and playback as a media server.

## Instructions
- Download or clone this repository (clone recommended for updates)
- Install latest version of [TouchDesigner](https://derivative.ca/) (free-license compatible) and open `app.toe`
![File explorer](https://i.imgur.com/MdNckUI.png)
- Enter perform mode (`key=f1`) and visit the `settings` page to adjust resolution, audio inputs / outputs, recording preferences, and more.

# How to use
![UI and stage layout](https://i.imgur.com/wKdergz.png)
## Main UI
![Labelled UI area](https://i.imgur.com/34I5qbO.png)
1. Track output monitoring area
    * a) Blue outline indicates track is hidden
2. Track control sliders
    * a) Opacity
    * b) Speed (0-3x source playback speed) \*Right click to reset at 1
    * c) Volume \*For tracks playing back clips with audio
3. Track control buttons
    * a) Mute \*For clips with audio
    * b) Blind \*Hides track by overriding opacity at 0
    * c) Stage FX
    Click to view and edit plugin settings in the FX staging area (8b.)
    * d) Loop (video)
    * e) Pulse (video)
4. Cell
    * a) Displays thumbnail for track media at associated cue (5.)
    * b) Clicking cell sets its file as source media for associated track
    * c) Drag and drop cell onto track monitors (1.) to set as source media for that track
    * d) Drop images or videos from file system into cell to immediately write to cue
5. Cue launch button
    * a) Plays cue from disk - updates all Track controls and Plugin settings to saved state
6. Cue edit (delete, add above/below)
7. *SAVE BUTTON* Writes all current Track controls and Plugin settings to currently active cue (highlighted with blue)
8. Dashboard tabs
    * a) Setlist: table of contents for scenes in Source Directory. Create your own Source Directory and point Thump to it under the Settings tab!
    * b) FX: View/edit Plugin settings for currently staged track (3c.)
    * c) FX Bin: Plugin library. Create your own and point to it under the Settings tab
    * d) Settings: Resolution, Recording, Audio in/out, Source Directory, Plugin Directory, FPS Monitor, Project Mapping (Stoner), NDI
9. Launch neighbor of active cue
10. Page up/down through scene cues

## Audio
- Necessary to identify input for audio-reactive visualizations
- Under settings tab, set the input/output device. Common setup involves [VB-Cable](https://www.vb-audio.com/Cable/) or [Soundflower](https://github.com/mattingalls/Soundflower/releases) as virtual input device and playing back out of physical device

## Recording
...

## MIDI
- Custom mappings can be added through TouchDesigner [MIDI mapping workflow](https://www.youtube.com/watch?v=XLeghJmFBh0)
- Templates located in `/local/midi/`. As of writing, Akai MPD218 is the sole mapping included in source. If you have a device mapping you'd like to contribute, please message / PR!

## Plugins
- Detailed plugin creation guide coming soon
- You can get started building your own VFX plugins by clicking "Create New" under the FX Bin tab
- In principle, any TouchDesigner component can be turned into a plugin if it contains an In TOP, an Out TOP, and the boilerplate Plugin extension (can be modified for custom Saving, Loading, and other behavior)
- Check out included plugins for guidance / inspiration :rocket:
