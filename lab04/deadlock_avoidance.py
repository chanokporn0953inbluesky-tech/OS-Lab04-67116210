# deadlock_avoidance.py
import threading
import time

gpu_0_lock = threading.Lock()
gpu_1_lock = threading.Lock()

def train_model_a():
    """โมเดล A ต้องการ GPU 0 ก่อน จากนั้นจึงต้องการ GPU 1"""
    print("[Model A] กำลังรอ GPU 0...")
    gpu_0_lock.acquire()
    print("[Model A] ได้รับ GPU 0 แล้ว กำลังประมวลผล...")
    time.sleep(0.1) 
    
    print("[Model A] กำลังรอ GPU 1...")
    gpu_1_lock.acquire()
    print("[Model A] ได้รับ GPU 1 แล้ว! การฝึกสอนเสร็จสมบูรณ์")
    
    gpu_1_lock.release()
    gpu_0_lock.release()

def train_model_b():
    """
    เดิมทีโมเดล B ต้องการ GPU 1 ก่อน 
    แต่เพื่อป้องกัน Circular Wait เราจึงบังคับให้มันต้องร้องขอ GPU 0 ก่อน
    """
    print("[Model B] กำลังรอ GPU 0 (กฎการจัดลำดับอย่างเคร่งครัด)...")
    gpu_0_lock.acquire()
    print("[Model B] ได้รับ GPU 0 แล้ว กำลังประมวลผล...")
    time.sleep(0.1) 
    
    print("[Model B] กำลังรอ GPU 1...")
    gpu_1_lock.acquire()
    print("[Model B] ได้รับ GPU 1 แล้ว! การฝึกสอนเสร็จสมบูรณ์")
    
    gpu_1_lock.release()
    gpu_0_lock.release()

def main():
    print("--- กำลังเริ่มต้นคลัสเตอร์การฝึกสอน ML (โหมดปลอดภัย) ---")
    t1 = threading.Thread(target=train_model_a)
    t2 = threading.Thread(target=train_model_b)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print("--- การทำงานของคลัสเตอร์เสร็จสมบูรณ์อย่างราบรื่น ---")

if __name__ == "__main__":
    main()
    