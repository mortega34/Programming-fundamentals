# -*- coding: utf-8 -*-
## 6.009 -- Fall 2016 -- Lab 10
#  Time spent on the lab:
#    Week 1: …
#    Week 2: …

class Textures(object):
    """A collection of object textures.

    Each constant in this class describes one texture, and
    single-letter texture names are also used in level maps.
    For example, the letter "e" in a game level map indicates
    that there is a bee at that position in the game.

    To add support for a new blob type, or to add a new texture
    for an existing blob, you'll probably want to update this
    list and the TEXTURE_MAP list in ``Constants``.
    """
    Bee = "e"
    Boat = "b"
    Building = "B"
    Castle = "C"
    Cloud = "c"
    Fire = "f"
    Fireball = "F"
    Floor = "="
    Helicopter = "h"
    Mushroom = "m"
    Player = "p"
    PlayerBored = "bored"
    PlayerFlying = "h"
    PlayerLost = "defeat"
    PlayerWon = "victory"
    Rain = "r"
    Storm = "s"
    Sun = "o"
    Tree = "t"
    Water = "w"

class Constants(object):
    """A collection of game-world constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    TILE_SIZE = 128
    GRAVITY = -9
    MAX_DOWNWARDS_SPEED = 48

    PLAYER_DRAG = 6
    PLAYER_MAX_HORIZONTAL_SPEED = 48
    PLAYER_HORIZONTAL_ACCELERATION = 16
    PLAYER_JUMP_SPEED = 62
    PLAYER_JUMP_DURATION = 3
    PLAYER_BORED_THRESHOLD = 60

    STORM_LIGHTNING_ROUNDS = 5
    STORM_RAIN_ROUNDS = 10

    BEE_SPEED = 40
    MUSHROOM_SPEED = 16
    FIREBALL_SPEED = 60

    SUN_POWER = 5

    TEXTURE_MAP = {Textures.Bee: '1f41d',          # 🐝
                   Textures.Boat: '26f5',          # ⛵
                   Textures.Building: '1f3e2',     # 🏢
                   Textures.Castle: '1f3f0',       # 🏰
                   Textures.Cloud: '2601',         # ☁
                   Textures.Fire: '1f525',         # 🔥
                   Textures.Fireball: '1f525',     # 🔥
                   Textures.Floor: '2b1b',         # ⬛
                   Textures.Helicopter: '1f681',   # 🚁
                   Textures.Mushroom: '1f344',     # 🍄
                   Textures.Player: '1f60a',       # 😊
                   Textures.PlayerBored: '1f634',  # 😴
                   Textures.PlayerFlying: '1f681', # 🚁
                   Textures.PlayerLost: '1f61e',   # 😞
                   Textures.PlayerWon: '1f60e',    # 😎
                   Textures.Rain: '1f327',         # 🌧
                   Textures.Storm: '26c8',         # ⛈
                   Textures.Sun: '2600',           # ☀
                   Textures.Tree: '1f333',         # 🌳
                   Textures.Water: '1f30a'}        # 🌊


class Rectangle(object):
    """A rectangle object to help with collision detection and resolution."""

    def __init__(self, x, y, w, h):
        """Initialize a new rectangle.

        `x` and `y` are the coordinates of the bottom-left corner. `w`
        and `h` are the dimensions of the rectangle.
        """
        self.x, self.y = x, y
        self.w, self.h = w, h

    def intersects(self, other):
        """Check whether `self` and `other` overlap.

        Rectangles are open on the top and right sides, and closed on
        the bottom and left sides; concretely, this means that the
        rectangle [0, 0, 1, 1] does not intersect either of [0, 1, 1, 1]
        or [1, 0, 1, 1].
        """
        raise NotImplementedError

    @staticmethod
    def translationvector(r1, r2):
        """Compute how much `r2` needs to move to stop intersecting `r1`.

        If `r2` does not intersect `r1`, return ``None``.  Otherwise,
        return a minimal pair ``(x, y)`` such that translating `r2` by
        ``(x, y)`` would suppress the overlap. ``(x, y)`` is minimal in
        the sense of the "L1" distance; in other words, the sum of
        ``abs(x)`` and ``abs(y)`` should be as small as possible.

        When two pairs ``(x, y)`` and ``(y, x)`` are tied, return the
        one with the smallest element first.
        """
        raise NotImplementedError

class Blob(object):
    HARD_BLOBS =  ['26f5', '1f3e2', '1f3f0', '2601', '2b1b', '1f327', '26c8', '1f333', '1f30a']
    SOFT_BLOBS = ['1f41d','1f525','1f525','1f681','1f344','1f60a','2600']
    FEELS_GRAVITY = ['1f525', '1f681', '1f344', '1f60a', '2600']


    def __init__(self, pos, texture, identifier, x_speed=0, y_speed=0):
        self.position = pos
        self.texture = texture
        self.identifier = identifier
        self.y_speed = y_speed
        self.x_speed = x_speed

    def get_y(self):
        return self.position[1]

    def get_x(self):
        return self.position[0]

    def set_y(self, y):
        self.position[1] = y

    def set_x(self, x):
        self.position[0] = x

    def get_x_speed(self):
        return self.x_speed

    def set_x_speed(self, new_speed):
        self.x_speed = new_speed

    def get_y_speed(self):
        return self.y_speed

    def set_y_speed(self, new_speed):
        self.y_speed = new_speed

    def pos_dict(self, pos):
        return {"identifier": self.identifier, "texture": self.texture, "pos": pos}

    def is_player(self):
        return self.texture == '1f60a'

    def inWindow(self, left, right, top, bottom):
        # check if BOTTOM LEFT corner is in window
        if left < self.position[0] < right and bottom < self.position[1] < top:
            return True
        # check if TOP LEFT corner is in window
        elif left < self.position[0] < right and bottom < self.position[1] + Constants.TILE_SIZE < top:
            return True
        # check if TOP RIGHT corner is in window
        elif left < self.position[0]+ Constants.TILE_SIZE < right and bottom < self.position[1]+ Constants.TILE_SIZE < top:
            return True
        # check if BOTTOM RIGHT corner is in window
        elif left < self.position[0]+ Constants.TILE_SIZE < right and bottom < self.position[1] < top:
            return True

    def is_effected_by_gravity(self):
        return self.texture in Blob.FEELS_GRAVITY



    def __repr__(self):
        return "Blob({}, {}, {})".format(self.position, self.texture, self.identifier) 
    # def __str__(self):
    #     return "Position: ",self.position,"\nTexture: ",self.texture,"\nID: ", self.identifier


class Game(object):
    def __init__(self, levelmap):
        """Initialize a new game, populated with objects from `levelmap`.

        `levelmap` is a 2D array of 1-character strings; all possible
        strings (and some others) are listed in the ``Textures`` class.
        Each character in `levelmap` corresponds to a blob of size
        ``TILE_SIZE * TILE_SIZE``.

        This function is free to store `levelmap`'s data however it
        wants; for example, it may choose to just keep a copy of
        `levelmap`; or it could choose to read through `levelmap` and
        extract the position of each blob listed in `levelmap`.

        Any choice is acceptable, as long as it plays well with the
        implementation of ``timestep`` and ``render`` below.
        """
        self.blobs = []
        height = len(levelmap)
        
        self.identifier = 0

        for y, row in enumerate(levelmap):
            for x, elem in enumerate(row):
                if elem != " ":
                    if elem == "p":
                        self.player = Blob([x*Constants.TILE_SIZE, (height-(y+1))*Constants.TILE_SIZE],
                            Constants.TEXTURE_MAP[elem], self.identifier)
                        self.identifier += 1
                        self.blobs.append(self.player)

                    else:
                        temp = Blob([x*Constants.TILE_SIZE, (height-(y+1))*Constants.TILE_SIZE],
                            Constants.TEXTURE_MAP[elem], self.identifier) 
                        self.identifier += 1
                        self.blobs.append(temp)

       
        



    def timestep(self, keys):
        """Simulate the evolution of the game state over one time step.
        `keys` indicates currently pressed keys."""


        
        for blob in self.blobs:
            # gravity effects
            if blob.is_effected_by_gravity():
                new_speed = max(-Constants.MAX_DOWNWARDS_SPEED, blob.get_y_speed() + Constants.GRAVITY)
                blob.set_y_speed( new_speed )
                blob.set_y(blob.get_y_speed() + blob.get_y())

            # key effects
            if blob.is_player() and keys:

                for key in keys:
                    if key == "up":
                        blob.set_y_speed(Constants.PLAYER_JUMP_SPEED)
                        blob.set_y(blob.get_y_speed() + blob.get_y())
                    elif key == "left" or key == "right":
                        if key =="left":
                            new_speed = blob.get_x_speed() - Constants.PLAYER_HORIZONTAL_ACCELERATION
                        else:
                            new_speed = blob.get_x_speed() + Constants.PLAYER_HORIZONTAL_ACCELERATION
                        
                        blob.set_x_speed( new_speed )

                        # account for drag effects
                        if blob.get_x_speed() < 0:
                            if abs(blob.get_x_speed()) < Constants.PLAYER_DRAG:
                                drag = -blob.get_x_speed()
                            else:
                                drag = Constants.PLAYER_DRAG
                                
                        elif blob.get_x_speed() > 0:
                            if abs(blob.get_x_speed()) < Constants.PLAYER_DRAG:
                                drag = -blob.get_x_speed()
                            else:
                                drag = -Constants.PLAYER_DRAG
                        else:
                            drag = 0


                        


                        blob.set_x_speed( min(max(blob.get_x_speed() + drag, -Constants.PLAYER_MAX_HORIZONTAL_SPEED), Constants.PLAYER_MAX_HORIZONTAL_SPEED) )
                        blob.set_x(blob.get_x_speed() + blob.get_x())
                        

            # account for drag with no key presses
            elif blob.is_player() and not keys:
                
                if blob.get_x_speed() < 0:
                    if abs(blob.get_x_speed()) < Constants.PLAYER_DRAG:
                        drag = -blob.get_x_speed()
                    else:
                        drag = Constants.PLAYER_DRAG
                elif blob.get_x_speed() > 0:
                    if abs(blob.get_x_speed()) < Constants.PLAYER_DRAG:
                        drag = -blob.get_x_speed()
                    else:
                        drag = -Constants.PLAYER_DRAG
                else:
                    drag = 0
                blob.set_x_speed(blob.get_x_speed() + drag)
                blob.set_x(blob.get_x_speed() + blob.get_x())





                

    def render(self, w, h):
        """Serialize blobs at distance less than `w`, `h` of player."""
        
        left_edge = self.player.get_x() - w/2
        right_edge = self.player.get_x() + w/2
        bottom_edge = 0
        top_edge = h

        result = []
        
        for blob in self.blobs:
            if blob.inWindow(left_edge, right_edge, top_edge, bottom_edge):
                result.append(blob.pos_dict([ blob.get_x() - left_edge, blob.get_y() ]))


        return ("ongoing", result)






