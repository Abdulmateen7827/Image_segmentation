# Mobile App Integration Guide

This guide provides instructions for integrating the Vegetable Classification API with mobile applications.

## 📱 Mobile-Optimized Endpoints

### Primary Mobile Endpoint
```
POST /predict-mobile
```

**Purpose**: Optimized for mobile camera images with simplified response format.

### Standard Endpoint (Alternative)
```
POST /predict
```

**Purpose**: Full-featured endpoint with detailed confidence scores.

## 🔧 API Configuration

### Base URLs
- **Development**: `http://localhost:8000`
- **Production**: `https://your-app-name.onrender.com`

### Headers
```http
Content-Type: multipart/form-data
Accept: application/json
```

## 📱 Mobile App Integration Examples

### iOS (Swift)

```swift
import UIKit

class VegetableClassifier {
    private let baseURL = "https://your-app-name.onrender.com"
    
    func classifyVegetable(image: UIImage, completion: @escaping (Result<PredictionResult, Error>) -> Void) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            completion(.failure(APIError.invalidImage))
            return
        }
        
        let url = URL(string: "\(baseURL)/predict-mobile")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add image data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(APIError.noData))
                return
            }
            
            do {
                let result = try JSONDecoder().decode(PredictionResult.self, from: data)
                completion(.success(result))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// Response models
struct PredictionResult: Codable {
    let success: Bool
    let prediction: Prediction?
    let top3: [TopPrediction]?
    let inferenceTime: Double?
    let timestamp: Double?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case success, prediction, top3 = "top_3", inferenceTime = "inference_time", timestamp, error
    }
}

struct Prediction: Codable {
    let className: String
    let confidence: Double
    let classId: Int
    
    enum CodingKeys: String, CodingKey {
        case className = "class", confidence, classId = "class_id"
    }
}

struct TopPrediction: Codable {
    let className: String
    let confidence: Double
    
    enum CodingKeys: String, CodingKey {
        case className = "class", confidence
    }
}

enum APIError: Error {
    case invalidImage
    case noData
}
```

### Android (Kotlin)

```kotlin
import android.graphics.Bitmap
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.File

class VegetableClassifier {
    private val baseURL = "https://your-app-name.onrender.com"
    private val client = OkHttpClient()
    
    fun classifyVegetable(bitmap: Bitmap, callback: (Result<PredictionResult>) -> Unit) {
        val byteArrayOutputStream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80, byteArrayOutputStream)
        val imageBytes = byteArrayOutputStream.toByteArray()
        
        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart(
                "file",
                "image.jpg",
                RequestBody.create("image/jpeg".toMediaType(), imageBytes)
            )
            .build()
        
        val request = Request.Builder()
            .url("$baseURL/predict-mobile")
            .post(requestBody)
            .build()
        
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                callback(Result.failure(e))
            }
            
            override fun onResponse(call: Call, response: Response) {
                val responseBody = response.body?.string()
                if (response.isSuccessful && responseBody != null) {
                    try {
                        val jsonObject = JSONObject(responseBody)
                        val result = parsePredictionResult(jsonObject)
                        callback(Result.success(result))
                    } catch (e: Exception) {
                        callback(Result.failure(e))
                    }
                } else {
                    callback(Result.failure(Exception("Request failed")))
                }
            }
        })
    }
    
    private fun parsePredictionResult(json: JSONObject): PredictionResult {
        return PredictionResult(
            success = json.optBoolean("success"),
            prediction = if (json.has("prediction")) {
                val predJson = json.getJSONObject("prediction")
                Prediction(
                    className = predJson.getString("class"),
                    confidence = predJson.getDouble("confidence"),
                    classId = predJson.getInt("class_id")
                )
            } else null,
            top3 = if (json.has("top_3")) {
                val top3Array = json.getJSONArray("top_3")
                val top3List = mutableListOf<TopPrediction>()
                for (i in 0 until top3Array.length()) {
                    val item = top3Array.getJSONObject(i)
                    top3List.add(
                        TopPrediction(
                            className = item.getString("class"),
                            confidence = item.getDouble("confidence")
                        )
                    )
                }
                top3List
            } else null,
            inferenceTime = json.optDouble("inference_time"),
            timestamp = json.optDouble("timestamp"),
            error = json.optString("error")
        )
    }
}

data class PredictionResult(
    val success: Boolean,
    val prediction: Prediction?,
    val top3: List<TopPrediction>?,
    val inferenceTime: Double?,
    val timestamp: Double?,
    val error: String?
)

data class Prediction(
    val className: String,
    val confidence: Double,
    val classId: Int
)

data class TopPrediction(
    val className: String,
    val confidence: Double
)
```

### React Native

