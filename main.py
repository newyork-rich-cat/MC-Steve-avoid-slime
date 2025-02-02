import os
import pygame
import random

##############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
scale_factor = 0.25
original_size = character.get_rect().size
new_width = int(original_size[0] * scale_factor)
new_height = int(original_size[1] * scale_factor)
character = pygame.transform.scale(character, (new_width, new_height))

character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
scale_factor = 0.25
original_size = weapon.get_rect().size
new_width = int(original_size[0] * scale_factor)
new_height = int(original_size[1] * scale_factor)
weapon = pygame.transform.scale(weapon, (new_width, new_height))

weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 슬라임과 마그마 큐브 이미지 로드
slime_images = []
magma_cube_images = []

# 슬라임 이미지 로드
slime_scale_factors = [0.1, 0.06, 0.05, 0.04]
for scale_factor in slime_scale_factors:
    slime = pygame.image.load(os.path.join(image_path, "slime.png"))
    original_size = slime.get_rect().size
    new_width = int(original_size[0] * scale_factor)
    new_height = int(original_size[1] * scale_factor)
    slime = pygame.transform.scale(slime, (new_width, new_height))
    slime_images.append(slime)

# 마그마 큐브 이미지 로드
magma_cube_scale_factors = [0.5, 0.4, 0.3, 0.2]
for scale_factor in magma_cube_scale_factors:
    magma_cube = pygame.image.load(os.path.join(image_path, "magma_cube.png"))
    original_size = magma_cube.get_rect().size
    new_width = int(original_size[0] * scale_factor)
    new_height = int(original_size[1] * scale_factor)
    magma_cube = pygame.transform.scale(magma_cube, (new_width, new_height))
    magma_cube_images.append(magma_cube)

# 슬라임과 마그마 큐브의 속도 설정
slime_speed_y = [-18, -15, -12, -9]  # 슬라임의 y축 속도
magma_cube_speed_y = [-25, -20, -15, -10]  # 마그마 큐브의 y축 속도

# 슬라임과 마그마 큐브 리스트
slimes = []
magma_cubes = []

# 초기 마그마 큐브 추가
magma_cubes.append({
    "pos_x": 50,  # 마그마 큐브의 x 좌표
    "pos_y": 50,  # 마그마 큐브의 y 좌표
    "img_idx": 0,  # 마그마 큐브의 이미지 인덱스
    "to_x": 3,  # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
    "to_y": -6,  # y축 이동방향
    "init_spd_y": magma_cube_speed_y[0],  # y 최초 속도
    "is_magma_cube": True  # 마그마 큐브인지 여부
})

# 초기 슬라임 추가 
slimes.append({
    "pos_x": 100,  # 슬라임의 x 좌표
    "pos_y": 50,  # 슬라임의 y 좌표
    "img_idx": 0,  # 슬라임의 이미지 인덱스
    "to_x": -3,  # x축 이동방향
    "to_y": -6,  # y축 이동방향
    "init_spd_y": slime_speed_y[0],  # y 최초 속도
    "is_magma_cube": False  # 슬라임인지 여부
})

