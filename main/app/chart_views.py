from app import app
import base64
from io import BytesIO
from matplotlib.figure import Figure

from flask.templating import render_template

@app.route("/chart_example")
def chart_example():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    chart =  f"<img src='data:image/png;base64,{data}'/>"
    
    return render_template('chart_example.html', chart=chart)