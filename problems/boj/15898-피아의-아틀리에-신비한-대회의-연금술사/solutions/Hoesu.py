"""
[Baekjoon 15898] 피아의 아틀리에 ~신비한 대회의 연금술사~
https://bowlog.tistory.com/41

작성자 : @Hoesu
결과   : 통과
접근   :
    - 재료를 넣는 순서가 결과에 영향을 준다.
    - 품질은 재료를 넣을 때마다 0~9로 보정된다. 마지막에 한 번만 보정하면 틀린다.
    - 원소가 W인 칸은 색을 바꾸지 않는다 (효능은 그대로 더해짐).
    - 가마 밖으로 나갈 수 없으므로 위치는 (0,0)~(1,1) 4가지, 회전은 4가지.
    - 흰색 칸의 품질은 점수에 포함되지 않는다.
회고   :
    - 처음에 조합을 생각했는데, 재료를 넣는 순서가 결과에 영향을 준다는 것을 깨달았다. 그래서 바로 순열로 바꿨다.
    - 재료와 가마가 들고 다니는 데이터가 2차원 배열 두 장이라서 귀찮았다.
    - 굳이 굳이 백트래킹 안해도 풀 수 있긴함.
"""


class Ingredient:
    """4x4 효능/원소 격자와 회전본을 가진 재료."""

    def __init__(self, index, effect, element):
        """재료 번호와 효능/원소 격자를 저장하고 회전본을 미리 만든다."""
        self.index = index
        self.effect = effect
        self.element = element
        self.orientations = self._make_orientations()

    def _make_orientations(self):
        """0, 90, 180, 270도 회전한 (효능, 원소) 쌍 4개를 만든다."""
        effect, element = self.effect, self.element
        result = []
        for _ in range(4):
            result.append((effect, element))
            effect, element = rotate(effect), rotate(element)
        return result


class Cauldron:
    """5x5 효능/원소 격자로 이루어진 가마."""

    def __init__(self, other=None):
        """빈 가마를 만들거나, other가 주어지면 그 가마를 복사한다."""
        if other is None:
            self.effect = [[0] * 5 for _ in range(5)]
            self.element = [[0] * 5 for _ in range(5)]
        else:
            self.effect = [row[:] for row in other.effect]
            self.element = [row[:] for row in other.element]

    def add(self, sr, sc, ing_eff, ing_ele):
        """(sr, sc)를 왼쪽 위로 하여 재료를 넣고 효능을 0~9로 제한한다."""
        for i in range(4):
            for j in range(4):
                r, c = sr + i, sc + j
                self.effect[r][c] += ing_eff[i][j]
                if ing_ele[i][j] != 0:
                    self.element[r][c] = ing_ele[i][j]
                self.effect[r][c] = max(0, min(9, self.effect[r][c]))

    def get_score(self):
        """칸마다 효능 x 원소 값을 더한 가마의 점수를 반환한다."""
        return sum(
            self.effect[r][c] * self.element[r][c]
            for r in range(5)
            for c in range(5)
        )


def encode(string):
    """원소 문자(R, B, G, Y, W)를 점수 계수로 바꾼다."""
    rule = {'R': 7, 'B': 5, 'G': 3, 'Y': 2, 'W': 0}
    return rule[string]


def rotate(grid):
    """2차원 리스트를 시계 방향으로 90도 회전한 새 리스트를 반환한다."""
    return [list(row) for row in zip(*grid[::-1])]


def backtrack(cauldron, ingredients, used, depth=0):
    """재료를 MAX_DEPTH개 넣었을 때 얻을 수 있는 최대 점수를 반환한다."""
    if depth == MAX_DEPTH:
        return cauldron.get_score()

    best = 0
    for idx, ing in ingredients.items():
        if used[idx]:
            continue
        used[idx] = True

        # 가마 전체를 돌려도 점수는 같으므로, 첫 재료는 회전 없이만 넣는다
        orientations = ing.orientations[:1] if depth == 0 else ing.orientations
        for effect, element in orientations:
            for sr in range(2):
                for sc in range(2):
                    nxt = Cauldron(cauldron)
                    nxt.add(sr, sc, effect, element)
                    best = max(best, backtrack(nxt, ingredients, used, depth + 1))
        used[idx] = False
    return best


if __name__ == '__main__':
    MAX_DEPTH = 3
    N = int(input())

    ingredients = {}
    for i in range(1, N+1):
        x = [list(map(int, input().split())) for _ in range(4)]
        y = [list(map(encode, input().split())) for _ in range(4)]
        ingredients[i] = Ingredient(i, x, y)

    print(backtrack(Cauldron(), ingredients, [False] * (N + 1)))
