import struct
from random import choice
from os import path, makedirs
from requests import get
from requests.exceptions import ConnectionError

from .names import QUICK_DRAWING_FILES, QUICK_DRAWING_NAMES

BINARY_URL = "https://storage.googleapis.com/quickdraw_dataset/full/binary/"
CACHE_DIR = path.join(".",".quickdrawcache")


class QuickDrawData():
    """
    Allows interaction with the Google Quick, Draw! data set, downloads 
    Quick Draw data from 
    https://storage.googleapis.com/quickdraw_dataset/full/binary/ 
    and loads it into memory for easy access and processing.

    The following example will load the anvil drawings and get a single 
    drawing::

        from quickdraw import QuickDrawData

        qd = QuickDrawData()

        anvil = qd.get_drawing("anvil")
        print(anvil)

    :param int max_drawings:
        The maximum number of drawings to be loaded into memory,
        defaults to 1000.

    :param bool refresh_data:
        If `True` forces data to be downloaded even if it has been 
        downloaded before, defaults to `False`.

    :param bool jit_loading:
        If `True` (the default) only downloads and loads data into 
        memory when it is required (jit = just in time). If `False` 
        all drawings will be downloaded and loaded into memory.

    :param bool print_messages:
        If ``True`` (the default), status messages will be printed
        stating when data is being downloaded or loaded.

    :param string cache_dir:
        Specify a cache directory to use when downloading data files,
        defaults to `./.quickdrawcache`.
    """
    def __init__(self, max_drawings=1000, refresh_data=False, jit_loading=True, print_messages=True, cache_dir=CACHE_DIR):
        self._print_messages = print_messages
        self._refresh_data = refresh_data
        self._max_drawings = max_drawings
        self._cache_dir = cache_dir

        self._drawing_groups = {}

        # if not jit (just in time) loading, load all drawings
        if not jit_loading:
            self.load_all_drawings()

    def get_drawing(self, name, index=None):
        """
        Get a drawing.

        Returns an instance of :class:`QuickDrawing` representing a single 
        Quick, Draw drawing.

        :param string name:
            The name of the drawing to get (anvil, ant, aircraft, etc).

        :param int index:
            The index of the drawing to get.

            If `None` (the default) a random drawing will be returned.
        """
        return self.get_drawing_group(name).get_drawing(index)

    def get_drawing_group(self, name):
        # has this drawing group been loaded to memory
        if name not in self._drawing_groups.keys():
            drawings = QuickDrawDataGroup(
                name, 
                max_drawings=self._max_drawings, 
                refresh_data=self._refresh_data, 
                print_messages=self._print_messages,
                cache_dir=self._cache_dir)
            self._drawing_groups[name] = drawings

        return self._drawing_groups[name]

    def load_all_drawings(self):
        for drawing_group in QUICK_DRAWING_NAMES:
            self.get_drawing_group(drawing_group)

    @property
    def drawing_names(self):
        return QUICK_DRAWING_NAMES


