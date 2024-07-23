---
date: 2024-07-23T10:52:48.168931
author: AutoGPT <info@agpt.co>
---

# k4

The development of the kiosk management application will be approached with meticulous attention to detail, ensuring that the final product meets all specified requirements and enhancements to cater to a broad user base while maintaining a strong security posture. The application will be built on the tech stack comprising Python for the backend programming, leveraging the FastAPI framework for its asynchronous support and ease in building APIs, PostgreSQL for the database to ensure robust data management, and Prisma as the ORM for efficient database interactions. The system design will incorporate the following key functionalities and features:

- UI Customization: In line with the requirements, the UI will be fully customizable, offering theme support, layout flexibility, multi-language capability, accessibility compliance, interactive elements, real-time content updates, user authentication options, and feedback mechanisms. This approach will ensure that the UI aligns with the municipal brand identity and is universally accessible.

- Local CMS: To manage and schedule a variety of content types including promotional media, informational content, and customer feedback surveys, the CMS will feature scheduling capabilities for specific times or dates, and support for offline functionality. This ensures that content remains relevant and engaging for the target audience.

- Security Features: The application will incorporate user authentication, secure communication through SSL/TLS, data encryption, role-based access control (RBAC), regular security audits, and anti-tampering measures to protect the software and data from unauthorized access or modifications.

- Hardware and Peripherals Support: The system will support durable, industrial-grade touchscreens and robust peripheral devices like barcode scanners and printers, prioritizing easy maintenance and updates. The hardware selection will reflect the need for high reliability in public spaces.

- Analytics and Reporting: Comprehensive analytics and reporting capabilities will include real-time tracking, inventory management, customer interaction data, system performance metrics, customizable reports, predictive analytics, and a mobile-accessible dashboard.

- Multilingual Support and Automated Diagnostics: The application will feature multilingual support and automated diagnostics to enhance usability for a global audience and ensure efficient operation.

- Compatibility and Software Dependencies: The development process will consider compatibility with various operating systems, the need for specific runtime versions, library dependencies, and third-party tools or services interactions. Containerization technologies like Docker may also be incorporated for efficient distribution or deployment.

- Recursive Programming and Human-in-the-Loop: By leveraging recursive programming, the system will manage complexity efficiently. A human-in-the-loop approach will facilitate continuous iteration and refinement of the application, ensuring that development aligns with user feedback and evolving requirements.

- Integrations: Real-time device monitoring, remote management capabilities within the local network, and firewall integration will be incorporated to ensure that the system is comprehensive and secure against potential threats.

This strategic plan outlines our approach to deploying a robust, secure, and user-friendly kiosk management system on a private municipal server, incorporating advanced functionalities and ensuring that the system is adaptable, scalable, and resilient.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'k4'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
