# deadlock_simulation.py
import threading
import time

# จำลองทรัพยากรฮาร์ดแวร์ (OS Mutex Locks)
gpu_0_lock = threading.Lock()
gpu_1_lock = threading.Lock()

def train_model_a():
    """โมเดล A ต้องการ GPU 0 ก่อน จากนั้นจึงต้องการ GPU 1"""
    print("[Model A] กำลังรอเพื่อครอบครอง GPU 0...")
    gpu_0_lock.acquire()
    print("[Model A] ครอบครอง GPU 0 สำเร็จแล้ว! กำลังประมวลผล...")
    
    # จำลองระยะเวลาในการประมวลผล และบังคับให้ OS สลับบริบทการทำงาน (Context Switch)
    time.sleep(0.1) 
    
    print("[Model A] กำลังรอเพื่อครอบครอง GPU 1...")
    gpu_1_lock.acquire()
    print("[Model A] ครอบครอง GPU 1 สำเร็จแล้ว! การฝึกสอนเสร็จสมบูรณ์")
    
    # ปลดปล่อยทรัพยากร (Release resources)
    gpu_1_lock.release()
    gpu_0_lock.release()

def train_model_b():
    """โมเดล B ต้องการ GPU 1 ก่อน จากนั้นจึงต้องการ GPU 0"""
    print("[Model B] กำลังรอเพื่อครอบครอง GPU 1...")
    gpu_1_lock.acquire()
    print("[Model B] ครอบครอง GPU 1 สำเร็จแล้ว! กำลังประมวลผล...")
    
    # จำลองระยะเวลาในการประมวลผล และบังคับให้ OS สลับบริบทการทำงาน (Context Switch)
    time.sleep(0.1) 
    
    print("[Model B] กำลังรอเพื่อครอบครอง GPU 0...")
    gpu_0_lock.acquire()
    print("[Model B] ครอบครอง GPU 0 สำเร็จแล้ว! การฝึกสอนเสร็จสมบูรณ์")
    
    # ปลดปล่อยทรัพยากร (Release resources)
    gpu_0_lock.release()
    gpu_1_lock.release()

def main():
    print("--- กำลังเริ่มต้นคลัสเตอร์การฝึกสอน ML ---")
    t1 = threading.Thread(target=train_model_a)
    t2 = threading.Thread(target=train_model_b)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print("--- การทำงานของคลัสเตอร์เสร็จสมบูรณ์ ---")

if __name__ == "__main__":
    main()
    