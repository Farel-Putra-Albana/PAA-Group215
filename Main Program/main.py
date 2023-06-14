import pygame
import random
import time
import queue
import threading

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
lebar_layar = 1200
tinggi_layar = 680

# Warna
HITAM = (0, 0, 0)
PUTIH = (255, 255, 255)
ABU_ABU = (128, 128, 128)
HIJAU = (0, 255, 0)
MERAH = (255, 0, 0)
CREAM = (254, 250, 224)
COKLAT = (212, 163, 115)

# Ukuran sel dalam labirin
ukuran_sel = 15
lebar_sel = (lebar_layar - 300) // ukuran_sel
tinggi_sel = tinggi_layar // ukuran_sel

# Jarak pandang Droid Hijau
droid_hijau_visibility = 1

droidMerah_tambahan_count = 0
baris_droid_merah = None
kolom_droid_merah = None

# Inisialisasi layar
screen = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Project PAA")
# Membuat dan menggati logo/icon screen
icon = pygame.image.load("Logo.png")
pygame.display.set_icon(icon)

# Membuat grid labirin
labirin = []
for i in range(tinggi_sel):
    labirin.append([1] * lebar_sel)

# Fungsi untuk mengacak posisi tembok
def acak_labirin(baris, kolom):
    arah = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(arah)

    for dx, dy in arah:
        baris_baru = baris + dx
        kolom_baru = kolom + dy

        if baris_baru < 0 or baris_baru >= tinggi_sel or kolom_baru < 0 or kolom_baru >= lebar_sel:
            continue

        if labirin[baris_baru][kolom_baru] == 1:
            labirin[baris_baru][kolom_baru] = 0
            labirin[baris + dx // 2][kolom + dy // 2] = 0
            acak_labirin(baris_baru, kolom_baru)

# Fungsi untuk memastikan semua jalur terhubung satu sama lain
def connect_labirin(baris, kolom):
    arah = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(arah)

    for dx, dy in arah:
        baris_baru = baris + dx
        kolom_baru = kolom + dy

        if baris_baru < 0 or baris_baru >= tinggi_sel or kolom_baru < 0 or kolom_baru >= lebar_sel:
            continue

        if labirin[baris_baru][kolom_baru] == 1:
            labirin[baris_baru][kolom_baru] = 0
            labirin[baris + dx // 2][kolom + dy // 2] = 0
            connect_labirin(baris_baru, kolom_baru)

# ketetanggaan antar baris dan kolom  
def get_neighbors(baris, kolom):
    neighbors = []
    arah = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in arah:
        baris_baru = baris + dx
        kolom_baru = kolom + dy

        if 0 <= baris_baru < tinggi_sel and 0 <= kolom_baru < lebar_sel and labirin[baris_baru][kolom_baru] == 0:
            neighbors.append((baris_baru, kolom_baru))

    return neighbors

# fungsi untuk menggambar labirin
def gambar_labirin():
    for baris in range(tinggi_sel):
        for kolom in range(lebar_sel):
            if pandangan_droidMerah:
                # Jika Pandangan Droid Merah aktif, gambar sel labirin secara normal (tanpa memperhatikan droid hijau)
                if labirin[baris][kolom] == 1 and not (baris == baris_droid_hijau and kolom == kolom_droid_hijau):
                    pygame.draw.rect(screen, HITAM, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))
                else:
                    pygame.draw.rect(screen, PUTIH, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))
            elif pandangan_droidHijau:
                # Jika Pandangan Droid Hijau aktif, gambar sel labirin hanya di sekitar droid hijau
                if abs(baris - baris_droid_hijau) <= droid_hijau_visibility and abs(kolom - kolom_droid_hijau) <= droid_hijau_visibility:
                    if labirin[baris][kolom] == 1 and not (baris == baris_droid_hijau and kolom == kolom_droid_hijau):
                        pygame.draw.rect(screen, HITAM, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))
                    else:
                        pygame.draw.rect(screen, PUTIH, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))
                    # Draw the hijau droid
                    if baris == baris_droid_hijau and kolom == kolom_droid_hijau:
                        gambar_droid(HIJAU, baris, kolom)
            else:
                # Jika Pandangan Droid tidak aktif, gambar sel labirin secara normal
                if labirin[baris][kolom] == 1:
                    pygame.draw.rect(screen, HITAM, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))
                else:
                    pygame.draw.rect(screen, PUTIH, (kolom * ukuran_sel, baris * ukuran_sel, ukuran_sel, ukuran_sel))

