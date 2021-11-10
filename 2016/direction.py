from point import Point2D


class Direction:
    @property
    def left(self):
        raise NotImplementedError()

    @property
    def right(self):
        raise NotImplementedError()
    
    @property
    def offset(self):
        raise NotImplementedError()


class North(Direction):
    @property
    def left(self):
        return West()
    
    @property
    def right(self):
        return East()
    
    @property
    def offset(self):
        return Point2D(0, -1)


class South(Direction):
    @property
    def left(self):
        return East()
    
    @property
    def right(self):
        return West()
    
    @property
    def offset(self):
        return Point2D(0, 1)


class East(Direction):
    @property
    def left(self):
        return North()
    
    @property
    def right(self):
        return South()
    
    @property
    def offset(self):
        return Point2D(1, 0)


class West(Direction):
    @property
    def left(self):
        return South()
    
    @property
    def right(self):
        return North()
    
    @property
    def offset(self):
        return Point2D(-1, 0)


def turn_left(direction: Direction, times: int) -> Direction:
    for _ in range(times):
        direction = direction.left
    return direction


def turn_right(direction: Direction, times: int) -> Direction:
    for _ in range(times):
        direction = direction.right
    return direction
