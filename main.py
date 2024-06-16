from manim import *

def update_graph(graph: FunctionGraph):
    graph.clear_points()
    graph.generate_points()

class CWLaser(Scene):
    def construct(self):
        self.play(Create(Text("Dauerstrichlaser:", z_index=1).shift(UP*3.5)))
        time = ValueTracker(0)
        self.add(time)
        laser_func = FunctionGraph(
            lambda x: np.sin(x - time.get_value()),
            color=RED
        )
        laser_func.add_updater(update_graph)
        plane = NumberPlane()
        time.add_updater(lambda m, dt: m.increment_value(3*dt))
        self.play(FadeIn(plane), Create(laser_func), FadeIn(NumberPlane()), FadeIn(Text("E").shift(LEFT*0.5+UP*2.5)), FadeIn(Text("x").shift(RIGHT*6.5+DOWN*0.5)))
        self.wait(10)

class PulseLaser(Scene):
    def construct(self):
        self.play(Create(Text("Pulslaser:", z_index=1).shift(UP*3.5)))
        time = ValueTracker(-5)
        self.add(time)
        laser_func = FunctionGraph(
            lambda x: np.sum([np.sin(f*(x - time.get_value()))*np.exp(np.square(7-f)/-2) if np.mod((x - time.get_value())+PI, 4*PI) < 2*PI else 0 for f in range(5,10)]),
            color=RED
        )
        laser_func.add_updater(update_graph)
        plane = NumberPlane()
        time.add_updater(lambda m, dt: m.increment_value(6*dt))
        self.play(FadeIn(plane), Create(laser_func), FadeIn(Text("E").shift(LEFT*0.5+UP*2.5)), FadeIn(Text("x").shift(RIGHT*6.5+DOWN*0.5)))
        self.wait((10*2*PI+5)/6-1)
        time.set_value(0)
        time.clear_updaters()
        self.wait(0)

comb_spike_colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
def generateSpectrogramSpike(n: int) -> Rectangle:
    rect = Rectangle(width=0.5, height=5*np.exp(-np.square(7-n)), fill_color=comb_spike_colors[n-5], fill_opacity=1, stroke_width=0)
    rect.shift(RIGHT*(n-3)+rect.height/2*UP)
    return rect

def calcWaveForFrequency(f: int, color = None, **kwargs) -> FunctionGraph:
    if color is None:
        color = comb_spike_colors[f-5]
    return FunctionGraph(
        lambda x: np.sin(f*x)*np.exp(np.square(7-f)/-2),
        color=color,
        **kwargs
    )

def add_spectrogram(scene: Scene):
    spectrogram_plane = NumberPlane(x_range=(
        -config["frame_x_radius"]+3,
        config["frame_x_radius"]+3,
        1,
    ), y_range=(
        -config["frame_y_radius"]+3,
        config["frame_y_radius"]+3,
        1,
    ))
    scene.add(spectrogram_plane)
    scene.add(Rectangle(
        height=spectrogram_plane.get_y_range()[1]-spectrogram_plane.get_y_range()[0]+0.2,
        width=spectrogram_plane.get_x_range()[1]-spectrogram_plane.get_x_range()[0]+0.2,
        z_index=-1,
        fill_opacity=1,
        fill_color=BLACK,
        stroke_width=3
    ))
    scene.add(Text("I").shift(LEFT*3.5+UP*3.5))
    scene.add(MathTex(r"\frac{f}{Hz}").shift(RIGHT*6.5+DOWN*3.5))
    comb_spikes = [generateSpectrogramSpike(n) for n in range(5,10)]
    comb_spikes_group = VGroup(*comb_spikes).shift(3*DOWN)
    scene.add(comb_spikes_group)

class Spectrogram(Scene):
    def construct(self):
        add_spectrogram(self)
        self.mobjects[-1].rotate(PI/2, LEFT, about_point=DOWN*3)
        self.play(Rotate(self.mobjects[-1], angle=-PI/2, axis=LEFT, about_point=DOWN*3))