def gambar_droid(color, baris, kolom):
    radius = ukuran_sel // 2
    x = kolom * ukuran_sel + radius
    y = baris * ukuran_sel + radius
    pygame.draw.circle(screen, color, (x, y), radius)

def button():
    pygame.draw.rect(screen, COKLAT, (lebar_layar - 300, 0, 300, tinggi_layar))

    font = pygame.font.Font(None, 24)
    labels = ["MULAI", "ACAK DROID", "TAMBAH DROID", "ACAK MAP", "PANDANGAN DROID HIJAU", "", "PANDANGAN DROID MERAH", "KURANGI DROID", "BERHENTI"]

    # Menambahkan tulisan "Menu Permainan"
    judul_font = pygame.font.Font(None, 40)
    judul_text = judul_font.render("Menu Permainan", True, HITAM)
    judul_text_rect = judul_text.get_rect(center=(lebar_layar - 143, 85))
    screen.blit(judul_text, judul_text_rect)
    
    # Menambahkan tulisan "Project PAA 2023" di footer
    judul_font = pygame.font.Font(None, 20)
    judul_text = judul_font.render("Project PAA 2023", True, HITAM)
    judul_text_rect = judul_text.get_rect(center=(lebar_layar - 143, 655))
    screen.blit(judul_text, judul_text_rect)

    for i, label in enumerate(labels):
        kotak_button = pygame.Rect(lebar_layar - 260, 140 + i * 50, 240, 40)
        radius = 15  # Radius sudut rounded rectangle
        if i == 5:
            text_rect = pygame.Rect(lebar_layar - 260, 140 + i * 50, 240, 40)
        elif i == 8:
            pygame.draw.rect(screen, MERAH, kotak_button, border_radius=radius)
        else:
            pygame.draw.rect(screen, CREAM, kotak_button, border_radius=radius)
            pygame.draw.rect(screen, PUTIH, kotak_button, 2, border_radius=radius)
            text_rect = kotak_button

    kotak_button_pandanganDroidMerah = pygame.Rect(lebar_layar - 260, 140 + 6 * 50, 240, 40)
    if pandangan_droidMerah:
        pygame.draw.rect(screen, MERAH, kotak_button_pandanganDroidMerah, border_radius=radius)
    else:
        pygame.draw.rect(screen, CREAM, kotak_button_pandanganDroidMerah, border_radius=radius)
    pygame.draw.rect(screen, PUTIH, kotak_button_pandanganDroidMerah, 2, border_radius=radius)
    pandangan_droidMerah_text = font.render("", True, HITAM)
    pandangan_droidMerah_text_rect = pandangan_droidMerah_text.get_rect(center=kotak_button_pandanganDroidMerah.center)
    screen.blit(pandangan_droidMerah_text, pandangan_droidMerah_text_rect)

    pandangan_droidHijau_kotak_button = pygame.Rect(lebar_layar - 260, 140 + 4 * 50, 240, 40)
    if pandangan_droidHijau:
        pygame.draw.rect(screen, HIJAU, pandangan_droidHijau_kotak_button, border_radius=radius)
    else:
        pygame.draw.rect(screen, CREAM, pandangan_droidHijau_kotak_button, border_radius=radius)
    pygame.draw.rect(screen, PUTIH, pandangan_droidHijau_kotak_button, 2, border_radius=radius)
    pandangan_droidHijau_text = font.render("", True, HITAM)
    pandangan_droidHijau_text_rect = pandangan_droidHijau_text.get_rect(center=pandangan_droidHijau_kotak_button.center)
    screen.blit(pandangan_droidHijau_text, pandangan_droidHijau_text_rect)

    # Sesuaikan posisi teks untuk setiap tombol
    for i, label in enumerate(labels):
        if i == 8:
            text_color = PUTIH  # Set text color to putih for button with index 7
        else:
            text_color = HITAM  # Set text color to hitam for other buttons

        text = font.render(label, True, text_color)
        text_rect = text.get_rect(center=(kotak_button.centerx, 140 + i * 50 + 20))
        screen.blit(text, text_rect)

    pandangan_droidMerah_text_rect = pandangan_droidMerah_text.get_rect(center=(kotak_button_pandanganDroidMerah.centerx, 140 + 5 * 50 + 20))
    screen.blit(pandangan_droidMerah_text, pandangan_droidMerah_text_rect)

    pandangan_droidHijau_text_rect = pandangan_droidHijau_text.get_rect(center=(pandangan_droidHijau_kotak_button.centerx, 140 + 3 * 50 + 20))
    screen.blit(pandangan_droidHijau_text, pandangan_droidHijau_text_rect)

    pygame.draw.rect(screen, HITAM, (lebar_layar - 260, 140 + 5 * 50 + 15, 240, 10), border_radius=radius)
    slider_pos = lebar_layar - 170 + int((droid_hijau_visibility - 2) / 3 * 240)
    pygame.draw.circle(screen, HITAM, (slider_pos, 140 + 5 * 50 + 20), 10)

