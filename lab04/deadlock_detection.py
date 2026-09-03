# deadlock_detection.py
import threading
import time

gpu_0_lock = threading.Lock()
gpu_1_lock = threading.Lock()

# เกณฑ์เวลาในการตรวจจับ (Timeout เป็นวินาที)
TIMEOUT = 2.0 

def train_model_a():
    print("[Model A] กำลังรอ GPU 0...")
    gpu_0_lock.acquire()
    print("[Model A] ครอบครอง GPU 0 แล้ว จำลองการทำงาน...")
    time.sleep(0.5)
    
    print("[Model A] พยายามครอบครอง GPU 1 (โหมดตรวจจับ)...")
    # การตรวจจับ DEADLOCK: รอสูงสุดเพียง TIMEOUT วินาทีเท่านั้น
    acquired = gpu_1_lock.acquire(timeout=TIMEOUT)
    
    if not acquired:
        # --- ตรวจพบ DEADLOCK และทำการกู้คืน ---
        print("\n>> [OS WATCHDOG] ตรวจพบ Deadlock ที่ Model A!")
        print(">> [RECOVERY] Model A กำลังปล่อย GPU 0 เพื่อป้องกันไม่ให้ทั้งระบบหยุดนิ่ง...\n")
        gpu_0_lock.release() # ย้อนกลับ / สละทรัพยากร (Rollback / Preempt resource)
        return
    
    print("[Model A] ครอบครอง GPU 1 สำเร็จแล้ว! กำลังฝึกสอน...")
    gpu_1_lock.release()
    gpu_0_lock.release()

def train_model_b():
    print("[Model B] กำลังรอ GPU 1...")
    gpu_1_lock.acquire()
    print("[Model B] ครอบครอง GPU 1 แล้ว จำลองการทำงาน...")
    time.sleep(0.5)
    
    print("[Model B] กำลังรอ GPU 0...")
    # Model B จะถูกบล็อกอยู่ที่นี่ แต่จะรอดได้เมื่อ Model A ยอมสละทรัพยากรให้
    gpu_0_lock.acquire()
    print("[Model B] ครอบครอง GPU 0 สำเร็จแล้ว! การฝึกสอนเสร็จสมบูรณ์")
    
    gpu_0_lock.release()
    gpu_1_lock.release()

def main():
    print("--- เริ่มต้นคลัสเตอร์พร้อมระบบตรวจจับ Deadlock ---")
    t1 = threading.Thread(target=train_model_a)
    t2 = threading.Thread(target=train_model_b)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print("--- ระบบทำงานเสร็จสิ้น (กู้คืนสำเร็จ) ---")

if __name__ == "__main__":
    main()
