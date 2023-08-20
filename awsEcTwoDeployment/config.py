# in class config , add a variable that specifies path to .pb file that will be stored here. However, I am not sure how much of a good idea would it be to put that kind of 
# memory consuming file into production


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"


    PATH_TO_CKPT = 'rest_apis/static/object_detection_files/frozen_inference_graph.pb'
    PATH_TO_LABELS = 'rest_apis/static/object_detection_files/mscoco_label_map.pbtxt'

    IMAGE_PATH = 'rest_apis/static/img'

    OBJECT_NOT_FOUND = "rest_apis/static/img/defaults/notFound.png"

    NUM_CLASSES = 90

    SESSION_COOKIE_SECURE = True

    ENCODER_PATH = 'rest_apis/static/object_detection_files/encoder-5-3000.pkl'
    DECODER_PATH = 'rest_apis/static/object_detection_files/decoder-5-3000.pkl'
    VOCAB_PATH = 'rest_apis/static/object_detection_files/vocab.pkl'
    EMBED_SIZE = 256
    HIDDEN_SIZE = 512
    NUM_LAYERS = 1

    # REDIS_URL = "redis://redis:6379"

    # # REDIS_URL_1 = "http://120.0.0.1:6379"

    # REDIS_URL_2 = "redis://redis.io:6379"

    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]



class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False


    # ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "png"]
    # MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
    # CLIENT_IMAGES = "appOne/static/client/forImg"


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False