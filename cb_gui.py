import os
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Button, Label, filedialog, Scrollbar, RIGHT, Y, LEFT, BOTH, Canvas, TOP, BOTTOM, messagebox, X
from tkinterdnd2 import DND_FILES, TkinterDnD
from cb import merge_comics

class ComicMergerApp:
    def __init__(self, master):
        self.master = master
        master.title("Çizgi Roman Birleştirici")
        master.geometry("850x420")
        master.configure(bg='#f0f0f0')

        self.comic_files = []
        self.cover_image = None
        self.cover_thumbnail = None
        self.drag_start_index = None
        self.drag_start_y = None
        self.dragged_item = None

        # Ana çerçeve
        self.frame = Frame(master, bg='#f0f0f0')
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Sol panel - dosya listesi
        self.left_frame = Frame(self.frame, bg='#f0f0f0')
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.label = Label(self.left_frame, text=".cbz / .cbr dosyalarını ekle", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        self.label.pack(pady=(0, 5))

        # Dosya listesi için container
        self.list_container = Frame(self.left_frame, bg='white', highlightthickness=1, highlightbackground='#ddd')
        self.list_container.pack(fill=BOTH, expand=True)

        # Canvas ve scrollbar için container
        self.canvas_container = Frame(self.list_container, bg='white')
        self.canvas_container.pack(side=LEFT, fill=BOTH, expand=True)

        # Canvas ve scrollbar
        self.list_canvas = Canvas(self.canvas_container, bg='white', highlightthickness=0)
        self.scrollbar = Scrollbar(self.canvas_container, orient="vertical", command=self.list_canvas.yview)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.list_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Dosya listesi için frame
        self.files_frame = Frame(self.list_canvas, bg='white')
        self.list_canvas.create_window((0, 0), window=self.files_frame, anchor='nw', width=self.list_canvas.winfo_width())

        # Sürükle-bırak için gerekli bağlantılar
        self.list_canvas.drop_target_register(DND_FILES)
        self.list_canvas.dnd_bind('<<Drop>>', self.add_files_dnd)

        # Dosya ekleme butonu
        self.add_button = Button(self.left_frame, text="+ Dosya Ekle", 
                               command=self.add_files_dialog,
                               bg='#4CAF50', fg='white',
                               font=('Arial', 9, 'bold'),
                               relief='flat',
                               padx=15, pady=5)
        self.add_button.pack(pady=10)

        # Sağ panel - kapak ve kontroller
        self.right_frame = Frame(self.frame, bg='#f0f0f0')
        self.right_frame.pack(side=RIGHT, fill=Y, padx=10)

        self.cover_label = Label(self.right_frame, text="Kapak Önizleme", 
                               bg='#f0f0f0', font=('Arial', 10, 'bold'))
        self.cover_label.pack()

        self.cover_canvas = Canvas(self.right_frame, width=200, height=280, bg='white',
                           highlightthickness=1, highlightbackground='#ddd')
        self.cover_canvas.pack(pady=5)

        self.cover_button = Button(self.right_frame, text="Kapak Resmi Seç",
                                 command=self.select_cover_image,
                                 bg='#2196F3', fg='white',
                                 font=('Arial', 9, 'bold'),
                                 relief='flat',
                                 padx=15, pady=5)
        self.cover_button.pack(pady=5)

        self.merge_button = Button(self.right_frame, text="CBZ Olarak Birleştir",
                                 command=self.merge,
                                 bg='#FF9800', fg='white',
                                 font=('Arial', 9, 'bold'),
                                 relief='flat',
                                 padx=15, pady=5)
        self.merge_button.pack(pady=10)

        self.status = Label(self.right_frame, text="", fg="green",
                          bg='#f0f0f0', font=('Arial', 9))
        self.status.pack()

        # Canvas yeniden boyutlandırma için bağlantılar
        self.files_frame.bind('<Configure>', self.on_frame_configure)
        self.list_canvas.bind('<Configure>', self.on_canvas_configure)

    def on_frame_configure(self, event=None):
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Canvas genişliğini frame genişliğine ayarla
        self.list_canvas.itemconfig(self.list_canvas.find_withtag("all")[0], width=event.width)

    def update_file_list(self):
        # Mevcut dosya öğelerini temizle
        for widget in self.files_frame.winfo_children():
            widget.destroy()

        # Yeni dosya öğelerini ekle
        for i, file in enumerate(self.comic_files):
            file_frame = Frame(self.files_frame, bg='white', height=30)
            file_frame.pack(fill=X, padx=5, pady=2)
            file_frame.pack_propagate(False)  # Sabit yükseklik için

            # Dosya adı etiketi
            file_label = Label(file_frame, text=os.path.basename(file), 
                  bg='white', font=('Arial', 9))
            file_label.pack(side=LEFT, fill=X, expand=True, padx=5)

            # Silme butonu
            delete_btn = Button(file_frame, text="×", 
                   command=lambda idx=i: self.remove_file(idx),
                   bg='#ff4444', fg='white',
                   font=('Arial', 9, 'bold'),
                   relief='flat',
                   width=2,
                   height=1)
            delete_btn.pack(side=RIGHT, padx=5, pady=2)

            # Aşağı ok butonu
            down_btn = Button(file_frame, text="↓",
                            command=lambda idx=i: self.move_file_down(idx),
                            bg='#2196F3', fg='white',
                            font=('Arial', 9, 'bold'),
                            relief='flat',
                            width=2)
            down_btn.pack(side=RIGHT, padx=2)

            # Yukarı ok butonu
            up_btn = Button(file_frame, text="↑",
                          command=lambda idx=i: self.move_file_up(idx),
                          bg='#2196F3', fg='white',
                          font=('Arial', 9, 'bold'),
                          relief='flat',
                          width=2)
            up_btn.pack(side=RIGHT, padx=2)

            # Hover efekti
            file_frame.bind('<Enter>', lambda e, f=file_frame: f.configure(bg='#f0f0f0'))
            file_frame.bind('<Leave>', lambda e, f=file_frame: f.configure(bg='white'))

    def move_file_up(self, index):
        if index > 0:
            # Dosyayı yukarı taşı
            self.comic_files[index], self.comic_files[index-1] = self.comic_files[index-1], self.comic_files[index]
            self.update_file_list()

    def move_file_down(self, index):
        if index < len(self.comic_files) - 1:
            # Dosyayı aşağı taşı
            self.comic_files[index], self.comic_files[index+1] = self.comic_files[index+1], self.comic_files[index]
            self.update_file_list()

    def remove_file(self, index):
        if 0 <= index < len(self.comic_files):
            self.comic_files.pop(index)
            self.update_file_list()

    def add_files_dnd(self, event):
        files = self.master.tk.splitlist(event.data)
        self._add_files(files)

    def add_files_dialog(self):
        files = filedialog.askopenfilenames(filetypes=[("Comic files", "*.cbz *.cbr")])
        self._add_files(files)

    def _add_files(self, files):
        for file in files:
            if file.lower().endswith((".cbz", ".cbr")) and file not in self.comic_files:
                self.comic_files.append(file)
                self.update_file_list()

    def select_cover_image(self):
        path = filedialog.askopenfilename(title="Kapak Seç", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.cover_image = path
            self.update_cover_preview()

    def update_cover_preview(self):
        image = Image.open(self.cover_image)
        image.thumbnail((200, 280))
        self.cover_thumbnail = ImageTk.PhotoImage(image)
        self.cover_canvas.create_image(100, 140, image=self.cover_thumbnail)

    def merge(self):
        if not self.comic_files or not self.cover_image:
            messagebox.showerror("Hata", "Lütfen dosyaları ve kapak resmini seçin!")
            return

        suggestion = os.path.splitext(os.path.basename(self.comic_files[0]))[0] + ".cbz"
        output_cbz = filedialog.asksaveasfilename(defaultextension=".cbz", initialfile=suggestion, filetypes=[("CBZ", "*.cbz")])
        if not output_cbz:
            return

        try:
            merge_comics(self.comic_files, self.cover_image, output_cbz)
            self.status.config(text=f"Başarıyla oluşturuldu: {os.path.basename(output_cbz)}", fg="green")
            messagebox.showinfo("Başarılı", f"Dosya başarıyla oluşturuldu:\n{os.path.basename(output_cbz)}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ComicMergerApp(root)
    root.mainloop()
