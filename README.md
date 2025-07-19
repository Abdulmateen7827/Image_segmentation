# Vegetable Classification API

A FastAPI-based REST API for classifying Nigerian vegetables using deep learning. The API supports image upload and returns predictions with confidence scores for 10 different vegetable classes.

## 🌿 Supported Vegetables

- Bitterleaf
- Efirin
- Ewedu
- amunututu
- elegede
- soko
- tete
- ugu
- uziza leave
- waterleaf

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **HEIC Support**: Handles HEIC, PNG, JPG, and other image formats
- **Real-time Predictions**: Quick inference with confidence scores
- **Batch Processing**: Support for multiple image predictions
- **Health Monitoring**: Built-in health checks and monitoring
- **CORS Support**: Cross-origin resource sharing enabled
- **Auto-documentation**: Interactive API documentation with Swagger UI

## 📁 Project Structure

```
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── render.yaml            # Render deployment config
├── test_api.py            # API testing script
├── notebook/
│   └── faruq1.h5         # Trained model
└── README.md              # This file
```

## 🛠️ Installation

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd vegetable-classification-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build the Docker image**
```bash
docker build -t vegetable-api .
```

2. **Run the container**
```bash
docker run -p 8000:8000 vegetable-api
```

## 🌐 API Endpoints

### Base URL
- **Local**: `http://localhost:8000`
- **Render**: `https://your-app-name.onrender.com`

### Available Endpoints

#### 1. Health Check
```http
GET /health
```
Returns API health status and model loading status.

#### 2. Root Endpoint
```http
GET /
```
Returns API information and available classes.

#### 3. Get Classes
```http
GET /classes
```
Returns all available vegetable classes and their mappings.

#### 4. Single Image Prediction
```http
POST /predict
```
Upload a single image and get prediction results.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "predicted_class": 3,
  "predicted_class_name": "amunututu",
  "confidence": 0.9234,
  "all_confidences": {
    "amunututu": 0.9234,
    "waterleaf": 0.0456,
    "Bitterleaf": 0.0123,
    ...
  },
  "inference_time": 0.0456,
  "status": "success"
}
```

#### 5. Batch Prediction
```http
POST /predict-batch
```
Upload multiple images and get predictions for all.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `files` (multiple image files)

**Response:**
```json
{
  "predictions": [
    {
      "file": "image1.jpg",
      "predicted_class": 3,
      "predicted_class_name": "amunututu",
      "confidence": 0.9234,
      "all_confidences": {...},
      "inference_time": 0.0456,
      "status": "success"
    },
    ...
  ]
}
```

## 🚀 Deployment on Render

### Automatic Deployment

1. **Connect your GitHub repository to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**
   - **Name**: `vegetable-classification-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your API

### Manual Deployment

1. **Push your code to GitHub**
```bash
git add .
git commit -m "Add FastAPI deployment"
git push origin main
```

2. **Create a new Web Service on Render**
   - Use the `render.yaml` configuration
   - Or manually configure as described above

## 🧪 Testing

### Local Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

### Manual Testing

1. **Test health endpoint**
```bash
curl http://localhost:8000/health
```

2. **Test prediction**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

3. **Test with Python requests**
```python
import requests

# Upload image and get prediction
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
    
result = response.json()
print(f"Predicted: {result['predicted_class_name']}")
print(f"Confidence: {result['confidence']}")
```

## 📊 API Documentation

Once deployed, you can access:

- **Interactive API Docs**: `https://your-app.onrender.com/docs`
- **ReDoc Documentation**: `https://your-app.onrender.com/redoc`
- **OpenAPI Schema**: `https://your-app.onrender.com/openapi.json`

## 🔧 Configuration

### Environment Variables

- `PORT`: Server port (set by Render)
- `PYTHON_VERSION`: Python version (3.9.0)

### Model Configuration

- **Model Path**: `notebook/faruq1.h5`
- **Input Size**: 224x224 pixels
- **Supported Formats**: HEIC, PNG, JPG, JPEG, BMP

## 📈 Performance

- **Model Loading**: ~2-5 seconds on startup
- **Inference Time**: ~0.05-0.1 seconds per image
- **Memory Usage**: ~500MB-1GB (depending on model size)
- **Concurrent Requests**: Supports multiple simultaneous predictions

## 🛡️ Error Handling

The API includes comprehensive error handling:

- **Invalid File Type**: Returns 400 for non-image files
- **Model Loading Errors**: Returns 500 if model fails to load
- **Preprocessing Errors**: Returns 400 for corrupted images
- **Prediction Errors**: Returns 500 for inference failures

## 🔄 Monitoring

- **Health Checks**: Automatic health monitoring
- **Startup Logs**: Model loading status
- **Request Logs**: Prediction timing and results
- **Error Logs**: Detailed error information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the health endpoint at `/health`

---

**Note**: Make sure your model file (`notebook/faruq1.h5`) is included in your repository or uploaded to Render during deployment.



