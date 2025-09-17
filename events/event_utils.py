def bind_mousewheel(widget, target_canvas):
    widget.bind("<Enter>", lambda e: target_canvas.bind("<MouseWheel>", lambda ev: target_canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
    widget.bind("<Leave>", lambda e: target_canvas.unbind("<MouseWheel>"))