class QuickDrawDataGroup():
    """
    Allows interaction with a group of Quick, Draw! drawings.

    The following example will load the ant group of drawings and get a 
    single drawing::

        from quickdraw import QuickDrawDataGroup

        ants = QuickDrawDataGroup("ant")
        ants.get_drawing()

    :param string name:
        The name of the drawings to be loaded (anvil, ant, aircraft, etc).

    :param int max_drawings:
        The maximum number of drawings to be loaded into memory,
        defaults to 1000.

    :param bool refresh_data:
        If `True` forces data to be downloaded even if it has been 
        downloaded before, defaults to `False`.

    :param bool print_messages:
        If ``True`` (the default), status messages will be printed
        stating when data is being downloaded or loaded.

    :param string cache_dir:
        Specify a cache directory to use when downloading data files,
        defaults to `./.quickdrawcache`.
    """
    def __init__(self, name, max_drawings=1000, refresh_data=False, print_messages=True, cache_dir=CACHE_DIR):
        
        if name not in QUICK_DRAWING_NAMES:
            raise ValueError("{} is not a valid google quick drawing".format(name))
        
        self._name = name
        self._print_messages = print_messages
        self._max_drawings = max_drawings
        self._cache_dir = cache_dir
        
        self._drawings = []

        # get the binary file for this drawing?
        filename = path.join(self._cache_dir, QUICK_DRAWING_FILES[name])
        
        # if the binary file doesn't exist or refresh_data is True, download the file
        if not path.isfile(filename) or refresh_data:
            
            # if the cache dir doesnt exist, create it
            if not path.isdir(self._cache_dir):
                makedirs(self._cache_dir)
            
            # download the binary file
            url = BINARY_URL + QUICK_DRAWING_FILES[name]
            self._download_drawings_binary(url, filename)

        # load the drawings
        self._load_drawings(filename)
            
    def _download_drawings_binary(self, url, filename):
        
        try:
            r = get(url, stream=True)
            
            self._print_message("downloading {} from {}".format(self._name, url))
            
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)

        except ConnectionError as e:
            raise Exception("connection error - you need to be connected to the internet to download {} drawings".format(self._name))

        # check file exists
        if not path.isfile(filename):
            raise Exception("something went wrong with the download of {} - file not found!".format(self._name))
        else:
            self._print_message("download complete")

    def _load_drawings(self, filename):

        self._print_message("loading {} drawings".format(self._name))

        binary_file = open(filename, 'rb')
        self._drawings_cache = []

        self._drawing_count = 0
        self._current_drawing = -1
        
        drawings_to_load = self._max_drawings
        if self._max_drawings is None:
            # bit hacky! but efficient...
            drawings_to_load = 9999999999999

        while self._drawing_count < drawings_to_load:
            try:
                key_id, = struct.unpack('Q', binary_file.read(8))
                countrycode, = struct.unpack('2s', binary_file.read(2))
                recognized, = struct.unpack('b', binary_file.read(1))
                timestamp, = struct.unpack('I', binary_file.read(4))
                n_strokes, = struct.unpack('H', binary_file.read(2))
                image = []

                for i in range(n_strokes):
                    n_points, = struct.unpack('H', binary_file.read(2))
                    fmt = str(n_points) + 'B'
                    x = struct.unpack(fmt, binary_file.read(n_points))
                    y = struct.unpack(fmt, binary_file.read(n_points))
                    image.append((x, y))

                self._drawings.append({
                    'key_id': key_id,
                    'countrycode': countrycode,
                    'recognized': recognized,
                    'timestamp': timestamp,
                    'n_strokes': n_strokes,
                    'image': image
                })

            # nothing left to read
            except struct.error:
                break

            self._drawing_count += 1

        self._print_message("load complete")

    def _print_message(self, message):
        if self._print_messages:
            print(message)

    @property
    def drawing_count(self):
        """
        Returns the number of drawings loaded.
        """
        return self._drawing_count

    @property
    def drawings(self):
        """
        An iterator of all the drawings loaded in this group. Returns a :class:`QuickDrawing` object.

        Load the anvil group of drawings and iterate through them::

            from quickdraw import QuickDrawDataGroup

            anvils = QuickDrawDataGroup("anvil")
            for anvil in anvils.drawings:
                print(anvil)
        """
        while True:
            self._current_drawing += 1
            if self._current_drawing == self._drawing_count - 1:
                # reached the end to the drawings
                self._current_drawing = 0
                raise StopIteration()
            else:
                # yield the next drawing
                yield self.get_drawing(index = self._current_drawing)

    def get_drawing(self, index=None):
        """
        Get a drawing from this group.

        Returns an instance of :class:`QuickDrawing` representing a single 
        Quick, Draw drawing.

        Get a single anvil drawing::

            from quickdraw import QuickDrawDataGroup

            anvils = QuickDrawDataGroup("anvil")
            anvil = anvils.get_drawing()

        :param int index:
            The index of the drawing to get.

            If `None` (the default) a random drawing will be returned.
        """
        if index is None:
            return QuickDrawing(self._name, choice(self._drawings))
        else:
            if index < self.drawing_count - 1:
                return QuickDrawing(self._name, self._drawings[index])
            else:
                raise IndexError("index {} out of range, there are {} drawings".format(index, self.drawing_count))


class QuickDrawing():
    """
    Represents a single Quick, Draw! drawing.
    """
    def __init__(self, name, drawing_data):
        self._name =name
        self._drawing_data = drawing_data
        self._strokes = None

    @property
    def name(self):
        """
        Returns the name of the drawing (anvil, aircraft, ant, etc).
        """
        return self._name

    @property
    def key_id(self):
        """
        Returns the id of the drawing.
        """
        return self._drawing_data["key_id"]

    @property
    def countrycode(self):
        """
        Returns the country code for the drawing.
        """
        return self._drawing_data["countrycode"]

    @property
    def recognized(self):
        """
        Returns a boolean representing whether the drawing was recognized.
        """
        return bool(self._drawing_data["recognized"])

    @property
    def timestamp(self):
        """
        Returns the time the drawing was created (in seconds since the epoch).
        """
        return self._drawing_data["timestamp"]

    @property
    def no_of_strokes(self):
        """
        Returns the number of pen strokes used to create the drawing.
        """
        return self._drawing_data["n_strokes"]

    @property
    def image_data(self):
        """
        Returns the raw image data as list of strokes with a list of X 
        co-ordinates and a list of Y co-ordinates.

        Co-ordinates are aligned to the top-left hand corner with values
        from 0 to 255.

        See https://github.com/googlecreativelab/quickdraw-dataset#simplified-drawing-files-ndjson
        for more information regarding how the data is represented.
        """
        return self._drawing_data["image"]
    
    @property
    def strokes(self):
        """
        Returns a list of pen strokes containing a list of (x,y) coordinates which make up the drawing.

        To iterate though the strokes data use::
        
            from quickdraw import QuickDrawData

            qd = QuickDrawData()

            anvil = qd.get_drawing("anvil")
            for stroke in anvil.strokes:
                for x, y in stroke:
                    print("x={} y={}".format(x, y)) 
        """
        # load the strokes
        if self._strokes is None:
            
            self._strokes = []
            for stroke in self.image_data:
                points = []
                xs = stroke[0]
                ys = stroke[1]

                if len(xs) != len(ys):
                    raise Exception("something is wrong, different number of x's and y's")

                for point in range(len(xs)):
                    x = xs[point]
                    y = ys[point]
                    points.append((x,y))
                self._strokes.append(points)

        return self._strokes
                
    def __str__(self):
        return "QuickDrawing key_id={}".format(self.key_id)

