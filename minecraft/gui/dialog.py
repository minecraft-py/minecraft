# Show native dialog using tkinter.
# Copy from pyglet example and make some changes.

from os.path import curdir
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, colorchooser, filedialog
from tkinter.commondialog import Dialog as TkDialog

from minecraft import assets
from pyglet.event import EventDispatcher


class DialogBase(EventDispatcher):
    _executor = ThreadPoolExecutor(max_workers=1)
    _dialog = None

    @staticmethod
    def _show_dialog(dialog: TkDialog):
        root = Tk()
        root.withdraw()
        return dialog.show()

    def show(self):
        future = self._executor.submit(self._show_dialog, self._dialog)
        future.add_done_callback(self._callback)

    def _callback(self, future):
        raise NotImplementedError


class ColorChooserDialog(DialogBase):
    def __init__(self, title=None, initialcolor=(255, 255, 255)):
        self._dialog = colorchooser.Chooser(
            title=title or assets.translate("gui.dialog.color_chooser"),
            initialcolor=initialcolor,
        )

    def _callback(self, future):
        self.dispatch_event("on_return", future.result())

    def on_return(self, color):
        pass


class FileOpenDialog(DialogBase):
    def __init__(
        self,
        title=None,
        initial_dir=curdir,
        filetypes=None,
        multiple=False,
    ):
        self._dialog = filedialog.Open(
            title=title or assets.translate("gui.dialog.file_open"),
            initialdir=initial_dir,
            filetypes=filetypes or (),
            multiple=multiple,
        )

    def _callback(self, future):
        self.dispatch_event("on_return", future.result())

    def on_return(self, filenames):
        pass


class SaveAsDialog(DialogBase):
    def __init__(
        self,
        title=None,
        initial_dir=curdir,
        initial_file=None,
        filetypes=None,
        default_ext="",
    ):
        self._dialog = filedialog.SaveAs(
            title=title or assets.translate("gui.dialog.save_as"),
            initialdir=initial_dir,
            initialfile=initial_file or (),
            filetypes=filetypes or (),
            defaultextension=default_ext,
        )

    def _dispatch_event(self, future):
        self.dispatch_event("on_return", future.result())

    def on_return(self, filename):
        pass


ColorChooserDialog.register_event_type("on_return")
FileOpenDialog.register_event_type("on_return")
SaveAsDialog.register_event_type("on_return")


__all__ = "BaseDialog", "ColorChooserDialog", "FileOpenDialog", "SaveAsDialog"
