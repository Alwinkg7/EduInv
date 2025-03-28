# Edu.Inv: Empowering Education Through Investments

Edu.Inv is a Django-based web application designed to bridge the gap between students seeking financial assistance for education and investors looking to make a meaningful impact while earning returns. The platform prioritizes transparency, accessibility, and fairness, creating a seamless experience for both students and investors.

## Features

- **Student Loan Applications**: Students can apply for tailored loans to fund their education.
- **Investor Opportunities**: Investors can support students while earning returns on their investments.
- **Admin Panel**: Manage users, loan applications, and investor details.
- **Secure File Uploads**: Students can upload necessary documents like Aadhaar, ID proofs, and bank passbooks.
- **Loan Repayment Tracking**: Track repayment schedules, installments, and statuses.
- **Email Notifications**: Integrated email system for communication and updates.
- **Data Flow Diagrams**: Visual representations of system workflows.

## Project Structure

EduInv/ ├── AdminApp/ # Admin-specific functionality ├── EduInv/ # Main project settings and configurations ├── EduInvApp/ # Core application logic │ ├── migrations/ # Database migrations │ ├── templates/ # HTML templates │ ├── static/ # Static assets (CSS, JS, images) ├── media/ # User-uploaded files ├── manage.py # Django management script ├── db.sqlite3 # SQLite database ├── DFD_LEVEL_*.drawio # Data Flow Diagrams └── .idea/ # IDE-specific settings


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/EduInv.git
   cd EduInv
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```
6. Access the application at http://127.0.0.1:8000.



## Configuration

  Email Settings: Update email credentials in EduInv/settings.py for email notifications.
  Stripe Integration: Replace STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY in EduInv/settings.py with your Stripe API keys.
### Usage
  Admin Panel: Access the admin interface at /admin to manage users, loans, and investors.
  Student Portal: Students can apply for loans and track their applications.
  Investor Portal: Investors can view opportunities and manage their investments.
### Data Flow Diagrams
  The project includes Data Flow Diagrams (DFDs) to visualize system workflows:

  Level 0: Overview of the system.
  Level 1: Detailed workflows for Admin, Client, and Investor roles.
### Contributing
  Contributions are welcome! Please follow these steps:

### Fork the repository.
  Create a new branch for your feature or bug fix.
  Commit your changes and push them to your fork.
  Submit a pull request.
## License
  This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, contact alwinkgofficial@gmail.com.






