# Fungsi untuk mengubah jarak pandang droid hijau
def ubah_pandangan_DroidHijau(pos):
    global droid_hijau_visibility

    lebar_slider = 160
    slider_pos = pos[0] - (lebar_layar - 180)
    percentage = slider_pos / lebar_slider
    droid_hijau_visibility = int(percentage * 4) + 2
    
def is_putih_path(baris, kolom):
    return labirin[baris][kolom] == 0

def kurangi_droid():
    global droidMerah_tambahan
    if len(droidMerah_tambahan) > 0:
        droidMerah_tambahan.pop()

# fungsi untuk button acak map
def acak_map():
    global labirin, pandangan_droidHijau, pandangan_droidMerah

    pandangan_droidHijau = False
    pandangan_droidMerah = False

    labirin = []
    for i in range(tinggi_sel):
        labirin.append([1] * lebar_sel)

    acak_labirin(0, 0)
    connect_labirin(0, 0)
    acak_droid()  # Mengacak posisi droid setelah mengacak map
    #acak_droid_tambahan()

# droid merah utama
def tambah_droid_merah():
    global droidMerah_tambahan
    # Mengecek apakah sudah mencapai batas maksimal droid merah
    if len(droidMerah_tambahan) >= MAX_droidMerah_tambahan:
        return
    # Mengacak posisi droid merah baru di jalur putih
    while True:
        baris_droid_merah = random.randint(0, tinggi_sel - 1)
        kolom_droid_merah = random.randint(0, lebar_sel - 1)
        if is_putih_path(baris_droid_merah, kolom_droid_merah) and (baris_droid_merah != baris_droid_hijau or kolom_droid_merah != kolom_droid_hijau):
            break
    # Menambahkan droid merah baru ke dalam list
    droidMerah_tambahan.append((baris_droid_merah, kolom_droid_merah))

labirin_baris = 10
labirin_kolom = 10
MAX_droidMerah_tambahan = 10

# Fungsi untuk menambahkan droid merah 
def tambah_droid():
    global droidMerah_tambahan
    # Mengecek apakah sudah mencapai batas maksimal droid merah
    if len(droidMerah_tambahan) >= MAX_droidMerah_tambahan:
        return
    # Mengacak posisi droid merah baru di jalur putih
    while True:
        baris_droid_merah = random.randint(0, tinggi_sel - 1)
        kolom_droid_merah = random.randint(0, lebar_sel - 1)
        if is_putih_path(baris_droid_merah, kolom_droid_merah) and (
                baris_droid_merah != baris_droid_hijau or kolom_droid_merah != kolom_droid_hijau):
            break
    # Menambahkan droid merah baru ke dalam list
    droidMerah_tambahan.append((baris_droid_merah, kolom_droid_merah))
        
