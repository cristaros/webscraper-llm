import io, pytest
from PIL import Image
from collector.images import inspect_image

def test_detects_actual_format_and_dimensions():
    data=io.BytesIO(); Image.new('RGB',(640,360),'white').save(data,format='PNG')
    info=inspect_image(data.getvalue()); assert (info.width,info.height,info.content_type)==(640,360,'image/png')
def test_html_disguised_as_image_is_rejected():
    with pytest.raises(ValueError): inspect_image(b'<html><script>bad()</script></html>')
