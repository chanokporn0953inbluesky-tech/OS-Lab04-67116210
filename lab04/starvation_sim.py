# starvation_sim.py
import threading
import time

shared_resource_lock = threading.Lock()
job_counts = {"Greedy_Model_A": 0, "Greedy_Model_B": 0, "Polite_Model": 0}
is_running = True

def greedy_task(name):
    """เธรดที่ละโมบซึ่งจะเข้าแย่งชิงการล็อกอย่างต่อเนื่อง"""
    while is_running:
        shared_resource_lock.acquire()
        
        # วิกฤตการณ์ (Critical Section)
        job_counts[name] += 1
        
        shared_resource_lock.release()
        # หยุดพักเสี้ยววินาทีเพื่อบังคับให้ OS สลับบริบท แต่จะกลับมาแข่งขันใหม่ทันที
        time.sleep(0.00001) 

def polite_task(name):
    """เธรดที่สุภาพซึ่งจะรออย่างเหมาะสมก่อนที่จะร้องขอการล็อก"""
    while is_running:
        # ผู้ทำงานที่สุภาพจะรอนานขึ้นเล็กน้อยก่อนส่งคำขอ
        time.sleep(0.01) 
        
        shared_resource_lock.acquire()
        
        # วิกฤตการณ์ (Critical Section)
        job_counts[name] += 1
        
        shared_resource_lock.release()

def main():
    print("--- เริ่มต้นการจำลองภาวะอดอยากของคลัสเตอร์ (ทำงานเป็นเวลา 3 วินาที) ---")
    
    t1 = threading.Thread(target=greedy_task, args=("Greedy_Model_A",))
    t2 = threading.Thread(target=greedy_task, args=("Greedy_Model_B",))
    t3 = threading.Thread(target=polite_task, args=("Polite_Model",))
    t1.start()
    t2.start()
    t3.start()
    
    # ปล่อยให้การจำลองทำงานเป็นเวลา 3 วินาทีถ้วน
    time.sleep(3.0)
    
    global is_running
    is_running = False # ส่งสัญญาณให้ทุกเธรดหยุดการทำงาน
    t1.join()
    t2.join()
    t3.join()
    
    print("\n--- สรุปจำนวนครั้งในการเข้าครอบครองทรัพยากร ---")
    for worker_name, count in job_counts.items():
        print(f"{worker_name}: {count} ครั้ง")

if __name__ == "__main__":
    main()
    