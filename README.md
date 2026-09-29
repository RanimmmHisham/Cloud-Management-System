# 🚀 Cloud Management System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat\&logo=python\&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?style=flat\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![QEMU](https://img.shields.io/badge/Virtualization-QEMU-FF6600?style=flat\&logo=qemu\&logoColor=white)](https://www.qemu.org/)
[![GUI](https://img.shields.io/badge/UI-Tkinter%20%2B%20ttkbootstrap-0275d8?style=flat)](https://ttkbootstrap.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A desktop application for managing virtual machines and Docker-based container workloads through a unified graphical interface.

The system combines **QEMU virtualization** and **Docker container management** in a single Python application, allowing users to create virtual machines, build and manage Docker images, search Docker Hub, pull images, and manage running containers without relying entirely on command-line tools.

---

## ✨ Features

### 🖥️ Virtual Machine Management

The application provides a graphical interface for configuring and launching x86_64 virtual machines using QEMU.

* Configure the number of CPU cores.
* Allocate custom memory.
* Select a virtual disk image.
* Attach an Ubuntu ISO installation image.
* Launch VMs using `qemu-system-x86_64`.
* Execute VM initialization in a background thread to keep the GUI responsive.

### 🐳 Docker Image Management

Manage Docker images directly from the application.

* Create and edit Dockerfiles through the GUI.
* Build Docker images with custom names and tags.
* List locally available Docker images.
* Search for images in the local Docker cache.
* Search Docker Hub for available images.
* Pull images from Docker Hub.
* Display image names, tags, and image IDs.

### 📦 Container Management

Manage the lifecycle of Docker containers through the graphical interface.

* Run Docker containers in detached mode.
* Assign custom container names.
* Configure host-to-container port mappings.
* List currently running containers.
* Display container IDs, names, images, and statuses.
* Stop running containers.

### ⚡ Responsive GUI

Long-running operations are executed using Python background threads so that operations such as:

* Docker image builds
* Image pulls
* VM initialization
* Docker Hub searches

do not block the main graphical interface.

### 🎨 Modern User Interface

The application uses **Tkinter** with **ttkbootstrap** to provide a modern desktop interface with a dark-themed developer-oriented design.

---

## 🏗️ System Architecture

```text
+--------------------------------------------------------+
|              Cloud Management System                   |
|              Tkinter + ttkbootstrap GUI               |
+---------------------------+----------------------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
     +---------------+             +------------------+
     | Virtual       |             | Docker Engine    |
     | Machines      |             |                  |
     +-------+-------+             +--------+---------+
             |                              |
             | subprocess                   | Docker SDK
             v                              v
     +---------------+             +------------------+
     | QEMU          |             | Docker Daemon    |
     | Hypervisor    |             |                  |
     +---------------+             +--------+---------+
                                            |
                              +-------------+-------------+
                              |                           |
                              v                           v
                         Docker Images               Containers
                              |
                              v
                         Docker Hub
```

---

## 🔧 Main Operations

| Operation               | Description                                                    |
| ----------------------- | -------------------------------------------------------------- |
| Create Virtual Machine  | Configure and launch an x86_64 VM using QEMU                   |
| Create Dockerfile       | Generate and save a Dockerfile through the GUI                 |
| Build Docker Image      | Build a Docker image from a Dockerfile                         |
| List Docker Images      | Display locally available Docker images                        |
| List Running Containers | Display active Docker containers                               |
| Stop Container          | Stop a running container                                       |
| Search Local Image      | Search locally available Docker images                         |
| Search Docker Hub       | Search the public Docker Hub registry                          |
| Pull Image              | Download an image from Docker Hub                              |
| Run Container           | Create and start a Docker container with optional port mapping |

---

## 🛠️ Technologies

* **Python 3.9+**
* **Tkinter** — Desktop graphical user interface
* **ttkbootstrap** — Modern styling and themes for Tkinter
* **Docker SDK for Python** — Programmatic Docker management
* **Docker Engine** — Container runtime
* **QEMU** — Virtual machine virtualization
* **Threading** — Background execution for long-running operations
* **Subprocess** — Integration with QEMU and Docker CLI operations

---

## 📋 Requirements

Before running the application, make sure the following are installed:

### Python

Python 3.9 or later.

Check your installation:

```bash
python --version
```

### Docker

Docker Engine must be installed and running.

Check Docker:

```bash
docker --version
```

The application uses the Docker daemon through the Docker SDK for Python.

### QEMU

QEMU is required for the virtual machine functionality.

Check QEMU:

```bash
qemu-system-x86_64 --version
```

> **Note:** QEMU functionality requires a compatible x86_64 environment and appropriate virtual machine disk/ISO files.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/RanimmmHisham/cloud.git
cd cloud
```

### 2. Install Python dependencies

```bash
pip install docker ttkbootstrap
```

Alternatively, if a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

### 3. Make sure Docker is running

Start Docker Engine before launching the application.

### 4. Run the application

```bash
python main.py
```

---

## 🖥️ Usage

After launching the application, the main interface provides access to the available VM and Docker management operations.

### Example Docker Workflow

```text
Create Dockerfile
       ↓
Build Docker Image
       ↓
List Docker Images
       ↓
Pull / Search Images
       ↓
Run Container
       ↓
List Running Containers
       ↓
Stop Container
```

### Example VM Workflow

```text
Select VM Configuration
       ↓
Choose CPU & Memory
       ↓
Select Disk Image
       ↓
Select Ubuntu ISO
       ↓
Create Virtual Machine
       ↓
Launch through QEMU
```

---


## 📁 Project Structure

```text
Cloud-Management-System/
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
│
└── screenshots/
    ├── main-interface.png
    ├── docker-management.png
    └── vm-configuration.png
```

> The exact file structure may vary depending on the current version of the project.

---

## 🧠 Technical Highlights

### Docker SDK Integration

The application communicates with the local Docker daemon through the **Docker SDK for Python**, enabling programmatic management of:

* Images
* Containers
* Image builds
* Image pulls
* Container execution
* Container status

### QEMU Integration

QEMU is accessed through Python's `subprocess` module to create and launch x86_64 virtual machines with configurable:

* CPU allocation
* Memory allocation
* Disk images
* ISO installation media

### Background Processing

Long-running operations are executed using Python's `threading` module. This prevents Docker builds, image downloads, and VM operations from freezing the graphical interface.

---

## 🔐 Design Considerations

The project demonstrates integration between several system-level technologies:

* GUI-based system administration
* Virtual machine management
* Container lifecycle management
* Docker API interaction
* Command-line process integration
* Background task execution

It was designed as a practical desktop tool for bringing common virtualization and container management operations into one interface.

---
