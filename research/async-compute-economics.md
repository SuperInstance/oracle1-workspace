# Async Compute Economics for Fishing Boats

Alright — let’s break this down systematically.  

---

## **1. Hardware & Power Context**

| Device | Cores / GPU | RAM | Power (active) | Use Case |
|--------|-------------|-----|----------------|----------|
| Pi 4B | 4× ARM A72 | 8 GB | ~15 W | Real-time chat, nav overlay, photo snap. Non-real-time vision, transcription, training. |
| Jetson Orin Nano | 1024 CUDA cores (Ampere) + 6× ARM A78AE | 8 GB | ~35 W | Everything Pi can do + **real-time vision**, slower-than-real-time transcription, overnight fine-tuning. |

**Power difference**: Jetson uses **20 W more** when active.  
At sea: solar-charged batteries, overnight 8+ hours idle compute possible.

---

## **2. Daily Data Load**

- **200 camera snaps** (assume 2 MB each → 400 MB raw images)  
- **8 hours audio** (assume 16 kHz mono, 16-bit → 8×3600×16000×2 bytes ≈ 921 MB raw audio)  
- **50 engine readings** (negligible size)  
- **20 nav waypoints** (negligible)  

**Total raw data per day**: ~1.3 GB.  
Satellite cost: **$10/MB** → would cost **$13,000/day** to send raw data.  
So **all processing must be local**, only send summaries.

---

## **3. Processing Tasks & Timing**

### **On Pi 4B:**
- **Real-time tasks** (must run immediately when data arrives):  
  - Chat interface (text, low CPU)  
  - Navigation overlay (low CPU)  
  - Photo snap (just saving image, low CPU)  

- **Non-real-time tasks** (deferred to idle times):  
  1. **Vision inference** on 200 images (object detection, fish counting, etc.)  
     - Pi 4B: CPU inference, maybe 2–5 seconds per image → 400–1000 seconds total (7–17 minutes).  
     - Could run overnight easily.  

  2. **Audio transcription** of 8 hours audio  
     - Pi 4B: Whisper small/base CPU, maybe 0.5–1× real-time? Actually on Pi 4B, likely **slower than real-time** (maybe 2× real-time length).  
     - 8 hours audio → 16 hours processing. **Cannot finish overnight** if also doing vision.  

  3. **Training/fine-tuning** (occasional)  
     - On Pi 4B, very slow, likely impractical for anything but tiny models.  

**Pi 4B schedule**:  
- Day: real