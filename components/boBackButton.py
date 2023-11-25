import gi
import math
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class GoBackButton(Gtk.EventBox):
    def __init__(self , stack ) : 
        super().__init__()

        self.radius = 15
        self.color = (0.8, 0.8, 0.8)

        # Connect the draw signal
        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cairo_context):
        allocation = widget.get_allocation()

        # Draw a rounded rectangle with the specified radius and color
        cairo_context.set_source_rgb(*self.color)
        cairo_context.move_to(self.radius, 0)
        cairo_context.arc(self.radius, self.radius, self.radius, 1.5 * math.pi, 2 * math.pi)
        cairo_context.arc(allocation.width - self.radius, self.radius, self.radius, 0, 0.5 * math.pi)
        cairo_context.arc(allocation.width - self.radius, allocation.height - self.radius, self.radius, 0.5 * math.pi, math.pi)
        cairo_context.arc(self.radius, allocation.height - self.radius, self.radius, math.pi, 1.5 * math.pi)
        cairo_context.close_path()
        cairo_context.fill_preserve()

        # Draw a border
        cairo_context.set_source_rgb(0, 0, 0)
        cairo_context.set_line_width(2)
        cairo_context.stroke()