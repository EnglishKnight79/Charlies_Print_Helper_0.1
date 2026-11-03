#!/usr/bin/env python3
# Charlies Print Helper - GIMP 3.x plug-in (Python 3)
# Menu: Filters > Charlies Print Helper...

import math
import sys

import gi
gi.require_version("Gimp", "3.0")
gi.require_version("GimpUi", "3.0")
gi.require_version("Gegl", "0.4")
from gi.repository import Gimp, GimpUi, Gegl, GObject, GLib  # noqa: E402

PROC_NAME = "madison-seamless-poster"
MAX_TILES = 600  # safety limit so GIMP doesn't choke

INTRO = (
    "Turns the open image into a seamless pattern and repeats it to fill "
    "a poster. Your original image is not changed. When it finishes, a new "
    "image opens: use File, Export As to save it for printing."
)
HELP = {
    "make-seamless": (
        "Blends the edges so the repeats join with no visible line. "
        "Leave ticked unless your image is already seamless."
    ),
    "tile-cm": (
        "How wide ONE copy of your image will look on the finished print. "
        "Smaller = more repeats and a finer pattern. Larger = fewer, bigger repeats."
    ),
    "poster-width-cm": "Width of the finished print, in centimetres (300 = 3 metres).",
    "poster-height-cm": "Height of the finished print, in centimetres.",
    "dpi": (
        "Print sharpness. 100 is fine for big posters viewed from a distance. "
        "Higher looks sharper up close but makes a much bigger, slower file."
    ),
}


class CharliesPrintHelper(Gimp.PlugIn):
    def do_query_procedures(self):
        return [PROC_NAME]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        proc = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )
        proc.set_image_types("*")
        proc.set_menu_label("Charlies Print Helper...")
        proc.add_menu_path("<Image>/Filters")
        proc.set_documentation(
            "Make the image seamless and tile it to a poster size",
            INTRO,
            name,
        )
        proc.set_attribution("Author", "Author", "2026")

        flags = GObject.ParamFlags.READWRITE
        proc.add_boolean_argument(
            "make-seamless", "Make edges seamless", HELP["make-seamless"], True, flags)
        proc.add_double_argument(
            "tile-cm", "One repeat size (cm)", HELP["tile-cm"], 1.0, 500.0, 30.0, flags)
        proc.add_double_argument(
            "poster-width-cm", "Poster width (cm)", HELP["poster-width-cm"],
            1.0, 1000.0, 300.0, flags)
        proc.add_double_argument(
            "poster-height-cm", "Poster height (cm)", HELP["poster-height-cm"],
            1.0, 1000.0, 100.0, flags)
        proc.add_int_argument(
            "dpi", "Print resolution (DPI)", HELP["dpi"], 30, 600, 100, flags)
        return proc

    def _show_dialog(self, procedure, config):
        GimpUi.init(PROC_NAME)
        dialog = GimpUi.ProcedureDialog(procedure=procedure, config=config)
        dialog.set_title("Charlies Print Helper")

        def note(label_id, text):
            lbl = dialog.get_label(label_id, text, True, False)
            try:
                lbl.set_markup("<i>%s</i>" % text)
                lbl.set_line_wrap(True)
                lbl.set_xalign(0.0)
                lbl.set_max_width_chars(60)
            except Exception:
                pass  # cosmetic only

        note("intro", INTRO)
        order = ["intro"]
        for prop in ["make-seamless", "tile-cm", "poster-width-cm",
                     "poster-height-cm", "dpi"]:
            note("help-" + prop, HELP[prop])
            order += [prop, "help-" + prop]

        dialog.fill(order)
        ok = dialog.run()
        dialog.destroy()
        return ok

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            if not self._show_dialog(procedure, config):
                return procedure.new_return_values(
                    Gimp.PDBStatusType.CANCEL, GLib.Error())

        make_seamless = config.get_property("make-seamless")
        tile_cm = config.get_property("tile-cm")
        poster_w_cm = config.get_property("poster-width-cm")
        poster_h_cm = config.get_property("poster-height-cm")
        dpi = config.get_property("dpi")

        px_per_cm = dpi / 2.54
        tile_w = max(1, int(round(tile_cm * px_per_cm)))
        poster_w = max(1, int(round(poster_w_cm * px_per_cm)))
        poster_h = max(1, int(round(poster_h_cm * px_per_cm)))

        # Keep the tile's aspect ratio (tile_cm is the width of one repeat)
        aspect = image.get_height() / image.get_width()
        tile_h = max(1, int(round(tile_w * aspect)))

        nx = math.ceil(poster_w / tile_w)
        ny = math.ceil(poster_h / tile_h)
        if nx * ny > MAX_TILES:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error("Too many repeats (%d). Make one repeat bigger." % (nx * ny)),
            )

        Gimp.progress_init("Building poster texture...")

        # 1. Work on a flattened copy so the original is untouched
        work = image.duplicate()
        work.undo_disable()
        work.flatten()
        layer = work.get_layers()[0]

        # 2. Seamless edges
        if make_seamless:
            filt = Gimp.DrawableFilter.new(layer, "gegl:tile-seamless", "Seamless")
            layer.append_filter(filt)
            layer.merge_filter(filt)

        # 3. Scale one repeat to its physical print size
        layer.scale(tile_w, tile_h, False)

        # 4. Tile it across a poster-sized canvas
        out = Gimp.Image.new(poster_w, poster_h, Gimp.ImageBaseType.RGB)
        out.undo_disable()
        total = nx * ny
        done = 0
        for ix in range(nx):
            for iy in range(ny):
                copy = Gimp.Layer.new_from_drawable(layer, out)
                out.insert_layer(copy, None, 0)
                copy.set_offsets(ix * tile_w, iy * tile_h)
                done += 1
                Gimp.progress_update(done / total)

        out.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
        out.set_resolution(dpi, dpi)
        out.undo_enable()

        work.delete()
        Gimp.Display.new(out)
        Gimp.displays_flush()
        Gimp.progress_end()

        return procedure.new_return_values(
            Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(CharliesPrintHelper.__gtype__, sys.argv)
