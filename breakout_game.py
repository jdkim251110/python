import pygame
import sys
import random

pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭깨기 게임")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# 패들
paddle_width = 300
paddle_height = 15
paddle_x = SCREEN_WIDTH // 2 - paddle_width // 2
paddle_y = SCREEN_HEIGHT - 30
paddle_speed = 8

# 공
ball_size = 8
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 5
ball_dy = -5
ball_speed = 5

# 블럭
blocks = []
block_width = 75
block_height = 20
block_colors = [YELLOW, CYAN, MAGENTA]
for row in range(3):
    for col in range(10):
        block_x = col * (block_width + 5) + 5
        block_y = row * (block_height + 5) + 30
        blocks.append({
            'rect': pygame.Rect(block_x, block_y, block_width, block_height),
            'color': block_colors[row]
        })

# 아이템(드롭)
items = []  # {'rect':..., 'type':'gun', 'color':...}
ITEM_SIZE = 20
ITEM_FALL_SPEED = 3
ITEM_DROP_CHANCE = 0.3  # 블럭 파괴 시 드롭 확률

# 총알
bullets = []  # pygame.Rect
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
BULLET_SPEED = 10
bullet_cooldown = 0
BULLET_COOLDOWN_FRAMES = 12

has_gun = False

score = 0
font = pygame.font.Font(None, 36)

# 게임 루프
running = True
while running:
    clock.tick(60)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
        paddle_x += paddle_speed

    # 스페이스로 총알 발사
    if has_gun and keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bx = paddle_x + paddle_width // 2 - BULLET_WIDTH // 2
        by = paddle_y - BULLET_HEIGHT
        bullets.append(pygame.Rect(bx, by, BULLET_WIDTH, BULLET_HEIGHT))
        bullet_cooldown = BULLET_COOLDOWN_FRAMES

    if bullet_cooldown > 0:
        bullet_cooldown -= 1
    
    # 공 움직임
    ball_x += ball_dx
    ball_y += ball_dy
    
    # 벽 충돌
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - ball_size:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1
    
    # 게임 오버
    if ball_y >= SCREEN_HEIGHT:
        print(f"게임 오버! 최종 점수: {score}")
        running = False
    
    # 패들 충돌
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
    if ball_rect.colliderect(paddle_rect):
        ball_dy *= -1
    
    # 블럭 충돌(공)
    for block in blocks[:]:
        if ball_rect.colliderect(block['rect']):
            blocks.remove(block)
            ball_dy *= -1
            score += 10
            # 아이템 드롭 확률
            if random.random() < ITEM_DROP_CHANCE:
                ix = block['rect'].centerx - ITEM_SIZE // 2
                iy = block['rect'].centery - ITEM_SIZE // 2
                items.append({
                    'rect': pygame.Rect(ix, iy, ITEM_SIZE, ITEM_SIZE),
                    'type': 'gun',
                    'color': ORANGE
                })
    
    # 총알 -> 블럭 충돌
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        # 화면 밖이면 제거
        if bullet.y + BULLET_HEIGHT < 0:
            bullets.remove(bullet)
            continue
        hit = False
        for block in blocks[:]:
            if bullet.colliderect(block['rect']):
                try:
                    blocks.remove(block)
                except ValueError:
                    pass
                score += 10
                hit = True
                # 드롭 확률 (총알로 부숴도 드롭 가능)
                if random.random() < ITEM_DROP_CHANCE:
                    ix = block['rect'].centerx - ITEM_SIZE // 2
                    iy = block['rect'].centery - ITEM_SIZE // 2
                    items.append({
                        'rect': pygame.Rect(ix, iy, ITEM_SIZE, ITEM_SIZE),
                        'type': 'gun',
                        'color': ORANGE
                    })
                break
        if hit:
            try:
                bullets.remove(bullet)
            except ValueError:
                pass

    # 아이템 낙하 및 획득
    for item in items[:]:
        item['rect'].y += ITEM_FALL_SPEED
        if item['rect'].colliderect(paddle_rect):
            if item['type'] == 'gun':
                has_gun = True
            items.remove(item)
            continue
        if item['rect'].y > SCREEN_HEIGHT:
            items.remove(item)
    
    # 게임 클리어
    if len(blocks) == 0:
        print(f"게임 클리어! 최종 점수: {score}")
        running = False
    
    # 화면 그리기
    screen.fill(BLACK)
    
    # 블럭 그리기
    for block in blocks:
        pygame.draw.rect(screen, block['color'], block['rect'])
    
    # 아이템 그리기
    for item in items:
        pygame.draw.rect(screen, item['color'], item['rect'])
        # 아이템 아이콘 간단 표시 (G)
        text = font.render("G", True, BLACK)
        screen.blit(text, (item['rect'].x + 3, item['rect'].y - 2))
    
    # 패들 그리기
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # 공 그리기
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_size)
    
    # 총알 그리기
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    
    # 점수 및 상태 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    gun_text = font.render(f"Gun: {'Ready' if has_gun else 'No'}", True, WHITE)
    screen.blit(gun_text, (10, 40))
    
    pygame.display.flip()

pygame.quit()
sys.exit()