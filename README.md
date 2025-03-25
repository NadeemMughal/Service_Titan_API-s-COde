# ServiceTitan Workflow API

This is related to "ServiceTitan_Retell_AI-BookingCode.py" File

**Author:** Muhammad Nadeem, AI Engineer  
**Date:** March 25, 2025  

Welcome to the **ServiceTitan Workflow API**, a powerful integration tool designed to streamline customer management and job booking processes within the ServiceTitan platform. Developed by Muhammad Nadeem, an AI Engineer, this API leverages modern web technologies to provide a seamless experience for handling both new and existing customers in a service-oriented business environment. Whether you're automating customer lookups, creating new customer profiles, or scheduling jobs, this project offers a robust solution tailored for efficiency and scalability.

## Table of Contents
- [Project Overview](#project-overview)
- [Purpose and Goals](#purpose-and-goals)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technologies Behind the Project](#technologies-behind-the-project)
- [Setup and Installation](#setup-and-installation)
- [Configuration Overview](#configuration-overview)
- [API Functionality](#api-functionality)
- [Who Should Use This](#who-should-use-this)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
The ServiceTitan Workflow API is a FastAPI-based application designed to interact with the ServiceTitan CRM and Job Management systems. It simplifies the process of managing customer data and scheduling service jobs by providing a set of well-defined endpoints. This project is particularly useful for businesses that rely on ServiceTitan for their operations and need an automated way to handle customer interactions, such as responding to incoming calls, creating customer records, and booking appointments.

As an AI Engineer, Muhammad Nadeem built this tool to bridge the gap between real-time customer events (like phone calls) and the ServiceTitan platform, ensuring a smooth workflow for service teams.

## Purpose and Goals
The primary goal of this API is to enhance operational efficiency for ServiceTitan users by:
- Automating customer lookups based on phone numbers from incoming calls.
- Enabling the creation of new customer profiles with associated locations.
- Facilitating job scheduling with detailed appointment information.
- Providing real-time integration capabilities through webhook support.

This project aims to reduce manual effort, minimize errors, and improve response times in customer service workflows.

## Key Features
- **Webhook Integration**: Captures phone numbers from incoming calls and retrieves matching customer data instantly.
- **Customer Management**: Supports fetching existing customers by phone or creating new ones with full address and contact details.
- **Location Handling**: Retrieves location information tied to customers for accurate job assignments.
- **Job Booking**: Allows detailed job creation, including appointment schedules, technician assignments, and custom metadata.
- **Time Zone Support**: Provides current time in Pakistan Standard Time for scheduling accuracy.
- **Error Handling**: Returns clear error messages for invalid inputs or system issues.
- **Logging**: Tracks all operations for troubleshooting and monitoring.

## How It Works
The API operates as a middle layer between external events (e.g., phone calls) and the ServiceTitan platform. Here’s a simplified workflow:
1. **Webhook Trigger**: When a call comes in, the system captures the caller’s phone number and sends it to the API.
2. **Customer Lookup**: The API checks ServiceTitan for existing customers matching the phone number.
3. **Customer Creation**: If no match is found, a new customer profile can be created with details like name, address, and phone.
4. **Location Retrieval**: The API fetches or generates location IDs linked to the customer.
5. **Job Booking**: A job is scheduled with specifics like appointment times, technician assignments, and job type.
6. **Response**: The API returns relevant IDs and confirmation messages for further use.

All interactions with ServiceTitan are authenticated securely using API credentials, ensuring data integrity.

## Technologies Behind the Project
This project leverages modern tools and services:
- **Python**: The backbone language, chosen for its versatility and rich ecosystem.
- **FastAPI**: A high-performance framework for building APIs with asynchronous capabilities.
- **ServiceTitan API**: Connects to CRM and Job Management endpoints for customer and job operations.
- **Asynchronous HTTP Client**: Handles external API calls efficiently.
- **Data Validation**: Ensures input data meets ServiceTitan’s requirements.
- **Time Zone Library**: Manages time conversions for accurate scheduling.
- **Web Server**: Runs the API with reload capabilities for development.

## Setup and Installation
To get started with this project locally, follow these high-level steps:

### Prerequisites
- A recent version of Python (3.10+ recommended).
- Access to Git for cloning the repository.
- ServiceTitan API credentials (Client ID, Client Secret, Tenant ID, App Key).

### Steps
1. **Clone the Project**: Download the repository using Git.
2. **Set Up a Virtual Environment**: Isolate dependencies for a clean setup.
3. **Install Required Libraries**: Use a package manager to install necessary Python packages.
4. **Configure Credentials**: Add your ServiceTitan API details to the configuration.
5. **Launch the API**: Run the application to start the server locally.

Detailed instructions with commands are available in the repository.

## Configuration Overview
- **API Credentials**: You’ll need to provide your ServiceTitan Client ID, Client Secret, Tenant ID, and App Key to authenticate requests.
- **Logging Level**: Set to detailed by default for debugging; adjustable for production use.
- **Timezone**: Configured for Pakistan (Asia/Karachi), but customizable for other regions.

## API Functionality
The API offers several key functionalities:
- **Webhook Endpoint**: Processes call events and returns customer data.
- **Customer Lookup**: Searches for customers by phone number.
- **Customer Creation**: Adds new customers with address and contact info, returning IDs.
- **Location Fetching**: Retrieves location details for a customer.
- **Job Scheduling**: Creates jobs with appointment details and metadata.
- **Time Check**: Provides the current time in a specified timezone.

Each function is designed to integrate smoothly with ServiceTitan’s ecosystem.

## Who Should Use This
This project is ideal for:
- **Service Businesses**: Companies using ServiceTitan for HVAC, plumbing, or similar services.
- **Developers**: Those building integrations with ServiceTitan.
- **Automation Enthusiasts**: Individuals or teams looking to streamline customer workflows.
- **AI Engineers**: Professionals exploring API-driven solutions for real-time data processing.

## Contributing
Contributions are encouraged! To contribute:
1. Fork the repository.
2. Create a branch for your feature or fix.
3. Submit a pull request with a clear description of your changes.

## Contact
For inquiries or feedback, contact:  
**Muhammad Nadeem**  
AI Engineer  
**Email:** muhammadnadeem51200@gmail.com  
**LinkedIn:** [https://www.linkedin.com/in/muhammad-nadeem-ml-engineer-researcher/](https://www.linkedin.com/in/muhammad-nadeem-ml-engineer-researcher/)
