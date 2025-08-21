# Web Service for Object Detection and Image Captioning

A Flask-based web service that combines AI-powered object detection and image captioning to find similar images through Google image search. Users can upload an image and choose between two AI models to discover visually similar content.

## 🚀 Features

- **Dual AI Processing Modes**:
  - **Object Detection**: Uses TensorFlow to detect objects in images and search for similar object combinations
  - **Image Captioning**: Uses PyTorch CNN-LSTM model to generate descriptive captions and find matching images

- **Asynchronous Processing**: Background task processing using Redis Queue (RQ) for handling computationally intensive AI operations

- **Real-time Web Interface**: AJAX-based file upload with live progress updates and dynamic image gallery display

- **Google Image Integration**: Automated web scraping to find and display similar images from Google Images

## 🏗️ Technical Architecture

### Backend Stack
- **Framework**: Flask with Flask-RESTful
- **Task Queue**: Redis + RQ for background processing
- **Configuration**: Environment-based configs (Development, Production, Testing)

### AI Models
- **Object Detection**: TensorFlow frozen graph model (COCO dataset, 90 object classes)
- **Image Captioning**: PyTorch encoder-decoder architecture
  - CNN Encoder: Pre-trained ResNet-152
  - RNN Decoder: LSTM with attention mechanism

### Frontend
- **Interface**: HTML5 with jQuery AJAX
- **Real-time Updates**: Polling-based status checking
- **Image Display**: Dynamic gallery generation

## 📁 Project Structure

```
awsEcTwoDeployment/
├── app.py                          # Main Flask application entry point
├── config.py                       # Configuration classes (Dev/Prod/Test)
├── check.py                        # Health check utilities
├── rest_apis/
│   ├── __init__.py                 # Flask app initialization
│   ├── api_file_one.py             # Main API endpoints
│   ├── task.py                     # Core AI processing tasks
│   ├── subTask.py                  # Image captioning functionality
│   ├── model.py                    # PyTorch model definitions
│   ├── build_vocab.py              # Vocabulary handling for captioning
│   ├── imageUrlsGoogleSearch.py    # Google Images scraping
│   ├── static/
│   │   └── main.js                 # Frontend JavaScript
│   ├── templates/
│   │   └── public/
│   │       ├── upload_image_ajax_detection.html  # Main upload interface
│   │       ├── response.html       # Image gallery template
│   │       └── templates/
│   │           └── public_template.html  # Base template
│   └── utils/
│       ├── label_map_util.py       # TensorFlow object detection utilities
│       └── string_int_label_map_pb2.py  # Protocol buffer definitions
└── image_finder_demo.mp4           # Demo video
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- Redis server
- Required AI model files (see Model Setup section)

### Python Dependencies
```bash
pip install flask flask-restful flask-script
pip install tensorflow torch torchvision
pip install redis rq
pip install pillow numpy beautifulsoup4
pip install pathlib datetime
```

### Model Setup
The application requires pre-trained model files to be placed in `rest_apis/static/object_detection_files/`:

**Object Detection Models:**
- `frozen_inference_graph.pb` - TensorFlow frozen graph
- `mscoco_label_map.pbtxt` - COCO dataset label mapping

**Image Captioning Models:**
- `encoder-5-3000.pkl` - CNN encoder weights
- `decoder-5-3000.pkl` - LSTM decoder weights  
- `vocab.pkl` - Vocabulary mapping file

### Redis Configuration
1. Install and start Redis server
2. Default configuration uses `redis://redis:6379/0`
3. Update `config.py` if using different Redis settings

## 🚀 Usage

### Starting the Application
```bash
python app.py
```
The service will be available at `http://127.0.0.1:5000`

### API Endpoints

#### 1. Health Check
```http
GET /
```
Returns basic service status.

#### 2. Upload and Process Image
```http
POST /find-images
Content-Type: multipart/form-data

Parameters:
- file: Image file (JPEG, PNG, GIF)
- model: "objects" or "story"
```

**Response:**
```json
{
  "taskId": "unique-task-id",
  "imgPath": "static/img/timestamped_filename.jpg"
}
```

#### 3. Check Processing Status
```http
POST /getTheUrlsOfImagesFound
Content-Type: application/x-www-form-urlencoded

Parameters:
- taskId: Task ID from upload response
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "task_id": "task-id",
    "task_status": "finished",
    "task_result": ["url1", "url2", "url3"]
  }
}
```

#### 4. Generate Image Gallery
```http
POST /getImageDivs
Content-Type: application/x-www-form-urlencoded

Parameters:
- imageUrls[]: Array of image URLs
```

### Web Interface Usage

1. **Upload Image**: Click "Choose File" and select an image
2. **Select Model**: Choose between "Objects" (detection) or "Story" (captioning)
3. **Process**: Click "Discover Similar" to start processing
4. **View Results**: Similar images will appear automatically below

