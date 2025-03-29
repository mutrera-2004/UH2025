import leap
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Game variables
    targets = [{"x": 100, "y": 200, "hit": False}]
    score = 0

    controller = Leap.Controller()

    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Draw targets
        for target in targets:
            color = (0, 255, 0) if not target["hit"] else (255, 0, 0)
            pygame.draw.circle(screen, color, (target["x"], target["y"]), 30)
        
        # Leap Motion tracking
        frame = controller.frame()
        for hand in frame.hands:
            x = int(hand.palm_position.x * 2 + 400)
            y = int(600 - hand.palm_position.y * 2)
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 20)
            
            # Punch detection
            for target in targets:
                dist = ((x - target["x"])**2 + (y - target["y"])**2)**0.5
                if dist < 50 and not target["hit"]:
                    target["hit"] = True
                    score += 1
                    # Send signal to Arduino
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
