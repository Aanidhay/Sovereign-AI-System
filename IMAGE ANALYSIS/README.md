# Image Analysis Application

A web application that allows users to upload images and analyze them using local computer vision techniques - no external APIs required!

## Features

- **Image Upload**: Support for JPEG, PNG, WebP, and GIF formats (max 16MB)
- **Drag & Drop Interface**: Easy file upload with drag-and-drop functionality
- **Local Analysis**: Analyze images using OpenCV and PIL without any external APIs
- **Multiple Analysis Types**: 
  - Color analysis (dominant colors, brightness, contrast)
  - Dimension analysis (size, resolution, aspect ratio)
  - Sharpness and edge detection
  - Brightness and exposure assessment
- **Responsive Design**: Modern, mobile-friendly interface using Tailwind CSS
- **Session Management**: Maintains uploaded image state during the session

## Installation

1. Install Python 3.8 or higher
2. Clone or download this project
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Upload an Image**:
   - Click the upload area or drag and drop an image
   - Supported formats: JPEG, PNG, WebP, GIF
   - Maximum file size: 16MB

2. **Ask Questions**:
   - Once uploaded, enter your question in the text field
   - Examples:
     - "What do you see in this image?"
     - "What colors are dominant?"
     - "Is this image bright or dark?"
     - "What are the dimensions?"
     - "Is this image sharp or blurry?"
     - "Describe the visual properties"

3. **Get Analysis**:
   - Click "Analyze Image" to get detailed technical analysis
   - Ask multiple questions about the same image
   - Click "Upload New Image" to start over

## Analysis Capabilities

The application provides detailed analysis using computer vision techniques:

### 🎨 **Color Analysis**
- Dominant color detection (RGB values)
- Brightness and contrast levels
- Color temperature (warm/cool tones)
- Individual channel analysis

### 📐 **Dimension Analysis**
- Image dimensions and total pixels
- Aspect ratio calculation
- Resolution classification
- Display size estimates at different DPIs

### 🔍 **Sharpness & Detail**
- Edge detection using Canny algorithm
- Sharpness assessment
- Detail level quantification
- Blur detection

### 💡 **Brightness & Exposure**
- Overall brightness measurement
- Exposure classification (over/underexposed)
- Per-channel brightness analysis

## File Structure

```
IMAGE ANALYSIS/
├── app.py              # Main Flask application with local analysis
├── requirements.txt    # Python dependencies (no external APIs)
├── templates/
│   └── index.html     # Frontend interface
├── uploads/           # Temporary upload directory (created automatically)
└── README.md          # This file
```

## API Endpoints

- `GET /` - Main application page
- `POST /upload` - Upload an image
- `POST /analyze` - Analyze uploaded image with a query (local analysis)
- `POST /reset` - Clear session and uploaded image

## Technology Stack

- **Backend**: Flask (Python)
- **Image Processing**: OpenCV, PIL (Pillow)
- **Numerical Computing**: NumPy
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **No External APIs**: All processing happens locally

## Troubleshooting

**Common Issues:**

1. **"File type not allowed"**: Ensure your image is in JPEG, PNG, WebP, or GIF format
2. **"File size too large"**: Images must be under 16MB
3. **"Analysis failed"**: Check if OpenCV and PIL are properly installed

**Dependencies Issues:**
- Make sure you're using Python 3.8+
- Try installing dependencies in a virtual environment
- Update pip: `pip install --upgrade pip`

**OpenCV Installation:**
If you encounter OpenCV installation issues, try:
```bash
pip install opencv-python-headless
```

## Performance Notes

- All image processing happens locally on your machine
- No internet connection required after initial setup
- Processing time depends on image size and complexity
- Temporary files are automatically cleaned up when you upload a new image or close the session

## License

This project is for educational purposes. Uses open-source computer vision libraries for local image processing.