## ⚙️ Configuration

### Environment Configuration
The application supports three environments via `config.py`:

- **Development**: Debug enabled, local file paths
- **Production**: Optimized settings, secure cookies
- **Testing**: Test database, disabled security

### Key Configuration Parameters
```python
# AI Model Paths
PATH_TO_CKPT = 'rest_apis/static/object_detection_files/frozen_inference_graph.pb'
PATH_TO_LABELS = 'rest_apis/static/object_detection_files/mscoco_label_map.pbtxt'
ENCODER_PATH = 'rest_apis/static/object_detection_files/encoder-5-3000.pkl'
DECODER_PATH = 'rest_apis/static/object_detection_files/decoder-5-3000.pkl'
VOCAB_PATH = 'rest_apis/static/object_detection_files/vocab.pkl'

# Model Parameters  
NUM_CLASSES = 90
EMBED_SIZE = 256
HIDDEN_SIZE = 512
NUM_LAYERS = 1

# Storage
IMAGE_PATH = 'rest_apis/static/img'
OBJECT_NOT_FOUND = 'rest_apis/static/img/defaults/notFound.png'

# Redis Queue
REDIS_URL = 'redis://redis:6379/0'
QUEUES = ['default']
```

## 🤖 AI Models Details

### Object Detection Model
- **Architecture**: TensorFlow frozen graph model
- **Dataset**: COCO (Common Objects in Context)
- **Classes**: 90 object categories
- **Confidence Threshold**: 50%
- **Output**: Object names with confidence scores

**Processing Flow:**
1. Image preprocessing and tensor conversion
2. Object detection with bounding boxes
3. Confidence filtering and object extraction
4. Search query generation from detected objects
5. Google image search with constructed query

### Image Captioning Model
- **Encoder**: Pre-trained ResNet-152 CNN
- **Decoder**: LSTM with attention mechanism
- **Vocabulary**: Custom vocabulary from training dataset
- **Max Sequence Length**: 20 words

**Processing Flow:**
1. Image resize and normalization
2. Feature extraction using CNN encoder
3. Caption generation using LSTM decoder
4. Caption-based Google image search

## 🔄 Processing Workflow

### Background Task Processing
1. **Upload**: Image saved with timestamp
2. **Queue**: Task added to Redis queue
3. **Processing**: AI model processes image asynchronously
4. **Search**: Google Images scraped for similar content
5. **Response**: URLs returned to frontend
6. **Display**: Gallery rendered with found images

### Error Handling
- **No Objects Detected**: Returns default "not found" image
- **Model Loading Errors**: Graceful degradation with error messages
- **Network Issues**: Timeout handling for image searches
- **Invalid Formats**: File type validation and conversion

## 🔧 Development Notes

### Adding New Models
1. Place model files in `rest_apis/static/object_detection_files/`
2. Update configuration paths in `config.py`
3. Implement processing logic in `task.py` or `subTask.py`
4. Add model selection options in frontend

### Customizing Search Logic
- **Object Detection**: Modify query generation in `task.py`
- **Image Captioning**: Adjust caption processing in `subTask.py`
- **Search Parameters**: Update scraping logic in `imageUrlsGoogleSearch.py`

### Performance Optimization
- **Model Caching**: Models loaded once per worker process
- **Image Preprocessing**: Batch processing for multiple images
- **Queue Management**: Multiple worker processes for scaling
- **Memory Management**: Proper cleanup of large model objects

## 🐛 Troubleshooting

### Common Issues

**Model Files Not Found**
```
Solution: Ensure all required .pb, .pkl files are in correct directory
Check: rest_apis/static/object_detection_files/ contains all model files
```

**Redis Connection Error**
```
Solution: Verify Redis server is running
Check: Redis configuration in config.py matches your setup
```

**TensorFlow/PyTorch Compatibility**
```
Solution: Use compatible versions (TF 1.x for frozen graphs)
Check: Model files match framework versions
```

**Image Processing Errors**
```
Solution: Verify image format and size constraints
Check: PIL can open and process uploaded images
```

## 📋 Requirements Summary

### System Requirements
- Python 3.7+
- Redis server
- 2GB+ RAM (for model loading)
- 1GB+ storage (for model files)

### Python Packages
- flask, flask-restful, flask-script
- tensorflow (1.x for frozen graph compatibility)
- torch, torchvision
- redis, rq
- pillow, numpy, beautifulsoup4

### Model Files (Not Included)
- Object detection frozen graph (~100MB)
- Image captioning encoder/decoder (~50MB each)
- Vocabulary and label mapping files

## 📄 License

This project is for educational and research purposes. Please ensure compliance with:
- TensorFlow model licenses
- PyTorch model licenses  
- Google Images terms of service
- COCO dataset license terms

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all models work correctly
5. Submit pull request with detailed description

---

**Note**: This application requires pre-trained AI models that are not included in the repository due to size constraints. 

