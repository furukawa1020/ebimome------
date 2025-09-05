import pygame
import random
import math

# Pygameの初期化
pygame.init()

# 画面サイズ設定
screen = pygame.display.set_mode((1000, 600))  # 幅を広くして3人が並べるように

# 背景色の定義
WHITE = (255, 255, 255)

# 画像をロード
try:
    characters = [
        pygame.image.load("character1.png"),
        pygame.image.load("character1.png"),
        pygame.image.load("character1.png")
    ]
    ebis = [
        pygame.image.load("ebi1.png"),
        pygame.image.load("ebi1.png"),
        pygame.image.load("ebi1.png")
    ]
    hand_image = pygame.image.load("momute.png")
except Exception as e:
    print(f"画像のロードに失敗しました: {e}")
    pygame.quit()
    exit()

# 画像サイズ調整
characters = [pygame.transform.scale(char, (150, 150)) for char in characters]
ebis = [pygame.transform.scale(ebi, (80, 80)) for ebi in ebis]

# 手の画像を小さくして、90度回転させる（横向きにする）
hand_image = pygame.transform.scale(hand_image, (80, 80))  # 適切な大きさに変更
hand_image = pygame.transform.rotate(hand_image, 90)  # 手を90度回転して横向きに

# 位置を設定 (キャラクター、エビ、手の位置を3つずつ設定)
character_positions = [(100, 150), (350, 150), (600, 150)]
ebi_positions = [(120, 250), (370, 250), (620, 250)]
hand_positions = [(ebi_pos[0], ebi_pos[1]) for ebi_pos in ebi_positions]

# 揺れる動きを再現するための変数
shake_offsets = [0, 0, 0]
shake_directions = [1, 1, 1]

# 手の円運動と上下運動に関する変数
hand_angle = [0, 0, 0]  # 手の回転角度（ラジアンで管理）
hand_radius = 20  # 円運動の半径を小さく（20ピクセルに設定）
hand_speed = [random.uniform(0.02, 0.05) for _ in range(3)]  # 手の回転速度
hand_vertical_offset = [0, 0, 0]  # 上下運動の変位
hand_vertical_speed = [random.uniform(0.05, 0.1) for _ in range(3)]  # 上下運動の速度

# 動きを制御するフラグ（個別に停止・再開できるようにする）
is_hand_moving = [True, True, True]  # 手の動きを制御（クリックでトグル）

# ステータス表示用のフォント設定
font = pygame.font.SysFont(None, 36)

# 音楽の再生（音楽ファイルが存在する場所を指定）
pygame.mixer.init()
try:
    pygame.mixer.music.load("ebi.mp3")  # 音楽ファイル名を正しく指定
    pygame.mixer.music.play(-1)  # -1は無限ループ
except Exception as e:
    print(f"音楽のロードに失敗しました: {e}")
    pygame.quit()
    exit()

# 時間計測の初期化
start_time = pygame.time.get_ticks()  # ゲーム開始時の時間を記録

# ゲームのメインループ
running = True
while running:
    screen.fill(WHITE)

    # 経過時間を計算
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 秒単位の経過時間
    time_text = f"経過時間: {elapsed_time:.2f}秒"
    time_surface = font.render(time_text, True, (0, 0, 0))
    screen.blit(time_surface, (400, 50))  # 経過時間を画面上部に表示

    # キャラクター、エビの描画（手を描画する前に描く）
    for i in range(3):
        screen.blit(characters[i], character_positions[i])

        # 揺れるエビの描画
        ebi_position_with_shake = (ebi_positions[i][0], ebi_positions[i][1] + shake_offsets[i])
        screen.blit(ebis[i], ebi_position_with_shake)

        # 手の円運動と上下運動（上下に動くように変更）
        if is_hand_moving[i]:
            # 円運動の計算
            hand_angle[i] += hand_speed[i]  # 手の回転速度を適用
            hand_positions[i] = (
                ebi_positions[i][0] + hand_radius * math.cos(hand_angle[i]),
                ebi_positions[i][1] + hand_radius * math.sin(hand_angle[i])
            )

            # 手の上下運動の計算
            hand_vertical_offset[i] = math.sin(pygame.time.get_ticks() * hand_vertical_speed[i] / 1000) * 10  # 上下に10px動く

        # 揉む動作をする手の描画（エビの後に描画して前面に）
        hand_position_with_offset = (
            hand_positions[i][0], 
            hand_positions[i][1] + hand_vertical_offset[i]
        )
        screen.blit(hand_image, hand_position_with_offset)

        # ステータスの表示
        status_text = "動作中" if is_hand_moving[i] else "停止中"
        status_surface = font.render(status_text, True, (0, 0, 0))
        screen.blit(status_surface, (ebi_positions[i][0], ebi_positions[i][1] - 50))  # エビの上にステータス表示

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # クリックされた手をチェックして、動きをトグル（停止・再開）する
            for i in range(3):
                # 手の矩形を取得し、クリックされた場合にトグル
                hand_rect = hand_image.get_rect(topleft=(hand_positions[i][0], hand_positions[i][1] + hand_vertical_offset[i]))
                if hand_rect.collidepoint(event.pos):
                    is_hand_moving[i] = not is_hand_moving[i]  # 動きをトグルする

    # 画面の更新
    pygame.display.flip()

# Pygame終了
pygame.quit()
