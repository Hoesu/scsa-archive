"""
[Codetree baggage-conveyor-belt] 수하물 컨베이어 벨트
https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/baggage-conveyor-belt/description

작성자 : @Hoesu
결과   : 통과 / 실패 (실행 시간 ms, 메모리 KB)
복잡도 : 시간 O( ), 공간 O( )
접근   :
  -
  -
회고   :
  -
"""


class Box:
    DELTA_R = (0, 1, 0, -1, 0)
    DELTA_C = (0, 0, -1, 0, 1)

    def __init__(self, bi, bt, br, bc, bw):
        self.index = bi
        self.turn = bt
        self.row = br
        self.col = bc
        self.weight = bw
        self.damage = 0
        self.touched = 0
        self.broken = False

    def get_next(self):
        nxt_dir = geography[self.row][self.col]
        nxt_row = self.row + Box.DELTA_R[nxt_dir]
        nxt_col = self.col + Box.DELTA_C[nxt_dir]
        return nxt_row, nxt_col

    def is_immobile(self, touch_time):
        return self.touched == touch_time

    def move(self, move_time):
        self.damage = 0
        nxt_dir = geography[self.row][self.col]
        self.row += Box.DELTA_R[nxt_dir]
        self.col += Box.DELTA_C[nxt_dir]
        if geography[self.row][self.col] == 9:
            self.exit(move_time)

    def freeze(self, freeze_time):
        occupation[self.row][self.col] = self.index
        self.touched = freeze_time
        self.damage += 1
        if self.damage >= 3:
            self.broken = True

    def exit(self, arrival_time):
        if self.broken:
            answer[self.index-1] = -arrival_time
        else:
            answer[self.index-1] = arrival_time
        in_boxes.pop(self.index)


def move_priority(idx_lst, cur_time):
    candidates = []
    for idx in idx_lst:
        candidates.append([idx, in_boxes[idx].weight])
    candidates.sort(key=lambda x: (-x[1], x[0]))
    for idx, _ in candidates[1:]:
        in_boxes[idx].freeze(cur_time)


def enter_priority(box_lst):
    idx = min(box_lst, key=lambda x: (out_boxes[x].turn, x))
    in_boxes[idx] = out_boxes.pop(idx)


if __name__ == '__main__':
    N = int(input())
    geography = [list(map(int, input().split())) for _ in range(N)]
    B = int(input())

    answer = [0] * B
    in_boxes = {}
    out_boxes = {}

    for i in range(1, B+1):
        t, r, c, w = map(int, input().split())
        out_boxes[i] = Box(i, t, r-1, c-1, w)

    time = 1
    while True:
        expectation = {}
        occupation = [[0] * N for _ in range(N)]

        while in_boxes:
            expectation = {}
            immobile_cnt = 0
            for k, v in in_boxes.items():

                # 이동 불가 판정 받은 박스 무시
                if v.is_immobile(time):
                    continue

                # 다음 위치에 이동 불가 박스 존재하면 무시
                nr, nc = v.get_next()
                if occupation[nr][nc] != 0:
                    immobile_cnt += 1
                    v.freeze(time)
                    continue

                # 이동 시도 가능하면 박스 움직여보기
                if (nr, nc) in expectation:
                    expectation[(nr, nc)].append(k)
                else:
                    expectation[(nr, nc)] = [k]

            # 같은 위치에 여러 박스 존재하는 경우 처리
            for k, v in expectation.items():
                if len(v) > 1:
                    move_priority(v, time)
                    immobile_cnt += 1

            # 이번 턴에 이동 불가 판정을 받은 박스가 없다면 루프 종료
            if immobile_cnt == 0:
                break

        # 남은 박스 이동시키기
        for k, v in expectation.items():
            in_boxes[v[0]].move(time)

        # 수하물 투입
        filled = {(v.row, v.col) for v in in_boxes.values()}
        waiting = {}
        for k, v in out_boxes.items():
            # 투입 예정 턴이 지났고, 투입 칸이 비어있는 박스만 시도
            if v.turn <= time and (v.row, v.col) not in filled:
                if (v.row, v.col) in waiting:
                    waiting[(v.row, v.col)].append(k)
                else:
                    waiting[(v.row, v.col)] = [k]

        # 같은 칸에 여러 박스가 투입되려 하면 투입 예정 턴이 가장 이른 박스만 투입
        for k, v in waiting.items():
            enter_priority(v)

        # 모든 박스가 빠져나갔으면 종료
        if not in_boxes and not out_boxes:
            break
        time += 1

    print(*answer)
