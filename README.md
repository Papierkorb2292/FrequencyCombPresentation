# Frequency Comb Presentation (German)

This repo features a collection of animations used for a short presentationa about frequency combs.
Those animations (under `media/videos/main/1080p60`) are made with manim and their code can be found in `main.py`.

All texts in the animations are currently in german!

The animations are meant to be played in the following order:
- `CWLaser.mp4`, this animation shows the electric field of a constant wave laser, to set up a comparison to a pulse laser
- `PulseLaser.mp4`, this animation shows the electric field of a pulse laser. Here, the presentor can mention that, by only by looking at the graph, it seems like the pulses only have one constant wavelength, to set up the next animations, which show how the pulse is composed of a frequency comb.
- `Spectrogram.mp4`, this animation shows the frequency comb of the pulses from the previous scene.
- `Superposition.mp4`, this animation shows that the pulses from earlier are indeed a superposition of the waves of the previously shown frequency comb, by adding the waves together one after another.
- `UnknownWaveFrequency.mp4`, to explain how a frequency comb can be used to measure frequencies, this animation introduces a wave of an unknown frequency (which lies slighly below the highest spike of the frequency comb).
- `DetermineFrequency.mp4`, this animation shows the beat of the wave of unknown frequency and the frequency comb wave. After zooming out, the frequency of the beat of the wave of unknown frequency and the wave of the highest comb spike can be determined.
- `CalculateFrequency.mp4`, this animation shows the calculations necessary to calculate the unknown frequency based of the known frequency of the comb spike and based of the measured beat frequency.