
# 判斷給定位置是否在棋盤範圍內且符合三角形限制
def is_valid_position(row, col, size):
    if row < 0 or row >= size:  # 超過行邊界
        return False
    if col < 0 or col >= size:  # 超過列邊界
        return False
    if col > row:  # 三角形限制：列數不能大於行數
        return False
    return True

# 印出棋盤，並以三角形方式排列
def print_board(current_board, size):
    for i in range(size):
        # 在每行前添加空格，使棋盤居中
        for s in range(size - i - 1):
            print(" ", end="")
        for j in range(i + 1):
            print(current_board[i][j], end="")
            if j < i:  # 行內數字間加空格，最後一個不加
                print(" ", end="")
        print()

# 計算棋盤上剩餘棋子的數量
def count_pegs(current_board, size):
    count = 0
    for i in range(size):
        for j in range(i + 1):
            if current_board[i][j] == 1:
                count += 1
    return count

# 複製棋盤，用於回溯或暫存棋盤狀態
def copy_board(source, size):
    destination = [[0 for _ in range(7)] for _ in range(7)]
    for i in range(size):
        for j in range(i + 1):
            destination[i][j] = source[i][j]
    return destination

# 判斷一個跳躍是否合法
def is_valid_jump(from_row, from_col, to_row, to_col, board, board_size):
    if to_row < 0 or to_row >= board_size or to_col < 0 or to_col > to_row:
        return False  # 超出棋盤邊界
    mid_row = (from_row + to_row) // 2  # 中間棋子行
    mid_col = (from_col + to_col) // 2  # 中間棋子列
    return (board[from_row][from_col] == 1 and  # 起點有棋子
            board[mid_row][mid_col] == 1 and    # 中間有棋子
            board[to_row][to_col] == 0)         # 終點為空

# 回溯法求解最佳解
def solve_puzzle(board, size, steps, best_pegs_left, best_steps, best_board, best_moves, current_moves):
    current_pegs = count_pegs(board, size)  # 計算目前剩餘棋子

    # 更新最佳解
    if current_pegs < best_pegs_left[0] or (current_pegs == best_pegs_left[0] and steps < best_steps[0]):
        best_pegs_left[0] = current_pegs
        best_steps[0] = steps
        # 更新最佳棋盤
        for i in range(size):
            for j in range(i + 1):
                best_board[i][j] = board[i][j]
        # 更新最佳移動步驟
        for i in range(steps):
            for j in range(4):
                best_moves[i][j] = current_moves[i][j]

    # 遍歷所有棋子
    for from_row in range(size):
        for from_col in range(from_row + 1):
            # 六個跳躍方向
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)]
            for direction in directions:
                to_row = from_row + direction[0]
                to_col = from_col + direction[1]
                
                # 如果跳躍合法
                if is_valid_jump(from_row, from_col, to_row, to_col, board, size):
                    mid_row = (from_row + to_row) // 2
                    mid_col = (from_col + to_col) // 2
                    
                    # 記錄當前移動
                    current_moves[steps][0] = from_row
                    current_moves[steps][1] = from_col
                    current_moves[steps][2] = to_row
                    current_moves[steps][3] = to_col
                    
                    # 執行跳躍
                    board[from_row][from_col] = 0
                    board[mid_row][mid_col] = 0
                    board[to_row][to_col] = 1
                    
                    # 遞迴繼續搜索
                    solve_puzzle(board, size, steps + 1, best_pegs_left, best_steps, best_board, best_moves, current_moves)
                    
                    # 回溯：還原棋盤
                    board[from_row][from_col] = 1
                    board[mid_row][mid_col] = 1
                    board[to_row][to_col] = 0

# 玩家互動遊戲
def play_game(board, size, initial_board, best_steps_target, best_pegs_target):
    user_moves = []  # 紀錄玩家每步移動
    steps = 0
    
    print("\n=== 開始遊戲 ===")
    print("輸入格式: from_row from_col to_row to_col")
    print("例如: 2 0 0 0 (將位置(2,0)的棋子移動到(0,0))")
    print("輸入 'end' 結束遊戲\n")
    
    while True:
        current_pegs = count_pegs(board, size)
        
        print(f"\n--- 步驟 {steps} ---")
        print_board(board, size)
        print(f"剩餘棋子數: {current_pegs}")
        
        # 檢查是否達到最佳解
        if steps == best_steps_target and current_pegs == best_pegs_target:
            print("\n🎉 恭喜！你已經達到最佳解!")
            return steps, user_moves, True  # 達到最佳解
        
        # 檢查是否還有可行移動
        has_valid_move = False
        for from_row in range(size):
            for from_col in range(from_row + 1):
                directions = [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2)]
                for dr, dc in directions:
                    to_row = from_row + dr
                    to_col = from_col + dc
                    if is_valid_jump(from_row, from_col, to_row, to_col, board, size):
                        has_valid_move = True
                        break
                if has_valid_move:
                    break
            if has_valid_move:
                break
        
        if not has_valid_move:  # 無法移動，遊戲結束
            print("\n❌ 沒有可行的移動了! 遊戲結束")
            return steps, user_moves, False
        
        # 玩家輸入移動
        user_input = input("\n請輸入移動 (或輸入 'end' 結束): ").strip()
        if user_input.lower() == 'end':
            return steps, user_moves, False  # 使用者主動結束
        
        try:
            parts = user_input.split()
            if len(parts) != 4:
                print("輸入格式錯誤! 請輸入四個數字")
                continue
            
            from_row, from_col, to_row, to_col = map(int, parts)
            
            # 檢查合法性
            if not is_valid_position(from_row, from_col, size):
                print(f"起始位置 ({from_row},{from_col}) 不合法!")
                continue
            if not is_valid_position(to_row, to_col, size):
                print(f"目標位置 ({to_row},{to_col}) 不合法!")
                continue
            if not is_valid_jump(from_row, from_col, to_row, to_col, board, size):
                print("無效的移動! 請確認跳棋規則")
                continue
            
            # 執行移動
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            board[from_row][from_col] = 0
            board[mid_row][mid_col] = 0
            board[to_row][to_col] = 1
            
            user_moves.append((from_row, from_col, to_row, to_col))
            steps += 1
            print(f"✓ 成功移動! 從 ({from_row},{from_col}) 跳到 ({to_row},{to_col})")
            
        except ValueError:
            print("輸入格式錯誤! 請輸入四個數字")
            continue

