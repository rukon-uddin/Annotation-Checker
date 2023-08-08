from flask import Flask, render_template, json, request
import os
import glob
from yhf import YOLO_ConvertAndDrawBox as ycdb  # git clone https://github.com/rukon-uddin/YOLO-Helper-Function.git  # rename the file to yhf
import cv2

app = Flask(__name__)

cls_idx = {"0": "Car", "1": "Bike", "2": "Cycle"}

ANNOTATION_FOLDER = os.path.join('static', 'annotations')
IMAGE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = ANNOTATION_FOLDER


def save_annot_image():
    images = [i for i in os.listdir(IMAGE_FOLDER) if i.endswith(".jpg")]
    for i in images:
        img_name = i
        txt_name = i.split(".")[0]+".txt"
        img = cv2.imread(f"{IMAGE_FOLDER}/{img_name}")
        lines = open(f"{IMAGE_FOLDER}/{txt_name}").read().strip().split(" ")
        norm_coord = lines[1:]
        cl = lines[0]
        x1, y1, x2, y2 = ycdb.denormalize_yolo_coordinates(img, norm_coord)
        final_img = ycdb.draw_bbox(img, cls_idx[cl], (255, 0, 0), 4, x1, y1, x2, y2)
        cv2.imwrite(f"{ANNOTATION_FOLDER}/{img_name}", final_img)

def get_img_label():
    images = [i for i in os.listdir(IMAGE_FOLDER) if i.endswith(".jpg")]
    img_lab = {}
    for i in images:
        img_name = i
        txt_name = i.split(".")[0]+".txt"
        img = f"{ANNOTATION_FOLDER}/{img_name}"
        lines = open(f"{IMAGE_FOLDER}/{txt_name}").read().strip().split(" ")
        cl = lines[0]
        img_lab[img] = cls_idx[cl]
    return img_lab

@app.route("/")
def hello_world():
    # images = [os.path.join(app.config['UPLOAD_FOLDER'], i)  for i in os.listdir(ANNOTATION_FOLDER) if i.endswith(".jpg")]
    img_lab = get_img_label()
    print(img_lab)
    return render_template("index.html", user_image = img_lab)


@app.route("/delete_img", methods=['POST', 'GET'])
def deleteImage():
    if request.method == "POST":
        qtc_data = request.get_json()
        img_path = qtc_data[0]["Current Image"]
        print("Deleted image: ", img_path)
        # os.remove(img_path)
    return ""

if __name__ == "__main__":
    if len(os.listdir(ANNOTATION_FOLDER)) == 0:
        save_annot_image()
    app.run(debug=True)
