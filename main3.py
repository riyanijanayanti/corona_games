import random 
import pygame
import os 
pygame.font.init() 
pygame.mixer.init()

# Display Utama
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ayo kita perangi virus COVID-19!")

#Mendeklarasikan warna
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
LILAC = (200, 162, 200)
PURPLE = (128,0,128)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT) #pembagian integer, karena rect tidak dapat bekerja pada float.

#Pengaturan Font
SPLASH_FONT = pygame.font.SysFont('helvetica', 30) 
TITLE_FONT  = pygame.font.Font('04B_19.ttf', 60) 
HEALTH_FONT = pygame.font.SysFont('Times', 30)
WINNER_FONT = pygame.font.SysFont('Times', 30) 

FPS = 60 # Frames per second ketika kita ingin update game 
VEL = 5 # Kecepatan player - px untuk memindahkan jika tombol panah ditekan.
BULLET_VEL = 7
MAX_BULLETS = 3
VIRUS_VEL = 3

#Ukuran PLAYER (VIRUS DAN PEOPLE)
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100

#Ukuran Vaksin
VACCINE_WIDTH = 100
VACCINE_HEIGHT = 100

single_player = True

VIRUS_HIT = pygame.USEREVENT + 1
PEOPLE_HIT = pygame.USEREVENT + 2

# Load assets
#Pengaturan untuk Virus
VIRUS_IMAGE = pygame.image.load(os.path.join('Assets', 'virus2.png'))
VIRUS = pygame.transform.rotate(pygame.transform.scale(VIRUS_IMAGE, (PLAYER_WIDTH,PLAYER_HEIGHT)), 90)

#pengaturan untuk People
PEOPLE_IMAGE = pygame.image.load(os.path.join('Assets', 'people.png'))
PEOPLE = pygame.transform.rotate(pygame.transform.scale(PEOPLE_IMAGE, (PLAYER_WIDTH,PLAYER_HEIGHT)), 270)

#Pengaturan Background  Halaman Pertama
FIRST_IMAGE = pygame.image.load(os.path.join('Assets', 'first_bg.jpg'))
FIRST = pygame.transform.scale(FIRST_IMAGE, (WIDTH, HEIGHT))

#Pengaturan Background utama
SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'main_bg.jpg'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))


#Pengaturan Suara
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot.WAV'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun_people.WAV'))
VIRUS_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun_virus.WAV'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'bg_music.mp3'))

