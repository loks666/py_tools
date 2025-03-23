from PIL import Image, ImageDraw, ImageFont

# 创建空白图像
img = Image.new('RGB', (300, 300), (255, 255, 255))
draw = ImageDraw.Draw(img)

# 画一个红色圆圈
draw.ellipse((10, 10, 290, 290), outline='red', width=8)

# 添加公司名称
font = ImageFont.truetype("arial.ttf", 20)
draw.text((60, 130), "宁夏如云网络科技有限责任公司", fill="red", font=font)

# 保存印章
img.save("seal.png")