class Superposition(Scene):
    def construct(self):
        add_spectrogram(self)

        spectrogram_objects = self.mobjects[:4]
        comb_spikes = self.mobjects[-1].submobjects

        for o in self.mobjects:
            o.set_z_index(o.get_z_index()+10)

        self.play(*[o.animate.scale(0.35, about_point=ORIGIN).shift(UP*2.5+RIGHT*4.5) for o in self.mobjects])

        self.play(FadeIn(NumberPlane(x_range=(
            -config["frame_x_radius"],
            config["frame_x_radius"],
            2*PI,
        ))), FadeIn(Text("E").shift(LEFT*0.5+UP*3.5)), FadeIn(MathTex(r"\frac{t}{s}").shift(RIGHT*6.5+DOWN*0.5)))
        prev_wave = calcWaveForFrequency(7)
        prev_wave_function = prev_wave.function
        spike = comb_spikes[2]
        self.play(Transform(spike, prev_wave))
        self.remove(spike)
        self.add(prev_wave)
        self.wait(1)
        additional_frequencies = [6,8,5,9]
        for f in additional_frequencies:
            prev_wave.set_z_index(0)
            wave = calcWaveForFrequency(f)
            wave.set_z_index(1)
            spike = comb_spikes[f-5]
            self.play(Transform(spike, wave))
            self.remove(spike)
            self.add(wave)
            sum_wave = FunctionGraph(
                lambda x,wave=wave,prev_wave=prev_wave: prev_wave.function(x)[1] + wave.function(x)[1],
                color=wave.color
            )
            sum_wave.set_z_index(1)
            self.wait(1)
            self.play(Transform(wave, sum_wave))
            self.remove(wave)
            self.play(AnimationGroup(FadeToColor(sum_wave, WHITE), FadeOut(prev_wave)))
            prev_wave = sum_wave
        self.play(*[FadeOut(o) for o in spectrogram_objects])

# This scene sets up a new wave whose frequency is supposed to be determined accurately
# The only thing known about the frequency is that it is slightly below the 7Hz comb spike
class UnknownWaveFrequency(Scene):
    def construct(self):
        add_spectrogram(self)

        yellow_spike = self.mobjects[-1].submobjects[2]

        wave_frequenvy_indicator_wiggle = ValueTracker(0)
        wave_frequenvy_indicator_wiggle.add_updater(lambda m, dt: m.increment_value(2*dt))
        self.add(wave_frequenvy_indicator_wiggle)
        
        wave_frequency_indicator = Line(ORIGIN, UP*6, color=RED).shift(DOWN*3)
        wave_frequency_indicator.add_updater(lambda m: m.set_x(0.25*np.sin(wave_frequenvy_indicator_wiggle.get_value()) + 3.75))

        frequency_equation = MathTex(r"f=?")

        frequency_equation.add_updater(lambda m: m.next_to(wave_frequency_indicator, UP))

        self.play(Create(wave_frequency_indicator), Create(frequency_equation))
        self.wait(4)
        self.play(Create(MathTex(r"f_{spitze}=7Hz", color=YELLOW).next_to(yellow_spike, DOWN)))
        self.wait(4)


class DetermineFrequency(Scene):
    def construct(self):
        # Setup ending state of Scene "Superposition"
        plane = NumberPlane(x_range=(-40,40,2*PI)).shift(OUT)
        self.add(plane, Text("E").shift(LEFT*0.5+UP*3.5), MathTex(r"\frac{t}{s}").shift(RIGHT*6.5+DOWN*0.5))
        frequency_comb = FunctionGraph(
            lambda x: np.sum([np.sin(f*x)*np.exp(np.square(7-f)/-2) for f in range(5,10)]),
            color=WHITE
        )
        self.add(frequency_comb)

        # Add a wave of of frequency 6.8 (unknown to the viewer)
        # The frequency is known to be slightly below the 7Hz comb spike
        # The frequency will be determined by measuring the beat frequency of it and the aforementioned comb spike

        unknown_wave = calcWaveForFrequency(6.8, color=RED)
        self.play(Create(unknown_wave))
        
        # Extend unknown_wave to (-40,40)
        self.remove(unknown_wave)
        unknown_wave = calcWaveForFrequency(6.8, color=RED, x_range=(-40,40))
        self.add(unknown_wave)
        self.wait(1)
        # Convert the unknown wave to a beat frequency wave

        beat_wave = FunctionGraph(
            lambda x: unknown_wave.function(x)[1] + frequency_comb.function(x)[1],
            color=RED,
            x_range=(-40,40)
        ).shift(OUT)
        self.play(Transform(unknown_wave, beat_wave))
        self.remove(unknown_wave)
        self.add(beat_wave)
        self.play(FadeToColor(beat_wave, WHITE), FadeOut(frequency_comb))

        # Zoom out to show the beat frequency (Beat repeats at ((7-6.8)/2Pi)^-1 = 10Pi)

        zoom_matrix = [[2/5, 0, -7],
                       [0,   1,  0],
                       [0,   0,  1]]

        self.play(ApplyMatrix(zoom_matrix, plane), ApplyMatrix(zoom_matrix, beat_wave))
        self.wait(5)
        self.play(Create(MathTex(r"f_{Schwebung}=\frac{1}{5}Hz").shift(UP*2.5+LEFT*0.4)))


import sys

if "debug" in sys.argv:
    with tempconfig({"quality": "medium_quality", "disable_caching": True}):
        scene = Spectrogram()
        scene.render()