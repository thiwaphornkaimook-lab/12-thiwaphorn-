import sys
import subprocess
import re

def normalize_text(text):
    return text.strip().lower()

def extract_numbers(text):
    return [float(n) if '.' in n else int(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", text)]

def run_test(file_path, input_data):
    try:
        proc = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3
        )
        return proc.stdout, proc.stderr
    except Exception as e:
        return "", str(e)

# นิยาม Test Cases และเกณฑ์ให้คะแนน
TEST_CASES = {
    "Practice_1.py": [
        {"input": "5\n", "expected": 6},
        {"input": "99\n", "expected": 100}
    ],
    "Practice_2.py": [
        {"input": "2\n3\n", "expected": 5},
        {"input": "10\n20\n", "expected": 30}
    ]
}

def grade_problem(file_name, cases):
    total_score = 0
    for case in cases:
        out, err = run_test(file_name, case["input"])
        nums = extract_numbers(out)
        if case["expected"] in nums:
            total_score += 0.5  # ข้อละ 1 คะแนนเต็ม (ข้อละ 2 test cases)
        elif len(nums) > 0:
            total_score += 0.25 # คะแนน partial credit
    return total_score

if __name__ == "__main__":
    print("--- สรุปผลการตรวจคะแนน ---")
    score_1 = grade_problem("Practice_1.py", TEST_CASES["Practice_1.py"])
    score_2 = grade_problem("Practice_2.py", TEST_CASES["Practice_2.py"])
    
    print(f"Practice_1.py: {score_1} / 1.0 คะแนน")
    print(f"Practice_2.py: {score_2} / 1.0 คะแนน")
    print(f"คะแนนรวม: {score_1 + score_2} / 2.0 คะแนน")
