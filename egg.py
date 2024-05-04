import pygame
import random

# 初期化
pygame.init()

# 画面の幅と高さ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 画面の設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Egg Breaking Game")

# フォントの設定
font_path = "fonts/misaki_gothic.ttf"
key_description_font = pygame.font.Font(font_path, 20)  # フォントサイズを少し小さくする

# 画像の読み込み
egg_image = pygame.image.load("pic/egg.png")
cracked_egg_image = pygame.image.load("pic/cracked_egg.png")

# 卵のサイズを3倍にする
egg_image = pygame.transform.scale(egg_image, (egg_image.get_width() * 3, egg_image.get_height() * 3))
cracked_egg_image = pygame.transform.scale(cracked_egg_image, (cracked_egg_image.get_width() * 3, cracked_egg_image.get_height() * 3))

# クリック音の読み込み
click_sounds = ["sounds/click1.wav", "sounds/click2.wav"]

# 卵の生成関数
def spawn_egg():
    egg_x = random.randint(50, SCREEN_WIDTH - 50)  # 卵の x 座標をウィンドウ内のランダムな位置に設定
    egg_y = random.randint(50, SCREEN_HEIGHT - 50)  # 卵の y 座標をウィンドウ内のランダムな位置に設定
    egg_rects.append({"rect": egg_image.get_rect(midbottom=(egg_x, egg_y)), "cracked": False, "alpha": 255, "cracked_time": None})  # 卵の Rect をリストに追加

# クリック音の再生
def play_random_click_sound():
    click_sound = pygame.mixer.Sound(random.choice(click_sounds))  # ランダムなクリック音を選択
    click_sound.play()  # クリック音を再生