# 사라질 무기, 슬라임, 마그마 큐브 정보 저장 변수
weapon_to_remove = -1
slime_to_remove = -1
magma_cube_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# 게임 종료 메시지
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # 무기 위치를 위로
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]  # 천장에 닿은 무기 없애기

    # 슬라임과 마그마 큐브 위치 정의
    for slime in slimes:
        slime["pos_x"] += slime["to_x"]
        slime["pos_y"] += slime["to_y"]

        # 가로벽에 닿았을 때 방향 변경
        if slime["pos_x"] < 0 or slime["pos_x"] > screen_width - slime_images[slime["img_idx"]].get_rect().size[0]:
            slime["to_x"] *= -1

        # 세로 위치 처리
        if slime["pos_y"] >= screen_height - stage_height - slime_images[slime["img_idx"]].get_rect().size[1]:
            slime["to_y"] = slime["init_spd_y"]
        else:
            slime["to_y"] += 0.5

    for magma_cube in magma_cubes:
        magma_cube["pos_x"] += magma_cube["to_x"]
        magma_cube["pos_y"] += magma_cube["to_y"]

        # 가로벽에 닿았을 때 방향 변경
        if magma_cube["pos_x"] < 0 or magma_cube["pos_x"] > screen_width - magma_cube_images[magma_cube["img_idx"]].get_rect().size[0]:
            magma_cube["to_x"] *= -1

        # 세로 위치 처리
        if magma_cube["pos_y"] >= screen_height - stage_height - magma_cube_images[magma_cube["img_idx"]].get_rect().size[1]:
            magma_cube["to_y"] = magma_cube["init_spd_y"]
        else:
            magma_cube["to_y"] += 0.5

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 슬라임과 충돌 체크
    for slime in slimes:
        slime_rect = slime_images[slime["img_idx"]].get_rect()
        slime_rect.left = slime["pos_x"]
        slime_rect.top = slime["pos_y"]

        if character_rect.colliderect(slime_rect):
            running = False
            break

    # 마그마 큐브와 충돌 체크
    for magma_cube in magma_cubes:
        magma_cube_rect = magma_cube_images[magma_cube["img_idx"]].get_rect()
        magma_cube_rect.left = magma_cube["pos_x"]
        magma_cube_rect.top = magma_cube["pos_y"]

        if character_rect.colliderect(magma_cube_rect):
            running = False
            break

    # 무기와 슬라임/마그마 큐브 충돌 처리
    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_pos_x = weapon_val[0]
        weapon_pos_y = weapon_val[1]

        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_pos_x
        weapon_rect.top = weapon_pos_y

        # 슬라임과 충돌 체크
        for slime_idx, slime in enumerate(slimes):
            slime_rect = slime_images[slime["img_idx"]].get_rect()
            slime_rect.left = slime["pos_x"]
            slime_rect.top = slime["pos_y"]

            if weapon_rect.colliderect(slime_rect):
                weapon_to_remove = weapon_idx
                slime_to_remove = slime_idx

                if slime["img_idx"] < 3:  # 가장 작은 슬라임이 아니라면
                    slime_width = slime_rect.size[0]
                    slime_height = slime_rect.size[1]

                    small_slime_rect = slime_images[slime["img_idx"] + 1].get_rect()
                    small_slime_width = small_slime_rect.size[0]
                    small_slime_height = small_slime_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 슬라임
                    slimes.append({
                        "pos_x": slime["pos_x"] + (slime_width / 2) - (small_slime_width / 2),
                        "pos_y": slime["pos_y"] + (slime_height / 2) - (small_slime_height / 2),
                        "img_idx": slime["img_idx"] + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_spd_y": slime_speed_y[slime["img_idx"] + 1],
                        "is_magma_cube": False
                    })

                    # 오른쪽으로 튕겨나가는 작은 슬라임
                    slimes.append({
                        "pos_x": slime["pos_x"] + (slime_width / 2) - (small_slime_width / 2),
                        "pos_y": slime["pos_y"] + (slime_height / 2) - (small_slime_height / 2),
                        "img_idx": slime["img_idx"] + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": slime_speed_y[slime["img_idx"] + 1],
                        "is_magma_cube": False
                    })

                break

        # 마그마 큐브와 충돌 체크
        for magma_cube_idx, magma_cube in enumerate(magma_cubes):
            magma_cube_rect = magma_cube_images[magma_cube["img_idx"]].get_rect()
            magma_cube_rect.left = magma_cube["pos_x"]
            magma_cube_rect.top = magma_cube["pos_y"]

            if weapon_rect.colliderect(magma_cube_rect):
                weapon_to_remove = weapon_idx
                magma_cube_to_remove = magma_cube_idx

                if magma_cube["img_idx"] < 3:  # 가장 작은 마그마 큐브가 아니라면
                    magma_cube_width = magma_cube_rect.size[0]
                    magma_cube_height = magma_cube_rect.size[1]

                    small_magma_cube_rect = magma_cube_images[magma_cube["img_idx"] + 1].get_rect()
                    small_magma_cube_width = small_magma_cube_rect.size[0]
                    small_magma_cube_height = small_magma_cube_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 마그마 큐브
                    magma_cubes.append({
                        "pos_x": magma_cube["pos_x"] + (magma_cube_width / 2) - (small_magma_cube_width / 2),
                        "pos_y": magma_cube["pos_y"] + (magma_cube_height / 2) - (small_magma_cube_height / 2),
                        "img_idx": magma_cube["img_idx"] + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_spd_y": magma_cube_speed_y[magma_cube["img_idx"] + 1],
                        "is_magma_cube": True
                    })

                    # 오른쪽으로 튕겨나가는 작은 마그마 큐브
                    magma_cubes.append({
                        "pos_x": magma_cube["pos_x"] + (magma_cube_width / 2) - (small_magma_cube_width / 2),
                        "pos_y": magma_cube["pos_y"] + (magma_cube_height / 2) - (small_magma_cube_height / 2),
                        "img_idx": magma_cube["img_idx"] + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": magma_cube_speed_y[magma_cube["img_idx"] + 1],
                        "is_magma_cube": True
                    })

                break

    # 충돌된 무기, 슬라임, 마그마 큐브 제거
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if slime_to_remove > -1:
        del slimes[slime_to_remove]
        slime_to_remove = -1

    if magma_cube_to_remove > -1:
        del magma_cubes[magma_cube_to_remove]
        magma_cube_to_remove = -1

    # 모든 슬라임과 마그마 큐브를 없앤 경우 게임 종료 (성공)
    if len(slimes) == 0 and len(magma_cubes) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for slime in slimes:
        screen.blit(slime_images[slime["img_idx"]], (slime["pos_x"], slime["pos_y"]))

    for magma_cube in magma_cubes:
        screen.blit(magma_cube_images[magma_cube["img_idx"]], (magma_cube["pos_x"], magma_cube["pos_y"]))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2초 대기
pygame.time.delay(2000)

pygame.quit()