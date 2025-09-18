gato_panel.pack(side="left", expand=True, fill="both", padx=20, pady=10)
perro_panel.pack(side="left", expand=True, fill="both", padx=20, pady=10)

style.configure("Sub.TLabel", font=("Segoe UI", 14, "bold"), foreground="#333")
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1d6fb8")

gato_clicker_image_lbl.pack(pady=(10,0), expand=True)
perro_clicker_image_lbl.pack(pady=(10,0), expand=True)

shadow_frame = ttk.Frame(clicker_frame, padding=5, style="Shadow.TFrame")
shadow_frame.place(relx=0.5, rely=0.95, anchor="s")
players_panel.pack(in_=shadow_frame)