def acak_droid():
    global baris_droid_hijau, kolom_droid_hijau, baris_droid_merah, kolom_droid_merah

    while True:
        baris_droid_hijau = random.randint(0, tinggi_sel - 1)
        kolom_droid_hijau = random.randint(0, lebar_sel - 1)
        if labirin[baris_droid_hijau][kolom_droid_hijau] == 0:
            break

    while True:
        baris_droid_merah = random.randint(0, tinggi_sel - 1)
        kolom_droid_merah = random.randint(0, lebar_sel - 1)
        if labirin[baris_droid_merah][kolom_droid_merah] == 0:
            break

droidMerah_tambahan = []
def acak_droid_tambahan():
    global baris_droid_merah, kolom_droid_merah

    while True:
        baris = random.randint(0, tinggi_sel - 1)
        kolom = random.randint(0, lebar_sel - 1)
        if labirin[baris][kolom] == 0 and (baris, kolom) not in droidMerah_tambahan:
            break

    droidMerah_tambahan.append((baris, kolom))

def move_droid_merah():
    global baris_droid_merah, kolom_droid_merah, is_game_running

    if not is_game_running:
        return  # Hentikan pergerakan droid merah jika is_game_running adalah False

    # Ambil posisi droid hijau saat ini
    posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)

    # Cari jalur menggunakan BFS Search untuk droid hijau saat ini
    path = bfs_search((baris_droid_merah, kolom_droid_merah), posisi_terakhir_droid_hijau)

    if path:
        # Pindahkan droid merah ke langkah berikutnya dalam jalur
        baris_droid_merah, kolom_droid_merah = path[1]  # Mengambil langkah pertama setelah posisi saat ini

        # Delay sebelum pembaruan posisi berikutnya
        time.sleep(0.2)
    
    # Periksa apakah droid merah bertemu dengan droid hijau
    if (baris_droid_merah, kolom_droid_merah) == (baris_droid_hijau, kolom_droid_hijau):
        print("DROID MERAH TELAH MENEMUKAN DROID HIJAU")
        stop_game()

def update_posisi_droid_merah_tambahan():
    global droidMerah_tambahan
    
    if not is_game_running:
        return  # Hentikan pergerakan droid merah jika is_game_running adalah False

    for i in range(len(droidMerah_tambahan)):
        posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)
        path = bfs_search(droidMerah_tambahan[i], posisi_terakhir_droid_hijau)
        if path:
            droidMerah_tambahan[i] = path[1]
            time.sleep(0.2)
        # Periksa apakah droid merah bertemu dengan droid hijau
    if (droidMerah_tambahan) == (baris_droid_hijau, kolom_droid_hijau):
        print("DROID MERAH TELAH MENEMUKAN DROID HIJAU")
        stop_game()

def bfs_search(start, goal):
    visited = set()
    q = queue.Queue()
    q.put([start])

    while not q.empty():
        path = q.get()
        current_node = path[-1]

        if current_node == goal:
            return path

        if current_node in visited:
            continue

        visited.add(current_node)

        row, col = current_node
        neighbors = get_valid_neighbors(row, col)

        for neighbor in neighbors:
            new_path = list(path)
            new_path.append(neighbor)
            q.put(new_path)

    return None

def get_valid_neighbors(row, col):
    neighbors = []

    if row > 0 and labirin[row - 1][col] == 0:
        neighbors.append((row - 1, col))

    if row < tinggi_sel - 1 and labirin[row + 1][col] == 0:
        neighbors.append((row + 1, col))

    if col > 0 and labirin[row][col - 1] == 0:
        neighbors.append((row, col - 1))

    if col < lebar_sel - 1 and labirin[row][col + 1] == 0:
        neighbors.append((row, col + 1))

    return neighbors

