from ultralytics import YOLO

# Load your custom model
model = YOLO("yolov8n.pt")

# Run inference on the video
results = model.predict(
    source='IRAN_SHOCKED!_US_Marine_Corps_Heavy_Weapons_Supply_Convoy_Heading_to_Middle_East_Conflict_Zone(720p).mp4',
    conf=0.3,
    save=True,
    save_txt=False,  # Set to True if you want labels saved as text files
    save_conf=True,  # Save confidence scores in the output
    show=True,
    stream=False
)

# Process results and print detected class names
for result in results:
    if result.boxes is not None:
        for cls in result.boxes.cls:
            print(model.names[int(cls)])