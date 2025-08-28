# CPA Affiliate Network

[![telegram_badge]][telegram_link]

## Table of Contents

*   [About](#about)
*   [Affiliate UI](#affiliate-ui)
*   [API Spec](#api-spec)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
*   [Features](#features)
*   [API Documentation](#api-documentation)
*   [Development](#development)
*   [Contribute](#contribute)
*   [License](#license)

## About

This repository hosts the backend for the CPA Network, a robust and scalable platform designed for managing affiliate marketing campaigns. It provides the core infrastructure for tracking, reporting, and optimizing performance for Cost Per Action (CPA) campaigns, and now includes a server-rendered user interface for affiliates.

**Keywords:** Affiliate Tracking Software, CPA Platform, Affiliate Management Platform, Performance Marketing Backend and UI

## Affiliate UI

This project now includes a server-rendered Affiliate User Interface, This UI provides an out-of-the-box experience for affiliates to manage their campaigns and view their performance.

Key functionalities include:

*   **Affiliate Login & Authentication:** Secure web-based login for affiliates.
*   **Main Dashboard View:** A summary of performance metrics (clicks, conversions, earnings) upon login.
*   **Offer Browsing:** Ability to browse, search, and filter available offers.
*   **Detailed Reports**

### Screenshots

Here are some screenshots of the Affiliate UI:

*   **Dashboard**
    ![Affiliate Dashboard](https://drive.google.com/uc?export=view&id=1I5ijLTShvc_AhXi3KMd2Ini0oIcEr_iu)

*   **Offer Browsing**
    ![Offer Browsing Page](https://drive.google.com/uc?export=view&id=17hrxz8-7IC41Oz-3TkysM7A5_n8COc1r)

*   **Daily Report**
    ![Daily Report Page](https://drive.google.com/uc?export=view&id=19FaMNwg_5PW_SbDX2T-U0GzkLDmRlHr0)

*   **Offer Report**
    ![Offer Report Page](https://drive.google.com/uc?export=view&id=1GHZGLSGpMw8DY8SqxR_oP_NfNbCeGlBs)


## API Spec

[![](https://drive.google.com/uc?export=view&id=1PQxLndC4ZJ1YYUqUsoCc5pLq-r9e1hxd)](https://cpanova.github.io/cpa-network/index.html)

## Getting Started

Follow these steps to get a local copy of the project up and running for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your system:

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cpanova/cpa-network.git
    cd cpa-network/api
    ```
2.  **Configure Environment Variables:**
    *   Copy the example local settings file:
        ```bash
        cp project/settings/local.dist.py project/settings/local.py
        ```
    *   Copy the example environment variables file:
        ```bash
        cp .env.dist .env
        ```
    *   Edit `.env` and `project/settings/local.py` to configure your database and other settings.

3.  **Start the Development Environment:**
    ```bash
    docker compose up --build -d
    ```
    This command will build the Docker images (if not already built), create the necessary containers, and start them in detached mode.

## Features

*   **Affiliate Registration:** Allows new affiliates to sign up and manage their accounts.
*   **Offer Management:** Comprehensive tools for creating, configuring, and managing advertising offers.
*   **Conversion Import:** Facilitates the import of conversion data from various sources for accurate tracking.
*   **Reports:** Generates detailed reports on campaign performance, conversions, and affiliate earnings.

## API Documentation

Explore the full API documentation for detailed endpoints, request/response formats, and usage examples:

[API Documentation](https://cpanova.github.io/cpa-network/index.html)

## Development

Once the development environment is running:

*   **Django Admin:** Access the Django administration panel at `http://0.0.0.0:8000/admin/login/`
*   **API Spec:** View the browsable API at `http://0.0.0.0:8000/api/`

## Contribute

We welcome contributions! Please take part in our short [survey](https://forms.gle/fCU6NYjuY8A1J8xd6) (5 questions, no email) to help us improve.

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[telegram_badge]: https://img.shields.io/badge/telegram-252850?style=plastic&logo=telegram
[telegram_link]: https://t.me/bloogrox
