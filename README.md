# key-to-stl
# 🔑 Key to STL

Convert photos of physical keys into downloadable 3D STL files for 3D printing. Uses Keygen for license validation and includes a full image-to-STL processing pipeline.

## Features

- **License-Based Access**: Secure license validation using Keygen API
- **Photo Upload**: Simple web interface for uploading key images
- **Image Processing**: OpenCV-based key detection and profile extraction
- **STL Generation**: Automatic 3D model generation from key photos
- **Downloadable Files**: Get ready-to-print STL files instantly

## Project Structure

```
key-to-stl/
├── backend/
│   ├── app.py              # FastAPI application with Keygen integration
│   ├── key_processor.py    # Image processing and STL generation
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html         # Web interface
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Keygen credentials:**
   
   Set environment variables for Keygen:
   ```bash
   export KEYGEN_ACCOUNT_ID="your-account-id"
   export KEYGEN_PRODUCT_TOKEN="your-product-token"
   ```
   

   **IMPORTANT**: Create a `.env` file in the `backend/` directory using `.env.example` as a template:
   ```bash
   cp backend/.env.example backend/.env
   ```
   
   Then edit `backend/.env` and add your actual Keygen credentials:
   ```
   KEYGEN_ACCOUNT_ID=your_actual_account_id
   KEYGEN_PRODUCT_ID=your_actual_product_id
   KEYGEN_TOKEN=your_actual_api_token
   FLASK_SECRET_KEY=generate_random_secret_key_here
   ```
   
   > **⚠️ Security Note**: Never commit your `.env` file to version control. It's already in `.gitignore` to protect your credentials.
3. **Run the API server:**
   ```bash
   python app.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Update API URL (if needed):**
   
   In `frontend/index.html`, update the `API_BASE_URL` if your backend is hosted elsewhere:
   ```javascript
   const API_BASE_URL = 'http://your-backend-url:8000';
   ```

2. **Serve the frontend:**
   
   Open `frontend/index.html` in a browser, or use a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   
   Then visit `http://localhost:8080`

## Usage

1. **Enter License Key**: Validate your license through the Keygen API
2. **Upload Key Photo**: 
   - Place key on flat, plain background
   - Take photo from directly above
   - Ensure good lighting without shadows
3. **Generate STL**: Wait for processing (typically 5-15 seconds)
4. **Download**: Get your 3D printable STL file

## API Endpoints

### POST `/api/validate-license`
Validate a license key with Keygen.

**Request:**
```json
{
  "key": "XXXXX-XXXXX-XXXXX-XXXXX"
}
```

**Response:**
```json
{
  "valid": true,
  "license_id": "...",
  "message": "License validated successfully"
}
```

### POST `/api/generate-stl`
Generate STL file from uploaded key image.

**Request:** Multipart form data with `file` field

**Response:**
```json
{
  "downloadUrl": "/api/download/key_abc123.stl",
  "filename": "key_abc123.stl"
}
```

### GET `/api/download/{filename}`
Download generated STL file.

## Keygen Integration

This project uses [Keygen](https://keygen.sh) for license management:

1. **Product ID**: `02073ec9-de68-4dbb-8a87-54665836fbdd` (Replace Your Key)
2. **Distribution**: Licensed (only valid license holders can generate STLs)
3. **Validation**: Server-side validation via Keygen API

### Creating Licenses

In your Keygen dashboard:
1. Create a new policy for your product
2. Generate licenses for users
3. Distribute license keys to customers

## Technical Stack

- **Backend**: Python, FastAPI, OpenCV, Trimesh
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **License Management**: Keygen API
- **Image Processing**: OpenCV for key detection
- **3D Generation**: Trimesh for STL creation

## Development Notes

### Image Processing Pipeline

1. **Load and preprocess** image (grayscale, blur)
2. **Edge detection** using Canny algorithm
3. **Contour detection** to find key outline
4. **Bitting extraction** along key edge
5. **3D mesh generation** from profile
6. **STL export** for 3D printing

### Future Enhancements

- [ ] Improved key detection with ML models
- [ ] Support for different key types (car keys, padlock keys, etc.)
- [ ] Scale detection using reference objects
- [ ] Real-time preview of 3D model
- [ ] Batch processing of multiple keys
- [ ] Usage tracking and analytics via Keygen

## License

This project is for demonstration purposes. Check with Keygen for commercial licensing.

## Support

For issues related to:
- **License validation**: Check your Keygen account and product token
- **Image processing**: Ensure photos meet quality guidelines
- **STL files**: Verify generated files in 3D printing software before printing

---

**Built with Keygen** 🚀
