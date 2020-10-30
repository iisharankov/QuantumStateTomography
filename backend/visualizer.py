# Turn to base64
import base64, io


def _export_png(plt):
  # Matplotlib plot to base64
  pic_IObytes = io.BytesIO()
  plt.set_size_inches(3, 3)  # 300 x 300 px
  plt.savefig(pic_IObytes, format='png')
  pic_IObytes.seek(0)
  return base64.b64encode(pic_IObytes.read())
