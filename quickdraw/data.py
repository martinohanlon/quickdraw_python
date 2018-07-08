import struct
from random import choice
from os import path, makedirs
from requests import get
from requests.exceptions import ConnectionError

from .names import QUICK_DRAWING_FILES, QUICK_DRAWING_NAMES

BINARY_URL = "https://storage.googleapis.com/quickdraw_dataset/full/binary/"
CACHE_DIR = path.join(".",".quickdrawcache")


class QuickDrawData():
    def __init__(self, max_drawings=1000, refresh_data=False, jit_loading=True, print_messages=True):
        self._print_messages = print_messages
        self._refresh_data = refresh_data
        self._max_drawings = max_drawings

        self._drawing_groups = {}

        # if not jit (just in time) loading, load all drawings
        if not jit_loading:
            self.load_all_drawings()

    def get_drawing(self, name, index=None):
        return self.get_drawing_group(name).get_drawing(index)

    def get_drawing_group(self, name):
        # has this drawing group been loaded to memory
        if name not in self._drawing_groups.keys():
            drawings = QuickDrawDataGroup(
                name, 
                max_drawings=self._max_drawings, 
                refresh_data=self._refresh_data, 
                print_messages=self._print_messages)
            self._drawing_groups[name] = drawings

        return self._drawing_groups[name]

    def load_all_drawings(self):
        for drawing_group in QUICK_DRAWING_NAMES:
            self.get_drawing_group(drawing_group)

    @property
    def drawing_names(self):
        return QUICK_DRAWING_NAMES


class QuickDrawDataGroup():

    def __init__(self, name, max_drawings=1000, refresh_data=False, print_messages=True):
        
        if name not in QUICK_DRAWING_NAMES:
            raise ValueError("{} is not a valid google quick drawing".format(name))
        
        self._name = name
        self._print_messages = print_messages
        self._max_drawings = max_drawings
        
        self._drawings = []

        # get the binary file for this drawing?
        filename = path.join(CACHE_DIR, QUICK_DRAWING_FILES[name])
        print(filename)
        
        # if the binary file doesn't exist or refresh_data is True, download the file
        if not path.isfile(filename) or refresh_data:
            
            # if the cache dir doesnt exist, create it
            if not path.isdir(CACHE_DIR):
                makedirs(CACHE_DIR)
            
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

            except struct.error:
                break

            self._drawing_count = self._drawing_count + 1

        self._print_message("load complete")

    def _print_message(self, message):
        if self._print_messages:
            print(message)

    @property
    def drawing_count(self):
        return self._drawing_count

    def get_drawing(self, index=None):
        if index is None:
            return QuickDrawing(self._name, choice(self._drawings))
        else:
            if index < self.drawing_count - 1:
                return QuickDrawing(self._name, self._drawings[index])
            else:
                raise IndexError("index {} out of range, there are {} drawings".format(index, self.drawing_count))


class QuickDrawing():
    def __init__(self, name, drawing_data):
        self._name =name
        self._drawing_data = drawing_data
        self._strokes = None

    @property
    def name(self):
        return self._name

    @property
    def key_id(self):
        return self._drawing_data["key_id"]

    @property
    def countrycode(self):
        return self._drawing_data["countrycode"]

    @property
    def recognized(self):
        return self._drawing_data["recognized"]

    @property
    def timestamp(self):
        return self._drawing_data["timestamp"]

    @property
    def no_of_strokes(self):
        return self._drawing_data["n_strokes"]

    @property
    def image_data(self):
        return self._drawing_data["image"]
    
    @property
    def strokes(self):
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

