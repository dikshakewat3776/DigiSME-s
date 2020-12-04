from detecto import core, utils, visualize
# import torch
#
# print(torch.cuda.is_available())

image = utils.read_image('tomato.jpg')
model = core.Model()

labels, boxes, scores = model.predict_top(image)
visualize.show_labeled_image(image, boxes, labels)


