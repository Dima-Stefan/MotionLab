import cv2

for n in ["clip_fara_miscare", "clip_miscare", "clip_iluminare"]:
    cap = cv2.VideoCapture(f"data/{n}.avi")
    prev, active, i = None, [], 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        if prev is not None and (cv2.absdiff(g, prev) > 25).sum() > 50:
            active.append(i)
        prev, i = g, i + 1
    print(n, "cadre:", i, "active:", len(active), active[:1], active[-1:])