def update_game():
    if pygame.display.get_init():  # Check if the display is still open
        screen.fill(ABU_ABU)
        gambar_labirin()

        if not pandangan_droidMerah:
            if not pandangan_droidHijau:
                gambar_droid(HIJAU, baris_droid_hijau, kolom_droid_hijau)

        for droid_merah in droidMerah_tambahan:
            gambar_droid(MERAH, droid_merah[0], droid_merah[1])

        gambar_droid(HIJAU, baris_droid_merah, kolom_droid_merah)

        # Periksa apakah droid merah bertemu dengan droid hijau
        if (baris_droid_merah, kolom_droid_merah) == (baris_droid_hijau, kolom_droid_hijau):
            if pygame.display.get_init():  # Check if the display is still open
                pygame.draw.rect(screen, MERAH, (220, 250, 505, 100))
                font = pygame.font.Font(None, 30)
                text = font.render("DROID MERAH TELAH MENEMUKAN DROID HIJAU", True, PUTIH)
                screen.blit(text, (225, 295))
                button()
                pygame.display.flip()
            return  # Berhenti setelah menampilkan pesan

        move_droid_hijau()  # Pembaruan posisi droid hijau

        button()

        pygame.display.flip()

# Fungsi untuk menggerakkan droid hijau secara acak
def move_droid_hijau():
    global baris_droid_hijau, kolom_droid_hijau, posisi_terakhir_droid_hijau, is_game_running
    
    if not is_game_running:
        return  # Hentikan pergerakan droid merah jika is_game_running adalah False

    # Mendapatkan tetangga yang valid untuk droid hijau
    neighbors = get_valid_neighbors(baris_droid_hijau, kolom_droid_hijau)

    # Periksa apakah droid merah berada dalam jarak tertentu dari droid hijau
    if is_droid_merah_dekat():
        # Pilih tetangga yang menjauh dari droid merah
        farthest_neighbor = get_farthest_neighbor(neighbors)
        if farthest_neighbor is not None:
            # Simpan posisi terakhir droid hijau sebelum pindah ke tetangga yang dipilih
            posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)
            # Pindahkan droid hijau ke tetangga yang dipilih
            baris_droid_hijau, kolom_droid_hijau = farthest_neighbor
        else:
            # Jika tidak ada tetangga yang dapat dipilih (jalan mentok), berhenti
            print("DROID MERAH TELAH MENEMUKAN DROID HIJAU")
            stop_game()
    else:
        # Pilih tetangga secara acak
        random_neighbor = random.choice(neighbors)
        # Simpan posisi terakhir droid hijau sebelum pindah ke tetangga yang dipilih
        posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)
        # Pindahkan droid hijau ke tetangga yang dipilih secara acak
        baris_droid_hijau, kolom_droid_hijau = random_neighbor

# Fungsi untuk memeriksa apakah droid merah berada dalam jarak tertentu dari droid hijau
def is_droid_merah_dekat():
    jarak_minimal = 10  # Jarak minimal antara droid merah dan droid hijau

    # Hitung jarak antara droid merah dan droid hijau
    jarak = abs(baris_droid_merah - baris_droid_hijau) + abs(kolom_droid_merah - kolom_droid_hijau)

    # Kembalikan True jika droid merah berada dalam jarak tertentu, False jika tidak
    return jarak <= jarak_minimal

# Fungsi untuk mendapatkan tetangga yang menjauh dari droid merah
def get_farthest_neighbor(neighbors):
    farthest_distance = 0
    farthest_neighbor = None

    for neighbor in neighbors:
        row, col = neighbor
        distance = abs(baris_droid_merah - row) + abs(kolom_droid_merah - col)
        if distance > farthest_distance:
            farthest_distance = distance
            farthest_neighbor = neighbor

    return farthest_neighbor

game_started = False

# Fungsi untuk menjalankan pergerakan droid
def run_game():
    global is_game_running, posisi_terakhir_droid_hijau
    while is_game_running:
        posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)
        
        if is_game_running:
            move_droid_hijau()
            if not is_game_running:
                break
        
        if is_game_running:
            move_droid_merah()
            if not is_game_running:
                break
        
        if is_game_running:
            update_posisi_droid_merah_tambahan()
            if not is_game_running:
                break

    if is_game_running:
        update_game()

# Fungsi untuk menghentikan pergerakan droid merah dan hijau
def stop_game():
    global is_game_running
    is_game_running = False

is_game_running = False  # Global variable to track the game state

