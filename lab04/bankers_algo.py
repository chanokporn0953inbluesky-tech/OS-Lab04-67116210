# bankers_algo.py
import numpy as np

# ทรัพยากรทั้งหมดในระบบ: [GPU_Type_A, GPU_Type_B, High_Speed_RAM(TB)]
total_resources = np.array([10, 5, 7])

# ความต้องการสูงสุดสำหรับแต่ละงาน ML (Job 0, Job 1, Job 2)
max_need = np.array([
    [7, 5, 3], 
    [3, 2, 2], 
    [9, 0, 2]
])

# ทรัพยากรที่ถูกจัดสรรไปแล้วในปัจจุบัน
allocated = np.array([
    [0, 1, 0], 
    [2, 0, 0], 
    [3, 0, 2]
])

def is_safe_state(available, max_need, allocated):
    num_jobs = len(allocated)
    work = available.copy()
    finish = [False] * num_jobs
    safe_sequence = []
    
    # คำนวณความต้องการที่เหลือ: Need = Max - Allocated
    need = max_need - allocated
    while len(safe_sequence) < num_jobs:
        allocated_in_this_round = False
        
        for i in range(num_jobs):
            if not finish[i] and all(need[i] <= work):
                # งาน i สามารถทำงานจนเสร็จสิ้นได้
                work += allocated[i] # OS ดึงทรัพยากรกลับคืนมา
                finish[i] = True
                safe_sequence.append(f"Job_{i}")
                allocated_in_this_round = True
                
        if not allocated_in_this_round:
            return False, [] # ระบบอยู่ในสถานะไม่ปลอดภัย (UNSAFE state - กำลังจะเกิด Deadlock)
            
    return True, safe_sequence

def main():
    print("--- ตัวจัดตารางเวลา OS: การตรวจสอบด้วย Banker's Algorithm ---")
    
    # คำนวณทรัพยากรที่พร้อมใช้งานในตอนเริ่มต้น
    available = total_resources - np.sum(allocated, axis=0)
    print(f"ทรัพยากรที่พร้อมใช้งานในปัจจุบัน: {available}")
    
    safe, sequence = is_safe_state(available, max_need, allocated)
    
    if safe:
        print(f">> ระบบมีความปลอดภัย (SYSTEM IS SAFE) ลำดับการทำงาน: {' -> '.join(sequence)}")
        print(">> OS จะอนุมัติคำขอการล็อก")
    else:
        print(">> คำเตือน: ระบบไม่ปลอดภัย (SYSTEM IS UNSAFE)! การอนุมัติการล็อกจะทำให้เกิด Deadlock")
        print(">> ตัวจัดตารางเวลา OS จะปฏิเสธคำขอและบังคับให้กระบวนการนั้นรอ")

if __name__ == "__main__":
    main()