from advent import read_file, timer
from math import ceil


class Pair:
    def __init__(self, left, right, parent=None):
        self.left = left
        self.right = right
        self.parent = parent

        if isinstance(self.left, list):
            self.left = Pair(*self.left, self)

        if isinstance(self.right, list):
            self.right = Pair(*self.right, self)

    def check_explode(self, depth=None):
        """Recursively check for exploding pairs; return true when found"""
        depth = 0 if depth is None else depth

        if isinstance(self.left, Pair):
            if self.left.check_explode(depth + 1):
                return True
        if isinstance(self.right, Pair):
            if self.right.check_explode(depth + 1):
                return True
        if depth > 3:
            self.explode()

            if self is self.parent.left:
                self.parent.left = 0
            elif self is self.parent.right:
                self.parent.right = 0
            return True

    def check_split(self):
        """Recursively check for real nubmers >9; return true if found"""
        if isinstance(self.left, Pair):
            if self.left.check_split():
                return True
        elif self.left > 9:
            self.left = Pair(self.left // 2, ceil(self.left / 2))
            self.left.parent = self
            return True
        if isinstance(self.right, Pair):
            if self.right.check_split():
                return True
        elif self.right > 9:
            self.right = Pair(self.right // 2, ceil(self.right / 2))
            self.right.parent = self
            return True

    def __str__(self):
        return '[' + str(self.left) + ',' + str(self.right) + ']'

    def __repr__(self):
        return 'Pair(' + self.left.__repr__() + ', ' + self.right.__repr__() + ')'

    def __add__(self, other):
        """Take two pairs and add together, make sure the returned value is the parent of both pairs"""
        p = Pair(self, other)
        p.left.parent = p
        p.right.parent = p
        return p

    def find_left(self):
        """Find nearest left real number from pair self"""
        if self.parent:
            if self.parent.right is self:
                if not isinstance(self.parent.left, Pair):
                    return self.parent, 'l'
                curr = self.parent.left
                while isinstance(curr.right, Pair):
                    curr = curr.right
                return curr, 'r'
            return self.parent.find_left()

    def find_right(self):
        """Find nearest right real number from pair self"""
        if self.parent:
            if self.parent.left is self:
                if not isinstance(self.parent.right, Pair):
                    return self.parent, 'r'
                curr = self.parent.right
                while isinstance(curr.left, Pair):
                    curr = curr.left
                return curr, 'l'
            return self.parent.find_right()

    def explode(self):
        """Explode current pair"""
        left = self.find_left()
        right = self.find_right()

        if left:
            if left[1] == 'r':
                left[0].right += self.left
            else:
                left[0].left += self.left

        if right:
            if right[1] == 'r':
                right[0].right += self.right
            else:
                right[0].left += self.right

    def magnitude(self):
        if isinstance(self.left, Pair):
            left = self.left.magnitude() * 3
        else:
            left = self.left * 3
        if isinstance(self.right, Pair):
            right = self.right.magnitude() * 2
        else:
            right = self.right * 2

        return left + right


@timer
def p1(ins):
    # Super dangerous to use eval, do not use in real code...
    num = eval(ins[0])
    p = Pair(*num)
    for new_num in ins[1:]:
        p = p + Pair(*eval(new_num))

        # First check for explode, then for splits
        while p.check_explode() or p.check_split():
            pass

    return p.magnitude()


@timer
def p2(ins):
    m = 0
    for a in ins:
        for b in ins:
            # Skip matching snail numbers
            if a == b:
                continue

            # Again, super dangerous to use eval
            p = Pair(*eval(a)) + Pair(*eval(b))
            while p.check_explode() or p.check_split():
                pass

            m = max((m, p.magnitude()))
    return m


f = read_file("./Input/Input18").split('\n')
p1(f)
p2(f)
