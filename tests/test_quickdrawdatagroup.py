from quickdraw import QuickDrawDataGroup
from PIL.Image import Image

def test_get_data_group():
    qdg = QuickDrawDataGroup("anvil")
    assert qdg.drawing_count == 1000

    qdg = QuickDrawDataGroup("anvil", max_drawings=2000)
    assert qdg.drawing_count == 2000

def test_get_specific_drawing():
    qdg = QuickDrawDataGroup("anvil")

    # get the first anvil drawing and test the values
    d = qdg.get_drawing(0)
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

def test_get_random_drawing():
    qdg = QuickDrawDataGroup("anvil")

    d = qdg.get_drawing(0)
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

def test_drawings():
    qdg = QuickDrawDataGroup("anvil")
    count = 0
    for drawing in qdg.drawings:
        count += 1
    assert count == 1000
    
def test_recognized_data():
    qdg = QuickDrawDataGroup("anvil", recognized=True)
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
    qdg = QuickDrawDataGroup("anvil", recognized=False)
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
    qdg = QuickDrawDataGroup("anvil")
    # test a search with no criteria returns 1000 results
    r = qdg.search_drawings()
    assert len(r) == 1000

    # test a recognized search
    r = qdg.search_drawings(recognized=True)
    for d in r:
        assert d.recognized
    
    r = qdg.search_drawings(recognized=False)
    for d in r:
        assert not d.recognized

    # test a country search
    r = qdg.search_drawings(countrycode="US")
    for d in r:
        assert d.countrycode == "US"

    # pull first drawing
    key_id = r[0].key_id
    timestamp = r[0].timestamp

    # test key_id search
    r = qdg.search_drawings(key_id=key_id)
    for d in r:
        assert d.key_id == key_id

    # test timestamp search
    r = qdg.search_drawings(timestamp=timestamp)
    for d in r:
        assert d.timestamp == timestamp

    # test a compound search of recognized and country code
    r = qdg.search_drawings(recognized=True, countrycode="US")
    for d in r:
        assert d.recognized 
        assert d.countrycode == "US"