"""
[Programmers 77485] 행렬 테두리 회전하기
https://school.programmers.co.kr/learn/courses/30/lessons/77485?language=java&gad_source=1&gad_campaignid=22356298761&gbraid=0AAAAAC_c4nDtlcqqydkNIAku5Cjs5iSfH&gclid=CjwKCAjwgJHXBhBGEiwAHohJq2sxrj8JXKV8VnrT0chiKTrCEGzkiuBYkEN9rfxkfln8Dn8f349zQhoC2F8QAvD_BwE

작성자 : @Hyunnniiii
결과   : 통과 (실행 시간 ms, 메모리 KB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   :
    - 임시 배열 만들어서, 회전시킬 좌표들 순서대로 route에 넣은 뒤 회전시키면서 최소값 구함.
회고   :
    - 그냥 구현 문제인 것 같음. 회전시키는 부분만 잘 구현하면 됨.
"""

def solution(rows, columns, queries):
    # 회전에 의해 위치가 바뀐 숫자들 중 가장 작은 숫자 구하기
    arr = [[i for i in range(rows*columns+1, rows*columns + columns+1)] for rows in range(rows)]

    # 우하좌상
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]


    ans_lst = []
    for idx in range(len(queries)):
        sr, sc, er, ec = queries[idx]

        sr -= 1
        sc -= 1
        er -= 1
        ec -= 1

        min_num = arr[sr][sc]
        route = [(sr, sc)]
        cr, cc = sr, sc
        k = 0
        while True:
            nr, nc = cr + dr[k], cc + dc[k]

            if nr==sr and nc==sc:
                break

            if nr > er or nc > ec:
                k += 1
                continue

            if nr < sr or nc < sc:
                k += 1
                continue

            min_num = min(min_num, arr[nr][nc])
            route.append((nr, nc))
            cr, cc = nr, nc

        ans_lst.append(min_num)
        imsi = [row[:] for row in arr]
        for idx in range(len(route)):
            br, bc = route[idx-1]
            ar, ac = route[idx]
            arr[ar][ac] = imsi[br][bc]


    return ans_lst
