from tkinter import ttk
import tkinter as tk
class scroll_event:
    def __init__(self):
        pass
    def _update_scrollbar(self,canvas,scrollbar):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        bbox = canvas.bbox("all")
        if bbox:
            content_height = bbox[3] - bbox[1]
            canvas_height = canvas.winfo_height()

            if content_height <= canvas_height:
                # Ẩn scrollbar
                if scrollbar.winfo_ismapped():
                    scrollbar.pack_forget()
                self._unbind_mousewheel(canvas)
            else:
                # Hiện scrollbar
                if not scrollbar.winfo_ismapped():
                    scrollbar.pack(side=tk.RIGHT, fill="y")
                # Bật scroll cho canvas
                self._activate_mousewheel(canvas)
                
    def _bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda e: self._activate_mousewheel(widget))
        widget.bind("<Leave>", lambda e: self._deactivate_mousewheel(widget))

    def _activate_mousewheel(self, widget, event=None):
        widget.bind("<MouseWheel>", lambda e: self._on_mousewheel(widget, e))

    def _deactivate_mousewheel(self, widget, event=None):
        widget.unbind("<MouseWheel>")

    def _on_mousewheel(self, widget, event):
        widget.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"
    def _unbind_mousewheel(self, widget): 
        widget.unbind("<MouseWheel>")