```javascript
import { Platform } from 'react-native';

class VegetableClassifier {
  constructor() {
    this.baseURL = 'https://your-app-name.onrender.com';
  }

  async classifyVegetable(imageUri) {
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'image.jpg',
      });

      const response = await fetch(`${this.baseURL}/predict-mobile`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Classification error:', error);
      throw error;
    }
  }
}

// Usage example
const classifier = new VegetableClassifier();

// For camera capture
const handleCameraCapture = async (imageUri) => {
  try {
    const result = await classifier.classifyVegetable(imageUri);
    
    if (result.success) {
      console.log('Predicted:', result.prediction.class);
      console.log('Confidence:', result.prediction.confidence);
      console.log('Top 3:', result.top3);
    } else {
      console.error('Classification failed:', result.error);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Flutter

```dart
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class VegetableClassifier {
  static const String baseURL = 'https://your-app-name.onrender.com';

  static Future<PredictionResult> classifyVegetable(File imageFile) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseURL/predict-mobile'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          imageFile.path,
          filename: 'image.jpg',
        ),
      );

      var response = await request.send();
      var responseData = await response.stream.bytesToString();
      var jsonData = json.decode(responseData);

      return PredictionResult.fromJson(jsonData);
    } catch (e) {
      throw Exception('Classification failed: $e');
    }
  }
}

class PredictionResult {
  final bool success;
  final Prediction? prediction;
  final List<TopPrediction>? top3;
  final double? inferenceTime;
  final double? timestamp;
  final String? error;

  PredictionResult({
    required this.success,
    this.prediction,
    this.top3,
    this.inferenceTime,
    this.timestamp,
    this.error,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    return PredictionResult(
      success: json['success'] ?? false,
      prediction: json['prediction'] != null 
          ? Prediction.fromJson(json['prediction']) 
          : null,
      top3: json['top_3'] != null 
          ? List<TopPrediction>.from(
              json['top_3'].map((x) => TopPrediction.fromJson(x)))
          : null,
      inferenceTime: json['inference_time']?.toDouble(),
      timestamp: json['timestamp']?.toDouble(),
      error: json['error'],
    );
  }
}

class Prediction {
  final String className;
  final double confidence;
  final int classId;

  Prediction({
    required this.className,
    required this.confidence,
    required this.classId,
  });

  factory Prediction.fromJson(Map<String, dynamic> json) {
    return Prediction(
      className: json['class'],
      confidence: json['confidence'].toDouble(),
      classId: json['class_id'],
    );
  }
}

class TopPrediction {
  final String className;
  final double confidence;

  TopPrediction({
    required this.className,
    required this.confidence,
  });

  factory TopPrediction.fromJson(Map<String, dynamic> json) {
    return TopPrediction(
      className: json['class'],
      confidence: json['confidence'].toDouble(),
    );
  }
}
```

## 📊 Response Format

### Mobile-Optimized Response (`/predict-mobile`)
```json
{
  "success": true,
  "prediction": {
    "class": "amunututu",
    "confidence": 0.923,
    "class_id": 3
  },
  "top_3": [
    {
      "class": "amunututu",
      "confidence": 0.923
    },
    {
      "class": "waterleaf",
      "confidence": 0.046
    },
    {
      "class": "Bitterleaf",
      "confidence": 0.012
    }
  ],
  "inference_time": 0.045,
  "timestamp": 1703123456.789
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here",
  "timestamp": 1703123456.789
}
```

## 🔧 Best Practices

### 1. Image Optimization
- **Compression**: Use 80% JPEG quality for optimal size/quality balance
- **Resolution**: Resize to max 1024x1024 before upload
- **Format**: Prefer JPEG for photos, PNG for screenshots

### 2. Network Handling
- **Timeout**: Set 30-second timeout for requests
- **Retry Logic**: Implement exponential backoff for failed requests
- **Offline Support**: Cache recent predictions locally

### 3. User Experience
- **Loading States**: Show loading indicator during classification
- **Error Handling**: Display user-friendly error messages
- **Results Display**: Show confidence percentage and top 3 predictions

### 4. Performance
- **Image Caching**: Cache processed images locally
- **Batch Processing**: For multiple images, use `/predict-batch`
- **Background Processing**: Process images in background threads

## 🧪 Testing

### Test with Sample Images
```bash
# Test mobile endpoint
curl -X POST "https://your-app-name.onrender.com/predict-mobile" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

### Test Health Check
```bash
curl "https://your-app-name.onrender.com/health"
```

## 📱 Mobile App Features

### Recommended Features
1. **Camera Integration**: Direct camera capture
2. **Gallery Selection**: Choose from photo library
3. **Real-time Preview**: Show camera preview
4. **Results History**: Save and display past predictions
5. **Offline Mode**: Basic offline functionality
6. **Share Results**: Share predictions via social media

### UI/UX Considerations
- **Loading Animation**: Show progress during classification
- **Confidence Display**: Visual confidence indicators
- **Error Messages**: Clear, actionable error messages
- **Accessibility**: Support for screen readers
- **Dark Mode**: Support for dark/light themes

## 🔒 Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **Input Validation**: Validate images on client side
3. **Rate Limiting**: Implement request rate limiting
4. **Error Logging**: Log errors for debugging
5. **User Privacy**: Don't store sensitive user data

## 📈 Analytics

### Recommended Metrics
- **Classification Success Rate**: Track successful vs failed predictions
- **Response Time**: Monitor API response times
- **User Engagement**: Track feature usage
- **Error Rates**: Monitor different error types
- **Device Information**: Track device types and OS versions

This integration guide provides everything needed to connect mobile apps to your vegetable classification API! 