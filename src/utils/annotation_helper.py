def prepare_annotations(detections):
    annotated_images = []
    for img, boxes in detections:
        annotations = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            annotations.append(((x1, y1, x2, y2), "Muzzle"))
        annotated_images.append((img, annotations))
    return annotated_images