# Fungsi untuk memulai permainan
def start_game():
    global is_game_running, game_started
    if not is_game_running:
        is_game_running = True
        game_started = True
        game_thread = threading.Thread(target=run_game)
        game_thread.start()
  
baris_droid_hijau = 0  # Nilai awal baris_droid_hijau
kolom_droid_hijau = 0  # Nilai awal kolom_droid_hijau
# Kemudian, pada bagian yang lain dalam program, Anda dapat menggunakannya seperti ini:
posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)
            
# Loop utama
running = True
pandangan_droidMerah = False
pandangan_droidHijau = False
acak_map()
droidMerah_tambahan = []  # Menginisialisasi mendaftar droid merah
# Inisialisasi posisi terakhir droid hijau
posisi_terakhir_droid_hijau = (baris_droid_hijau, kolom_droid_hijau)

while running:
    screen.fill(ABU_ABU) # ketika pandangan droid hijau ditekan layar berubah warna abu-abu

    gambar_labirin()
    
    if not pandangan_droidMerah:
      if not pandangan_droidHijau:
        gambar_droid(HIJAU, baris_droid_hijau, kolom_droid_hijau)
    
    for droid_merah in droidMerah_tambahan:
        gambar_droid(MERAH, droid_merah[0], droid_merah[1])

    gambar_droid(MERAH, baris_droid_merah, kolom_droid_merah)
    button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if lebar_layar - 180 <= event.pos[0] <= lebar_layar - 20 and 50 <= event.pos[1] <= 650:
                    button_index = (event.pos[1] - 140) // 50
                    # button untuk mulai permainan
                    if button_index == 0:
                        start_game()  # Memulai permainan dalam thread terpisah
                    # button untuk acak droid
                    elif button_index == 1:
                        acak_droid()
                        for i in range(len(droidMerah_tambahan)):
                            while True:
                                baris = random.randint(0, tinggi_sel - 1)
                                kolom = random.randint(0, lebar_sel - 1)
                                if labirin[baris][kolom] == 0 and (baris, kolom) not in droidMerah_tambahan:
                                    break
                            droidMerah_tambahan[i] = (baris, kolom)
                        pygame.display.flip()  # Perbarui tampilan setelah mengacak posisi droid merah
                    # button untuk tambah droid     
                    elif button_index == 2:
                        if droidMerah_tambahan_count < MAX_droidMerah_tambahan:
                            tambah_droid()
                            for droid_merah in droidMerah_tambahan:
                                gambar_droid(MERAH, droid_merah[0], droid_merah[1])
                            pygame.display.flip()  # Perbarui tampilan setelah menambahkan dan menggambar droid merah
                    # button untuk acak map
                    elif button_index == 3:
                        acak_map()
                        for i in range(len(droidMerah_tambahan)):
                            while True:
                                baris = random.randint(0, tinggi_sel - 1)
                                kolom = random.randint(0, lebar_sel - 1)
                                if labirin[baris][kolom] == 0 and (baris, kolom) not in droidMerah_tambahan:
                                    break
                            droidMerah_tambahan[i] = (baris, kolom)
                        #droidMerah_tambahan = []  # Reset the list of merah droid
                        pygame.display.flip()  # Perbarui tampilan setelah menambahkan dan menggambar droid merah
                    # button untuk pandangan droid hijau
                    elif button_index == 4:
                        pandangan_droidHijau = not pandangan_droidHijau
                    # button untuk slider pandangan droid hijau
                    elif button_index == 5:
                        ubah_pandangan_DroidHijau(event.pos)
                    # button PANDANGAN DROID MERAH 
                    elif button_index == 6:
                        pandangan_droidMerah = not pandangan_droidMerah
                        if pandangan_droidMerah:
                          pandangan_droidHijau = False
                    #button untuk KURANGI DROID
                    elif button_index == 7:
                        kurangi_droid()
                        for droid_merah in droidMerah_tambahan:
                            gambar_droid(MERAH, droid_merah[0], droid_merah[1])
                        pygame.display.flip()  # Perbarui tampilan setelah mengurangi dan menggambar droid merah
                    #button untuk stop permainan
                    elif button_index == 8:
                        stop_game()

    pygame.display.flip()

pygame.quit()