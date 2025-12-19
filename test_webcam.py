"""
Webcam Test Script for NovaCare Fall Detection System
Tests the AI fall detection using your laptop's webcam - no Pi needed!

Usage: python test_webcam.py
Press 'q' to quit, 'r' to reset detector state
"""
import cv2
import sys
import time

# Add project root to path
sys.path.insert(0, '.')

from app.ai.pose_detector import PoseDetector
from app.ai.fall_detector import FullBodyFallDetector, DetectionResult, BodyPosture


def colorize_result(result: DetectionResult) -> tuple:
    """Get color based on detection result (BGR format)."""
    colors = {
        DetectionResult.NORMAL: (0, 255, 0),        # Green
        DetectionResult.BENDING_OVER: (0, 255, 255), # Yellow
        DetectionResult.FALL_DETECTED: (0, 0, 255),  # Red
        DetectionResult.PERSON_DOWN: (0, 0, 255),    # Red
        DetectionResult.NO_PERSON: (128, 128, 128),  # Gray
    }
    return colors.get(result, (255, 255, 255))


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║    🎥 NovaCare Webcam Test - Fall Detection AI                ║
    ║    ───────────────────────────────────────────────────────    ║
    ║    This tests your webcam + AI without Raspberry Pi           ║
    ║    ───────────────────────────────────────────────────────    ║
    ║    Controls:                                                  ║
    ║      Q - Quit                                                 ║
    ║      R - Reset detector                                       ║
    ║      S - Simulate fall (make yourself low/horizontal)         ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize components
    print("📷 Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not open webcam!")
        print("   Make sure no other app is using the camera.")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✅ Webcam opened successfully!")
    print("🧠 Initializing AI components...")
    
    # Initialize AI
    pose_detector = PoseDetector()
    fall_detector = FullBodyFallDetector(fallen_timeout=5.0)
    
    print("✅ AI initialized!")
    print("\n🚀 Starting detection loop...")
    print("   Stand in front of camera to test pose detection")
    print("   Bend over or lie down to test fall detection\n")
    
    frames = 0
    start_time = time.time()
    last_fps_update = start_time
    fps = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            continue
        
        frames += 1
        
        # Calculate FPS every second
        current_time = time.time()
        if current_time - last_fps_update >= 1.0:
            fps = frames / (current_time - start_time)
            last_fps_update = current_time
        
        # Process pose
        landmarks, annotated_frame = pose_detector.process_frame(frame)
        
        # Detect falls
        result, analysis = fall_detector.analyze(landmarks)
        
        # Get status color
        color = colorize_result(result)
        
        # Draw status overlay
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, annotated_frame, 0.4, 0, annotated_frame)
        
        # Status text
        cv2.putText(annotated_frame, f"Status: {result.value.upper()}", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        posture = analysis.get('posture', 'unknown')
        cv2.putText(annotated_frame, f"Posture: {posture}", 
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        body_angle = analysis.get('body_angle', 0)
        cv2.putText(annotated_frame, f"Body Angle: {body_angle:.1f} deg", 
                    (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        time_down = analysis.get('time_down', 0)
        if time_down > 0:
            cv2.putText(annotated_frame, f"Time Down: {time_down:.1f}s", 
                        (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", 
                        (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Alert banner for falls
        if result == DetectionResult.FALL_DETECTED:
            cv2.rectangle(annotated_frame, (0, 0), (640, 60), (0, 0, 255), -1)
            cv2.putText(annotated_frame, "!!! FALL DETECTED !!!", 
                        (150, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            print(f"🚨 FALL DETECTED! Posture: {posture}, Angle: {body_angle:.1f}°")
            
        elif result == DetectionResult.PERSON_DOWN:
            cv2.rectangle(annotated_frame, (0, 0), (640, 60), (0, 0, 200), -1)
            cv2.putText(annotated_frame, f"PERSON DOWN {time_down:.0f}s!", 
                        (180, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            print(f"🚨🚨 PERSON DOWN for {time_down:.0f}s! Not getting up!")
        
        # Show frame
        cv2.imshow('NovaCare - Webcam Test', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n👋 Exiting...")
            break
        elif key == ord('r'):
            print("🔄 Resetting detector state...")
            fall_detector.reset()
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pose_detector.close()
    
    print("\n✅ Test complete!")
    print(f"   Processed {frames} frames in {time.time() - start_time:.1f}s")
    print(f"   Average FPS: {fps:.1f}")


if __name__ == '__main__':
    main()
