# AI Jyotish Backend

This project serves as the backend for an AI Jyotish application, powered by Google's Gemini, and designed to be deployed on Google Cloud. The frontend will be developed using Flutter.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.11+
* pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-jyotish-backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ai-jyotish-backend
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

You can now access the interactive API documentation at `http://localhost:8000/docs`.

## Features

* **Comprehensive Astrological Calculations**: Utilizes the PyJHora library for a wide range of Vedic astrology calculations.
* **Modern API**: Built with FastAPI, providing a high-performance and easy-to-use API.
* **Data Validation**: Pydantic is used for robust data validation.
* **Scalable Architecture**: The project is structured with modular routers, making it easy to extend and maintain.

## API Endpoints

The API provides a variety of endpoints for astrological calculations, including:

* `/api/v1/comprehensive/full-analysis`: A comprehensive endpoint that returns a full astrological analysis.
* `/api/v1/charts`: Endpoints for generating various divisional charts.
* `/api/v1/dashas`: Endpoints for calculating Dasha periods.
* And many more!

For a full list of endpoints and their details, please refer to the API documentation at `/docs`.

## Tech Stack

* **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **PyJHora**: A library for Vedic astrology calculations.
* **Uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.
* **Gunicorn**: A Python WSGI HTTP Server for UNIX.
* **Swiss Ephemeris**: A library for high-precision astronomical calculations.

## Deployment

This project is intended to be deployed on Google Cloud. Detailed deployment instructions will be provided in the future.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
