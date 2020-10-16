import pygame, os

# The number of frames the longest animation has
animationFrames = 10


class Graphics:

    # Initialization
    # Arguments:
    #    graphicsDirectory: file path to Graphics folder, ex) 'D:\Python Game\Graphics'
    def __init__(self, graphicsDirectory, display, fps):
        self.graphicsDirectory = graphicsDirectory
        self.display = display
        self.fps = fps

        self.Player = CharacterGraphics('Player',
            pygame.image.load(os.path.join(self.graphicsDirectory, "Models", 'Player.png')).convert_alpha(),
            self.assign_images('Player', 'Walk'),
            self.assign_images('Player', 'Left Attack'),
            self.assign_images('Player', 'Right Attack'))

        self.Enemy1 = CharacterGraphics('Enemy1',
            pygame.image.load(os.path.join(self.graphicsDirectory, "Models", 'Enemy1.png')).convert_alpha(),
            self.assign_images('Enemy1', 'Walk'),
            self.assign_images('Enemy1', 'Left Attack'),
            self.assign_images('Enemy1', 'Right Attack'))

        self.Enemy2 = CharacterGraphics('Enemy2',
            pygame.image.load(os.path.join(self.graphicsDirectory, "Models", 'Enemy2.png')).convert_alpha(),
            self.assign_images('Enemy2', 'Walk'),
            self.assign_images('Enemy2', 'Left Attack'),
            self.assign_images('Enemy2', 'Right Attack'))

    # Creates a list with the desired animation frames
    # Arguments:
    #    character: string with character name including caps, ex) 'Player', 'Enemy1', 'Enemy2'
    #    action: action to be performed, either 'Walk', "Right Attack, or 'Left Attack'
    def assign_images(self, character, action):
        imageList = []
        for x in range(animationFrames):
            filePath = os.path.join(self.graphicsDirectory, "Animations", character, action, 'Frame' + str(x + 1) + '.png')
            if not os.path.exists(filePath):
                filePath = os.path.join(self.graphicsDirectory, "Models", character + '.png')
            imageList.append(pygame.image.load(filePath).convert_alpha())
        return imageList

    def animate(self, counter_two, scroll, players, enemies):
        from Platformer import find_enemy_in_area
        # Code for the animations to work
        if counter_two % int(self.fps / animationFrames) == 0:
            for player in players:
                if player.get_action()[0] == "MOVE" and not find_enemy_in_area(player):  # Needs 4
                    player.set_image(self.Player.get_animation_frame("walk", int(1 + (counter_two % self.fps) / (self.fps / animationFrames))))
                    self.display.blit(player.get_image(), (player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]))
                elif player.get_action()[0] == "ATTACK":
                    attack_direction = 'Right Attack'
                    if (player.get_action()[1].get_position()[0] - player.get_position()[0]) == -1:
                        attack_direction = 'Left Attack'
                    player.set_image(self.Player.get_animation_frame(attack_direction, int(1 + (counter_two % self.fps) / (self.fps / animationFrames))))
                    self.display.blit(player.get_image(), (player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]))
                else:
                    try:
                        player_current_image = (player.get_equiped_item()).get_player_image()
                        player.set_image(player_current_image)
                        self.display.blit(player.get_image(),
                                     (player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]))
                    except:
                        player.set_image(self.Player.get_model())
                        self.display.blit(player.get_image(), (player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]))

            for enemy in enemies:
                action = ''
                if enemy.get_action()[0] == "MOVE" and not find_enemy_in_area(enemy):
                    action = 'Walk'
                elif enemy.get_action()[0] == "ATTACK":
                    action = 'Right Attack'
                    if (enemy.get_action()[1].get_position()[0] - enemy.get_position()[0]) == -1:
                        action = 'Left Attack'
                if action == '':
                    exec('enemy.set_image(self.' + enemy.get_identifier() + '.get_model())')
                else:
                    exec('enemy.set_image(self.' + enemy.get_identifier() + '.get_animation_frame(action, int(1 + (counter_two % self.fps) / (self.fps / animationFrames))))')

                self.display.blit(enemy.get_image(), (enemy.get_rect().x - scroll[0], enemy.get_rect().y - scroll[1]))


class CharacterGraphics:
    def __init__(self, name, model, walk_animation, left_attack_animation, right_attack_animation):
        self.name = name
        self.model = model
        self.walk_animation = walk_animation
        self.left_attack_animation = left_attack_animation
        self.right_attack_animation = right_attack_animation

    def get_name(self):
        return self.name

    # Returns character model image
    def get_model(self):
        return self.model

    # Returns list of frames in character animation
    # Arguments:
    #    action: string with action name in any form, ex) 'Walk', 'Right attack', 'left_attack'
    def get_animation(self, action):
        action = str(action).lower().replace(" ", "").replace("_", "")
        if action == 'walk':
            return self.walk_animation
        elif action == 'leftattack':
            return self.left_attack_animation
        elif action == 'rightattack':
            return self.right_attack_animation

    # Returns a specific frame image from an animation
    # Arguments:
    #    action: string with action name in any form, ex) 'Walk', 'Right attack', 'left_attack'
    #    frame_number: int frame number to be returned, starts at 1 not 0
    def get_animation_frame(self, action, frame_number):
        action = str(action).lower().replace(" ", "").replace("_", "")
        if action == 'walk':
            return self.walk_animation[frame_number - 1]
        elif action == 'leftattack':
            return self.left_attack_animation[frame_number - 1]
        elif action == 'rightattack':
            return self.right_attack_animation[frame_number - 1]