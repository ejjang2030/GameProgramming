import pygame


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


thickness = 15
paddleH = 100


class Game:
    def __init__(self):
        self.__mWindow = None
        self.__mIsRunning = True
        self.__mTicksCount = 0
        self.__mPaddleDir = 0
        self.__mPaddlePos = Vector2(0, 0)
        self.__mBallPos = Vector2(300, 300)
        self.__mBallVel = Vector2(200, 235)
        self.__mClock = pygame.time.Clock()

    def initialize(self):
        pygame.init()
        if not pygame.get_init():
            print(f"Unable to initialize pygame: {pygame.get_error()}")
            return False
        pygame.display.set_caption("Game Programming in Python with Pygame(Chapter 1)")  # 윈도우 제목
        self.__mWindow = pygame.display.set_mode((1024, 768))
        self.__mClock = pygame.time.Clock()
        if not pygame.display.get_init():
            print(f"Failed to create window: {pygame.get_error()}")
            return False
        return True

    def runLoop(self):
        while self.__mIsRunning:
            self.__processInput()
            self.__updateGame()
            self.__generateOutput()

    def shutdown(self):
        pygame.quit()

    def __processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__mIsRunning = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__mIsRunning = False
                    break
                if event.key == ord("w") or event.key == pygame.K_UP:
                    self.__mPaddleDir -= 1
                if event.key == ord("s") or event.key == pygame.K_DOWN:
                    self.__mPaddleDir += 1
            if event.type == pygame.KEYUP:
                if event.key == ord("w") or event.key == ord("s") or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.__mPaddleDir = 0

    def __updateGame(self):
        deltaTime = self.__mClock.tick(30)
        if deltaTime > 0.05:
            deltaTime = 0.05
        self.__mTicksCount = pygame.time.get_ticks()
        if self.__mPaddleDir != 0:
            self.__mPaddlePos.y += self.__mPaddleDir * 300.0 * deltaTime
            # 패들이 화면 영역을 벗어나는지를 검증하자.
            if self.__mPaddlePos.y < (paddleH/2.0 + thickness):
                self.__mPaddlePos.y = paddleH/2.0 + thickness
            elif self.__mPaddlePos.y > (768 - paddleH/2 - thickness):
                self.__mPaddlePos.y = 768 - paddleH/2 - thickness
        self.__mBallPos.x += self.__mBallVel.x * deltaTime
        self.__mBallPos.y += self.__mBallVel.y * deltaTime
        diff = self.__mPaddlePos.y - self.__mBallPos.y
        if diff <= 0:
            diff = -diff
        if diff <= paddleH / 2 and 25 >= self.__mBallPos.x >= 20 and self.__mBallVel.x < 0:
            self.__mBallVel.x *= -1
        elif self.__mBallPos.x <= 0:
            self.__mIsRunning = False
        elif self.__mBallPos.x >= (1024 - thickness) and self.__mBallVel.x > 0:
            self.__mBallVel.x *= -1
        if self.__mBallPos.y <= thickness and self.__mBallVel.y < 0:
            self.__mBallVel.y *= -1
        elif self.__mBallPos.y >= (768 - thickness) and self.__mBallVel.y > 0:
            self.__mBallVel.y *= -1

    def __generateOutput(self):
        self.__mWindow.fill((0, 0, 255))
        wall = pygame.Rect(0, 0, 1024, thickness)
        pygame.draw.rect(self.__mWindow, (255, 255, 255), wall)
        wall = pygame.Rect(1024 - thickness, 0, thickness, 768)
        pygame.draw.rect(self.__mWindow, (255, 255, 255), wall)
        wall = pygame.Rect(0, 768 - thickness, 1024, thickness)
        pygame.draw.rect(self.__mWindow, (255, 255, 255), wall)
        paddle = pygame.Rect(self.__mPaddlePos.x, self.__mPaddlePos.y - paddleH/2, thickness, paddleH)
        pygame.draw.rect(self.__mWindow, (255, 255, 255), paddle)
        ball = pygame.Rect(self.__mBallPos.x - thickness / 2, self.__mBallPos.y - thickness / 2, thickness, thickness)
        pygame.draw.rect(self.__mWindow, (255, 255, 255), ball)
        pygame.display.update()
        self.__mClock.tick(60)


def main():
    game = Game()
    success = game.initialize()
    if success:
        game.runLoop()
    game.shutdown()


main()
