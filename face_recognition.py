def verify_voter(registered_image_path, live_capture_image_path):
    from deepface import DeepFace
    try:
        result = DeepFace.verify(registered_image_path, live_capture_image_path)
        return result["verified"]
    except Exception as e:
        print("Error in facial recognition:", e)
        return False
