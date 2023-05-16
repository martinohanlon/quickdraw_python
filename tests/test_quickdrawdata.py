from quickdraw import QuickDrawData, QuickDrawDataGroup, QuickDrawAnimation
from PIL.Image import Image

def test_get_specific_drawing():
    qd = QuickDrawData()

    # get the first anvil drawing and test the values
    d = qd.get_drawing("anvil", 0)
    assert d.name == "anvil"
    assert d.key_id == 5355190515400704
    assert d.recognized == True
    assert d.countrycode == "PL"
    assert d.timestamp == 1488368345

    # 1 stroke, 2 x,y coords, 33 points
    assert len(d.image_data) == 1
    assert len(d.image_data[0]) == 2
    assert len(d.image_data[0][0]) == 33
    assert len(d.image_data[0][1]) == 33
    
    assert d.no_of_strokes == 1
    assert len(d.strokes) == 1
    assert len(d.strokes[0]) == 33
    assert len(d.strokes[0][0]) == 2
    
    assert isinstance(d.image, Image)
    assert isinstance(d.get_image(stroke_color=(10,10,10), stroke_width=4, bg_color=(200,200,200)), Image)

    assert isinstance(d.animation, QuickDrawAnimation)
    assert isinstance(d.get_animation(stroke_color=(10,10,10), stroke_width=4, bg_color=(200,200,200)), QuickDrawAnimation)
    assert len(d.animation.frames) == 32

def test_get_random_drawing():
    qd = QuickDrawData()

    d = qd.get_drawing("anvil")
    assert d.name == "anvil"
    assert isinstance(d.key_id, int)
    assert isinstance(d.recognized, bool)
    assert isinstance(d.timestamp, int)
    assert isinstance(d.countrycode, str)

    assert isinstance(d.image_data, list)
    assert len(d.image_data) == d.no_of_strokes
    
    assert isinstance(d.strokes, list)
    assert len(d.strokes) == d.no_of_strokes
    for stroke in d.strokes:
        for point in stroke:
             assert len(point) == 2

    assert isinstance(d.image, Image)
    assert isinstance(d.get_image(stroke_color=(10,10,10), stroke_width=4, bg_color=(200,200,200)), Image)

    assert isinstance(d.animation, QuickDrawAnimation)
    assert isinstance(d.get_animation(stroke_color=(10,10,10), stroke_width=4, bg_color=(200,200,200)), QuickDrawAnimation)

def test_drawing_names():
    qd = QuickDrawData()
    assert len(qd.drawing_names) == 345

def test_load_drawings():
    qd = QuickDrawData()
    qd.load_drawings(["anvil", "ant"])
    assert qd.loaded_drawings == ["anvil", "ant"]

    qd.get_drawing("angel")
    assert qd.loaded_drawings == ["anvil", "ant", "angel"]

def test_get_drawing_group():
    qd = QuickDrawData()
    assert isinstance(qd.get_drawing_group("anvil"), QuickDrawDataGroup)

def test_recognized_data():
    qdg = QuickDrawData(recognized=True).get_drawing_group("anvil")
    assert qdg.drawing_count == 1000
    
    rec = 0
    unrec = 0

    for drawing in qdg.drawings:
        if drawing.recognized:
            rec += 1
        else:
            unrec += 1

    assert rec == qdg.drawing_count
    assert unrec == 0
    
def test_unrecognized_data():
    qdg = QuickDrawData(recognized=False).get_drawing_group("anvil")
    assert qdg.drawing_count == 1000
    
    rec = 0
    unrec = 0

    for drawing in qdg.drawings:
        if drawing.recognized:
            rec += 1
        else:
            unrec += 1

    assert rec == 0
    assert unrec == qdg.drawing_count

def test_search_drawings():
    qd = QuickDrawData()
    # test a search with no criteria returns 1000 results
    r = qd.search_drawings("anvil")
    assert len(r) == 1000

    # test a recognized search
    r = qd.search_drawings("anvil", recognized=True)
    for d in r:
        assert d.recognized
    
    r = qd.search_drawings("anvil", recognized=False)
    for d in r:
        assert not d.recognized

    # test a country search
    r = qd.search_drawings("anvil", countrycode="US")
    for d in r:
        assert d.countrycode == "US"

    # pull first drawing
    key_id = r[0].key_id
    timestamp = r[0].timestamp

    # test key_id search
    r = qd.search_drawings("anvil", key_id=key_id)
    for d in r:
        assert d.key_id == key_id

    # test timestamp search
    r = qd.search_drawings("anvil", timestamp=timestamp)
    for d in r:
        assert d.timestamp == timestamp

    # test a compound search of recognized and country code
    r = qd.search_drawings("anvil", recognized=True, countrycode="US")
    for d in r:
        assert d.recognized 
        assert d.countrycode == "US"

