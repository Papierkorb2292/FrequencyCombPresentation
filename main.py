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

def calcWaveForFrequency(f: int) -> FunctionGraph:
    return FunctionGraph(
        lambda x: np.sin(f*x)*np.exp(np.square(7-f)/-2),
        color=comb_spike_colors[f-5]
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
    scene.add(Text("f").shift(RIGHT*6.5+DOWN*3.5))
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

        self.play(FadeIn(NumberPlane()), FadeIn(Text("E").shift(LEFT*0.5+UP*3.5)), FadeIn(Text("x").shift(RIGHT*6.5+DOWN*0.5)))
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


import sys

if "debug" in sys.argv:
    with tempconfig({"quality": "medium_quality", "disable_caching": True}):
        scene = Spectrogram()
        scene.render()