#Pengaturan untuk tembakan virus
VIRUS_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'virus2.png'))
VIRUS_BULLET = pygame.transform.scale(VIRUS_BULLET_IMAGE, (PLAYER_WIDTH//3,PLAYER_HEIGHT//3))

#Pengaturan untuk Vaksin
VACCINE_IMAGE = pygame.image.load(os.path.join('Assets', 'vaksin.png'))
VACCINE = pygame.transform.scale(VACCINE_IMAGE, (VACCINE_WIDTH,VACCINE_HEIGHT))


def wait_for_key():
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(30) # kontrol kecepatan dari  infinate loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit game (click on [X])
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

#menampilkan halaman pertama
def show_start_screen():
    
    global single_player

    WIN.blit(FIRST, (0, 0)) # Menambahkan background image.

    # Title
    WIN.blit(TITLE_FONT.render('CORONA GAMES', False, LILAC),(300, 10))

    
    line1 = SPLASH_FONT.render("ATURAN MAIN:", 1, PURPLE)
    WIN.blit(line1, (WIDTH/2 - line1.get_width()/2, HEIGHT/2 - line1.get_height()/2 - 30))
    
    line2 = SPLASH_FONT.render("Player 1: Panah untuk bergerak. R-CTRL untuk menembak", 1, BLACK)
    WIN.blit(line2, (WIDTH/2 - line2.get_width()/2, HEIGHT/2 - line2.get_height()/2))

    if single_player:
        line3 = SPLASH_FONT.render("Player 2 (Optional): W,A,S,D untuk bergerak. L-CTRL untuk menembak", 1, BLACK)
    else:
        line3 = SPLASH_FONT.render("Player 2: W,A,S,D untuk bergerak. L-CTRL untuk menembak", 1, BLACK)
    WIN.blit(line3, (WIDTH/2 - line3.get_width()/2, HEIGHT/2 - line3.get_height()/2 + 40))

    line4 = SPLASH_FONT.render("TEKAN ENTER", 1, PURPLE)
    WIN.blit(line4, (WIDTH/2 - line4.get_width()/2, HEIGHT/2 - line4.get_height()/2 + 90))
    
    pygame.display.update() 
    wait_for_key()


# Perpindahan Virus (untuk 2 permainan)
def virus_handle_movement(keys_pressed, virus):
    if keys_pressed[pygame.K_a] and virus.x - VEL > 0: # Panah Kiri - Tombol A. Periksa apakah layar hilang sebelum menambahkan 1.
       virus.x -= VEL
    if keys_pressed[pygame.K_d] and virus.x + VEL + virus.width < BORDER.x: # Panah Kanan - Tombol D. Periksa apakah melewati batas tengah sebelum menambahkan 1.
        virus.x += VEL
    if keys_pressed[pygame.K_w] and virus.y - VEL > 0: # Panah ke atas - Tombol W. Periksa apakah layar hilang sebelum menambahkan 1.
       virus.y -= VEL
    if keys_pressed[pygame.K_s] and virus.y + VEL + virus.height < HEIGHT -17: # Panah ke bawah - tombol S. Periksa apakah ketinggian layar naik sebelum menambahkan 1.
        virus.y += VEL

# Perpindahan People
def people_handle_movement(keys_pressed, people):
    if keys_pressed[pygame.K_LEFT] and people.x - VEL > BORDER.x + BORDER.width: # Panah Kiri. Periksa apakah layar hilang sebelum menambahkan 1.
        people.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and people.x + VEL + people.width < WIDTH: # Panah Kanan. Periksa apakah melewati batas tengah sebelum menambahkan 1.
        people.x += VEL
    if keys_pressed[pygame.K_UP] and people.y - VEL > 0: # Panah ke atas. Periksa apakah layar hilang sebelum menambahkan 1
        people.y -= VEL
    if keys_pressed[pygame.K_DOWN] and people.y + VEL + people.height < HEIGHT - 17: # Panah ke bawah. Periksa apakah ketinggian layar naik sebelum menambahkan 1
        people.y += VEL

# Perpindahan Virus - otomatis dan random () (untuk 1 pemain)
def virus_handle_movement_auto(virus):
    global VIRUS_VEL
    rand_direction = random.randrange(1, 5, 1)
    if rand_direction == 1 and virus.x - VEL > 0:
        virus.x -= VEL*VIRUS_VEL
    if rand_direction == 2 and virus.x + VEL + virus.width < BORDER.x:
        virus.x += VEL*VIRUS_VEL
    if rand_direction == 3 and virus.y - VEL > 0:
        virus.y -= VEL*VIRUS_VEL
    if rand_direction == 4 and virus.y + VEL + virus.height < HEIGHT -17:
       virus.y += VEL*VIRUS_VEL

# Menangani gerakan dan lihat apakah peluru yang ditembakkan bertabrakan.
def handle_bullets(vaccine, virus_bullets,people_bullets,virus,people):
    for bullet in virus_bullets:
        bullet.x += BULLET_VEL
        if people.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(PEOPLE_HIT)) 
            virus_bullets.remove(bullet)
        elif bullet.x > WIDTH:
             virus_bullets.remove(bullet) 
        elif vaccine.colliderect(bullet):
             virus_bullets.remove(bullet)

    
    for bullet in people_bullets:
        bullet.x -= BULLET_VEL
        if  virus.colliderect(bullet):  
            pygame.event.post(pygame.event.Event(VIRUS_HIT)) 
            people_bullets.remove(bullet)
        elif bullet.x < 0:
            people_bullets.remove(bullet) 


# Draw/redraw window.
def draw_window(people, virus, people_bullets, virus_bullets, people_health, virus_health):
    WIN.blit(SPACE, (0, 0)) # Insert background image.
    pygame.draw.rect(WIN, BLACK, BORDER)


    # Render teks untuk skor kesehatan.
    people_health_text = HEALTH_FONT.render("Kekebalan Tubuh: " + str(people_health), 1, WHITE)
    WIN.blit(people_health_text, (WIDTH - people_health_text.get_width() - 10, 10))
    virus_health_text = HEALTH_FONT.render("Kekuatan Virus: " + str(virus_health), 1, RED)
    WIN.blit(virus_health_text, (10, 10))

    WIN.blit(VIRUS, (virus.x, virus.y)) # atur posisi saat ini untuk virus
    WIN.blit(PEOPLE, (people.x, people.y)) # atur posisi saat ini untuk virus
    # Gambar Vaksin
    WIN.blit(VACCINE, (WIDTH-500, HEIGHT-100)) # Atur posisi sekarang dari gambar vaksin
    
    # Gambar peluru
    for bullet in people_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    for bullet in virus_bullets:
        WIN.blit(VIRUS_BULLET, bullet)

    pygame.display.update()


def draw_winner(text1, text2):
    draw_text1 = WINNER_FONT.render(text1, 1, WHITE)
    WIN.blit(draw_text1, (WIDTH/2 - draw_text1.get_width()/2, HEIGHT/2 - 2*draw_text1.get_height()))
    draw_text2 = WINNER_FONT.render(text2, 1, WHITE)
    WIN.blit(draw_text2, (WIDTH/2 - draw_text2.get_width()/2, HEIGHT/2 - draw_text2.get_height()))
    pygame.display.update() 
    pygame.time.delay(7000) # tunggu 5 menit sebelum memulai game

def main():
    BACKGROUND_MUSIC.play(-1)
    show_start_screen()

    global single_player
    global MAX_BULLETS
    global VIRUS_VEL

    people = pygame.Rect(700, 250, PLAYER_WIDTH, PLAYER_HEIGHT) #Posisi saat ini untuk orang
    virus = pygame.Rect(200, 300, PLAYER_WIDTH, PLAYER_HEIGHT) # Posisi saat ini untuk virus
    vaccine = pygame.Rect(WIDTH-500, HEIGHT-100, VACCINE_WIDTH, VACCINE_HEIGHT) # Posisi permanen untuk gambar vaksin

    virus_bullets = []
    people_bullets = []

    virus_health = 10
    people_health = 10

    clock = pygame.time.Clock()
#looping untuk skor kesehatan/kekuatan 
    run = True
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_LCTRL:
                    # Player 2 menyentuh tombol. berganti ke mode 2 pemain
                    single_player = False
                if event.key == pygame.K_LCTRL and len(virus_bullets) < MAX_BULLETS: 
                    bullet = pygame.Rect(virus.x + virus.width, virus.y + virus.height//2 -2, 10, 5)
                    virus_bullets.append(bullet)
                    VIRUS_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(people_bullets) < MAX_BULLETS: 
                    bullet = pygame.Rect(people.x, people.y + people.height//2 -2, 10, 5)
                    people_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type ==PEOPLE_HIT:
                people_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == VIRUS_HIT:
                virus_health -= 1
                BULLET_HIT_SOUND.play()

        # Virus menyerang secara acak
        rand_fire = random.randrange(1, 50, 1)
        if rand_fire == 1 and single_player:
            bullet = pygame.Rect(virus.x + virus.width, virus.y + virus.height//2 -2, 10, 5)
            virus_bullets.append(bullet)
            VIRUS_FIRE_SOUND.play()

#teks jika kalah dan menang, menampilkan 5 ronde dengan kecepatan virus 
        winner_text1 =""
        winner_text2 =""
        if  people_health <= 0:
            winner_text1 ="Antibodimu kalah dari Virus!"
            winner_text2 ="Jangan lupa hubungi dokter, semoga lekas sembuh!"
            MAX_BULLETS = 6
            VIRUS_VEL = 4
            single_player = True

        if  virus_health <= 0:
            if MAX_BULLETS == 5:
                if single_player:
                    winner_text1 ="Yes! Imun kamu masih kuat!"
                else:
                    winner_text1 ="Wow! Serangan virus belum mempan!"
                winner_text2 ="Bersiaplah untuk serangan kedua!"
                VIRUS_VEL += 1
            if MAX_BULLETS == 4:
                winner_text1 ="Bersiaplah untuk pertarungan ketiga!"
                if single_player:
                    winner_text2 ="Hebat, Imun kamu masih kuat!"
                else:
                    winner_text2 ="Wow, serangan virus masih belum mempan!"
                VIRUS_VEL += 2
            if MAX_BULLETS == 3:
                winner_text1 ="Bersiaplah untuk pertarungan Keempat!"
                if single_player:
                    winner_text2 ="Jangan lupa makan vitamin dan makan sehat!"
                else:
                    winner_text2 ="Wow, efek vaksin membuat imun lebih kuat!"
                VIRUS_VEL += 3
            if MAX_BULLETS == 2:
                winner_text1 ="Bersiaplah untuk pertarungan Kelima!"
                if single_player:
                    winner_text2 ="Semangat, tubuhmu pasti kuat!"
                else:
                    winner_text2 ="Vitamin juga buat antibodi lebih kuat!"
                VIRUS_VEL += 4
            if MAX_BULLETS == 1:
                winner_text1 ="Virus sudah mati."
                if single_player:
                    winner_text2 ="Selamat, imun kamu menang!"
                else:
                    winner_text2 ="Terbukti, vaksin sangat menolong!"
                MAX_BULLETS = 6
                VIRUS_VEL = 5
                single_player = True

        if winner_text1 != "": 
            draw_window(people, virus, people_bullets, virus_bullets, people_health, virus_health)
            draw_winner(winner_text1, winner_text2)
            break

        keys_pressed = pygame.key.get_pressed()
        if (single_player): 
            virus_handle_movement_auto(virus)
        else:
            virus_handle_movement(keys_pressed, virus)

        people_handle_movement(keys_pressed, people)

        handle_bullets(vaccine, virus_bullets,people_bullets,virus,people) 

        draw_window(people, virus, people_bullets, virus_bullets, people_health, virus_health)

    # pygame.quit()  #akhiri game dan tutup halaman
    BACKGROUND_MUSIC.stop() # Stop musik utama sebelum running main 
    MAX_BULLETS -= 1
    main() # Ketika seseorang menang, Anda dapat memulai kembali permainan setelah 5 detik, alih-alih berhenti dan menutup jendela.


# Hanya jalankan "main" jika file ini saya jalankan secara langsung.
# Jangan dijalankan jika diimpor ke file lain.
if __name__ == "__main__":
    main()
