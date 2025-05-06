def show_vocab_lookup(user_name):
    import tkinter as tk
    import sqlite3
    from modules.menu import show_menu
    from modules.vocab_add import show_vocab_add
    from modules.db_helper import get_db_path

    win = tk.Tk()
    def center_window(win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        win.geometry(f"{width}x{height}+{x}+{y}")
    center_window(win, 750, 500)
    win.title("Tra từ vựng")
    win.geometry("750x500")
    win.configure(bg="#f7f9fa")

    tk.Label(win, text=f"🔍 Xin chào {user_name}, hãy nhập từ cần tra:", font=("Arial", 14), bg="#f7f9fa").pack(pady=20)

    mode_var = tk.StringVar(value="jp")
    mode_frame = tk.Frame(win, bg="#f7f9fa")
    tk.Radiobutton(mode_frame, text="Tra từ Nhật → Việt", variable=mode_var, value="jp", bg="#f7f9fa", font=("Arial", 11)).pack(side="left", padx=10)
    tk.Radiobutton(mode_frame, text="Tra từ Việt → Nhật", variable=mode_var, value="vn", bg="#f7f9fa", font=("Arial", 11)).pack(side="left", padx=10)
    mode_frame.pack(pady=10)

    entry_word = tk.Entry(win, font=("Arial", 14), width=35)
    entry_word.pack(pady=10)

    result = tk.Label(win, text="", font=("Arial", 12), fg="#2c3e50", bg="#f7f9fa")
    result.pack(pady=20)

    def tra_tu():
        word = entry_word.get().strip()
        if not word:
            result.config(text="⚠️ Vui lòng nhập từ cần tra")
            return

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        if mode_var.get() == "jp":
            cursor.execute("SELECT japanese, romaji, meaning FROM Words WHERE japanese = ?", (word,))
        else:
            cursor.execute("SELECT japanese, romaji, meaning FROM Words WHERE meaning LIKE ?", (f"%{word}%",))

        row = cursor.fetchone()
        conn.close()

        if row:
            result.config(text=f"Từ: {row[0]}\nRomaji: {row[1]}\nNghĩa: {row[2]}")
        else:
            result.config(text="❌ Không tìm thấy từ trong cơ sở dữ liệu.")

    tk.Button(win, text="Tra từ", font=("Arial", 12), bg="#27ae60", fg="white", command=tra_tu).pack(pady=10)

    tk.Button(win, text="⬅ Quay lại menu", font=("Arial", 11), bg="#dfe6e9", command=lambda: (win.destroy(), show_menu(user_name))).pack(pady=10)

    tk.Button(win, text="➕ Thêm từ mới", font=("Arial", 11), bg="#a29bfe", fg="white", command=lambda: (win.destroy(), show_vocab_add(user_name))).pack(pady=5)

    win.mainloop()