# 画像の設定
arrow_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(arrow_image, BLACK, [(10, 25), (40, 10), (40, 40)])
arrow_rect = arrow_image.get_rect(midright=(SCREEN_WIDTH - 0, SCREEN_HEIGHT // 2))
original_arrow_pos = arrow_rect.topleft
arrow_speed = 5

# キー説明文の設定
key_description_text1 = key_description_font.render("スペースキーで全ての卵を割る", True, BLACK)
key_description_text2 = key_description_font.render("gキーで卵を制作する", True, BLACK)
key_description_rect1 = key_description_text1.get_rect(topleft=(arrow_rect.right + 20, arrow_rect.centery - 15))  # テキスト位置を調整
key_description_rect2 = key_description_text2.get_rect(topleft=(arrow_rect.right + 20, arrow_rect.centery + 5))  # テキスト位置を調整

# クリーム色の領域を定義
key_description_rect3 = 180 #180がデフォ
cream_rect = pygame.Rect(arrow_rect.right - key_description_rect3, key_description_rect1.top - 10, key_description_rect2.width + key_description_rect3, key_description_rect2.bottom - key_description_rect1.top + 20)
    # クリーム設定
    # arrow_rect.right - 10                                         : 領域の左上隅の x 座標
    # key_description_rect1.top - 10                                : 領域の左上隅の y 座標
    # key_description_rect3 = 180                                   : 領域の幅
    # key_description_rect2.bottom - key_description_rect1.top + 20 : 領域の高さ
    #           ↓
    # 上：key_description_rect1.top - 10
    # 下：key_description_rect2.bottom + 10
    # 左：arrow_rect.right - 10
    # 右：arrow_rect.right - 10 + key_description_rect2.width + 180

#色定義
cream_surface = pygame.Surface((cream_rect.width, cream_rect.height), pygame.SRCALPHA)
cream_surface.fill((255, 255, 204, 128))  # クリーム色を描画し、アルファ値を128に設定する

# 卵の制作関連
egg_rects = []
egg_spawn_time = 0
egg_spawn_interval = random.randint(1000, 3000)  # ミリ秒単位

# フェードアウトの設定
FADE_DELAY = 7500  # フェードアウトの遅延時間（ミリ秒）
FADE_DURATION = 2500  # フェードアウトにかける時間（ミリ秒）

# マウスのドラッグ状態を管理する変数
dragging = False

# カウンターの初期化
broken_eggs_count = 0

# メインループ
running = True
while running:
    screen.fill(WHITE)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # スペースキーが押されたら全ての卵を割る
                egg_rects = []
                # 割れた卵の数をリセットしない
                # broken_eggs_count = 0
            elif event.key == pygame.K_g:
                # gキーが押されたら卵を制作する
                spawn_egg()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                # マウスの左ボタンが押されたらドラッグ中フラグを立てる
                dragging = True
                # クリックされた位置に卵を追加
                for egg in egg_rects:
                    if egg["rect"].collidepoint(event.pos) and not egg["cracked"]:
                        egg["cracked"] = True
                        egg["cracked_time"] = pygame.time.get_ticks()
                        play_random_click_sound()  # ランダムなクリック音を再生
                        broken_eggs_count += 1  # 割れた卵の数を増やす
                        break  # 1つだけ割るため、卵が重なっていた場合に最初の1つだけ割る
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左ボタンが離されたらドラッグ中フラグを解除
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:  # マウスがドラッグ中ならば
                # マウスの位置がウィンドウ内にあるかどうかを確認
                mouse_pos = pygame.mouse.get_pos()
                if 0 <= mouse_pos[0] <= SCREEN_WIDTH and 0 <= mouse_pos[1] <= SCREEN_HEIGHT:
                    # ドラッグ中にマウスが移動した位置にある卵を割る
                    for egg in egg_rects:
                        if egg["rect"].collidepoint(mouse_pos) and not egg["cracked"]:
                            egg["cracked"] = True
                            egg["cracked_time"] = pygame.time.get_ticks()
                            play_random_click_sound()  # ランダムなクリック音を再生
                            broken_eggs_count += 1  # 割れた卵の数を増やす
                            break  # 1つだけ割るため、卵が重なっていた場合に最初の1つだけ割る

    # 卵の数を画面に表示
    egg_count_text = key_description_font.render("Broken Eggs: {}".format(broken_eggs_count), True, BLACK)
    screen.blit(egg_count_text, (10, 10))

    # 卵をランダムな間隔で生成
    current_time = pygame.time.get_ticks()
    if current_time - egg_spawn_time > egg_spawn_interval:
        spawn_egg()
        egg_spawn_time = current_time
        egg_spawn_interval = random.randint(1000, 3000)  # 次の卵の生成間隔を設定

    key_description_setpos = key_description_rect2.width + key_description_rect3 + 90

    # 矢印の動きを制御
    mouse_pos = pygame.mouse.get_pos()
    if cream_rect.collidepoint(mouse_pos):
        if arrow_rect.right > cream_rect.left - 100:
            if arrow_rect.centerx > key_description_setpos // 1:
                arrow_rect.move_ip(-arrow_speed, 0)
            elif arrow_rect.centerx < key_description_setpos // 1:
                arrow_rect.move_ip(arrow_speed, 0)
    elif arrow_rect.collidepoint(mouse_pos) and arrow_rect.left > original_arrow_pos[0] + 2:
        if arrow_rect.centerx > key_description_setpos // 1:
            arrow_rect.move_ip(-arrow_speed, 0)
        elif arrow_rect.centerx < key_description_setpos // 1:
            arrow_rect.move_ip(arrow_speed, 0)
    elif arrow_rect.left > original_arrow_pos[0]:
        arrow_rect.move_ip(-arrow_speed, 0)
    elif arrow_rect.left < original_arrow_pos[0]:
        arrow_rect.move_ip(arrow_speed, 0)

    # クリーム色の領域の位置を更新
    cream_rect.x = arrow_rect.left - 10
    cream_rect.y = key_description_rect1.top - 10

    # キー説明文の位置を更新
    key_description_rect1.topleft = (arrow_rect.right + 20, arrow_rect.centery - 15)
    key_description_rect2.topleft = (arrow_rect.right + 20, arrow_rect.centery + 5)

    # 描画
    for egg in egg_rects:
        if egg["cracked"]:
            # 卵が割れたらフェードアウト効果を適用
            elapsed_time = current_time - egg["cracked_time"]
            if elapsed_time < FADE_DELAY:
                screen.blit(cracked_egg_image, egg["rect"])
            else:
                fade_alpha = 255 - ((elapsed_time - FADE_DELAY) / FADE_DURATION) * 255
                if fade_alpha > 0:
                    egg_surface = pygame.Surface((cracked_egg_image.get_width(), cracked_egg_image.get_height()), pygame.SRCALPHA)
                    egg_surface.set_alpha(fade_alpha)
                    egg_surface.blit(cracked_egg_image, (0, 0))
                    screen.blit(egg_surface, egg["rect"])
                else:
                    egg_rects.remove(egg)
        else:
            screen.blit(egg_image, egg["rect"])

    # クリーム色の領域の描画
    screen.blit(cream_surface, cream_rect)
    # 卵の数を画面に表示
    egg_count_text = key_description_font.render("Broken Eggs: {}".format(broken_eggs_count), True, BLACK)
    screen.blit(egg_count_text, (10, 10))
    # 矢印の描画
    pygame.draw.polygon(arrow_image, BLACK, [(10, 25), (40, 10), (40, 40)])
    screen.blit(arrow_image, arrow_rect)
    # キー説明文の描画
    screen.blit(key_description_text1, key_description_rect1)
    screen.blit(key_description_text2, key_description_rect2)
    
    pygame.display.flip()

    # FPSを設定
    pygame.time.Clock().tick(60)

pygame.quit()