# 計算最佳解的步數與剩餘棋子
def calculate_best_solution(board, size):
    start_peg = sum(range(2, size + 1))  # 初始棋子數
    best_pegs_left = [start_peg]
    best_steps = [0]
    best_board = [[0]*7 for _ in range(7)]
    best_moves = [[0]*4 for _ in range(50)]
    current_moves = [[0]*4 for _ in range(50)]
    
    solve_puzzle(board, size, 0, best_pegs_left, best_steps, best_board, best_moves, current_moves)
    return best_steps[0], best_pegs_left[0]

# 顯示最佳解
def show_solution(initial_board, size, empty_row, empty_col):
    start_peg = sum(range(2, size + 1))
    best_pegs_left = [start_peg]
    best_steps = [0]
    best_board = [[0]*7 for _ in range(7)]
    best_moves = [[0]*4 for _ in range(50)]
    current_moves = [[0]*4 for _ in range(50)]
    
    board = copy_board(initial_board, size)
    print("\n正在計算最佳解...")
    solve_puzzle(board, size, 0, best_pegs_left, best_steps, best_board, best_moves, current_moves)
    
    if best_pegs_left[0] < start_peg:
        print(f"\n=== 最佳解答: 最少步數 {best_steps[0]}, 剩餘棋子 {best_pegs_left[0]} ===")
        temp_board = copy_board(initial_board, size)
        print_board(temp_board, size)
        for i in range(best_steps[0]):
            fr, fc, tr, tc = best_moves[i]
            mr, mc = (fr+tr)//2, (fc+tc)//2
            temp_board[fr][fc] = 0
            temp_board[mr][mc] = 0
            temp_board[tr][tc] = 1
            print(f"\n步驟 {i+1}: 從 ({fr},{fc}) 移動到 ({tr},{tc})")
            print_board(temp_board, size)
        return best_steps[0], best_pegs_left[0]
    else:
        print("無法找到解答。")
        return 0, start_peg

# 主程式
def main():
    print("="*50)
    print("歡迎來到三角跳棋遊戲!")
    print("="*50)
    
    size = int(input("\n請輸入三角形大小 (3-7): "))
    while size < 3 or size > 7:
        size = int(input("無效大小，請輸入 3-7: "))
    
    # 初始化棋盤
    board = [[1 if j<=i else 0 for j in range(7)] for i in range(7)]
    
    empty_row, empty_col = map(int, input("\n請輸入空格位置 (行 列): ").split())
    while not is_valid_position(empty_row, empty_col, size):
        empty_row, empty_col = map(int, input("位置不合法，重新輸入: ").split())
    board[empty_row][empty_col] = 0
    
    initial_board = copy_board(board, size)
    print("\n初始棋盤:")
    print_board(board, size)
    
    mode = input("\n選擇模式: 1. 自己玩  2. 電腦解答: ").strip()
    if mode == '1':
        temp_board = copy_board(initial_board, size)
        best_steps, best_pegs = calculate_best_solution(temp_board, size)
        player_board = copy_board(initial_board, size)
        user_steps, user_moves, success = play_game(player_board, size, initial_board, best_steps, best_pegs)
        user_pegs = count_pegs(player_board, size)
        if success:
            print_board(player_board, size)
            return
        print(f"\n你的步數: {user_steps}, 剩餘棋子: {user_pegs}")
        print("\n最終棋盤:")
        print_board(player_board, size)
        print("\n最佳解:")
        show_solution(initial_board, size, empty_row, empty_col)
    elif mode == '2':
        show_solution(initial_board, size, empty_row, empty_col)
    else:
        print("無效選擇")
    
    print("\n感謝遊玩三角跳棋! 再見!")

if __name__ == "__main__":
    main()
