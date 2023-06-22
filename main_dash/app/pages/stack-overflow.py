import dash
from dash import html
from app import stack_layout
import base64

with open('./app/assets/company_size.png', "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
    # ...
    imag = html.Img(id="tag_id", src=img_data, alt="my image", 
    className="img_class")

with open('./app/assets/degrees_through_years.png', "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
    # ...
    imag2 = html.Img(id="tag_id", src=img_data, alt="my image", 
    className="img_class")

with open('./app/assets/gender_through_years.png', "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
    # ...
    imag4 = html.Img(id="tag_id", src=img_data, alt="my image", 
    className="img_class")


with open('./app/assets/remote_work.png', "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
    # ...
    imag3 = html.Img(id="tag_id", src=img_data, alt="my image", 
    className="img_class")

dash.register_page(__name__)
layout = html.Div(children=[
    html.H1(children=''),
        html.Div(children=[
            imag
        ]),
        html.Div(children=[
            imag2
        ]),
        html.Div(children=[
            imag3
        ]),
        html.Div(children=[
            imag4
        ]),
        # html.Div(children=stack_layout.languages_through_years, style={"min-height" : "450px"}),

])


