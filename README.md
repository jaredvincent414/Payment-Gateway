# Payment Gateway API

A simple RESTful API for processing payments using PayPal 
## Features

- Process payments without user authentication
- API versioning
- PayPal integration
- Automated testing and deployment using GitHub Actions

## Requirements

- Django 5.2+
- Django REST Framework
- PayPal REST SDK

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd payment-gateway
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```
Then edit the `.env` file with your actual configuration values.

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### 1. Initiate a Payment
- **URL**: `/api/v1/payments/`
- **Method**: POST
- **Request Body**:
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
}
```
- **Response**:
```json
{
    "payment": {
        "id": "uuid",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": "50.00",
        "status": "pending"
    },
    "approval_url": "https://paypal.com/approve-payment",
    "status": "success",
    "message": "Payment initiated successfully."
}
```

### 2. Get Payment Status
- **URL**: `/api/v1/payments/{id}/`
- **Method**: GET
- **Response**:
```json
{
    "payment": {
        "id": "uuid",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": "50.00",
        "status": "completed"
    },
    "status": "success",
    "message": "Payment details retrieved successfully."
}
```

## Testing

Run the test suite:
```bash
python manage.py test
```

## CI/CD

The project includes a GitHub Actions workflow for continuous integration and deployment. The workflow:
1. Runs tests on push to main branch
2. Checks code style
3. Deploys to production if tests pass

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
