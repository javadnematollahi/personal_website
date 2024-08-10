import cv2
# import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib
import dlib
import shutil
import os
from Align_face_own import *
matplotlib.use('agg')
import onnxruntime as ort
import numpy as np
# import onnx
# from onnxoptimizer import optimize
# import tf2onnx
# landmarks_detector = LandmarksDetector('weights/shape_predictor_68_face_landmarks.dat')
# loaded_model = tf.keras.models.load_model('weights/Age_prediction.h5')

def predict(image_path: str):
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor("weights/shape_predictor_68_face_landmarks.dat")
  fa = FaceAligner(predictor, desiredFaceWidth=256)
  # load the input image, resize it, and convert it to grayscale
  image = cv2.imread(image_path)
  image = imutils.resize(image, width=800)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # show the original input image and detect faces in the grayscale
  # image
  rects = detector(gray, 2)
  # fig = plt.figure(figsize=(18,6))
  
  # loop over the face detections
  paths = []
  shutil.rmtree("static/images/ageimages") 
  os.mkdir("static/images/ageimages")
  for i,rect in enumerate(rects):
    # extract the ROI of the *original* face, then align the face
    # using facial landmarks
    # (x, y, w, h) = rect_to_bb(rect)
    # faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
    faceAligned = fa.align(image, gray, rect)

    image_RGB = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2RGB)
    image_edit = cv2.resize(image_RGB, (128, 128))
    image_data=image_edit.reshape(1,128,128,3)
    image_data = image_data.astype(np.float32) / 255.0


    onnx_model_path = 'optimized_model.onnx'
    ort_session = ort.InferenceSession(onnx_model_path)

    # Prepare input data
    # Replace this with the actual input shape and data
    input_name = ort_session.get_inputs()[0].name

    # Run inference
    age_pred = ort_session.run(None, {input_name: image_data})


    # age_pred = loaded_model.predict(image_data)
    print(age_pred[0][0][0])
    # return preds,image
    # age,image = predict('input/00.jpg')
    # age_pred=round(age_pred[0][0], 2)
    # plt.title("Your age is about\n",fontsize = 30)
    fig1 = plt.figure(figsize=(2,2.5))
    fig1.add_subplot(1,1,1)
    plt.imshow(image_edit)
    plt.axis("off")
    plt.title("Age:{:.2f}".format(age_pred[0][0][0]),fontsize = 20)
    plt.savefig(f"static/images/ageimages/{i}.jpg", bbox_inches='tight', pad_inches=0)
    plt.close(fig1)
    paths.append(f"static/images/ageimages/{i}.jpg")
    # fig.add_subplot(1, len(rects), i+1)
    # plt.imshow(image_RGB)
    # plt.axis("off")
    # plt.savefig(f"static/images/ageimages/{i}.jpg")
    # paths.append(f"static/images/ageimages/{i}.jpg")

  # plt.suptitle("Your age is about:",fontsize = 30)
  # filename = image_path.split("\\")[-1]
  # plt.savefig(f"static/images/customerimages/{filename}")
  return paths
  # plt.show()

if __name__=="__main__":
  predict('static/uploads/1.jpg')


  # # convert tensorflow model to onnx
  # # Load your .h5 model
  # h5_model_path = 'weights\Age_prediction.h5'
  # model = tf.keras.models.load_model(h5_model_path)

  # # Convert the model to ONNX
  # onnx_model_path = 'model.onnx'
  # spec = (tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype),)
  # output_path = onnx_model_path
  # model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=18)
  # with open(output_path, "wb") as f:
  #     f.write(model_proto.SerializeToString())
  # onnx_model = onnx.load(onnx_model_path)

  # # Apply optimizations
  # optimized_model = optimize(onnx_model)

  # # Save the optimized model
  # optimized_model_path = 'optimized_model.onnx'
  # onnx.save(optimized_model, optimized_model_path)

