# 🚀 Portal BT

## 🛠️ Getting Started

Follow these steps to get the project up and running in your local environment using Docker.

### 📦 Clone the repository

```bash
git clone https://github.com/AndriwRC/portal-bt.git
cd portal-bt
````

### ⚙️ Set environment variables

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Then, edit the `.env` file and set your environment variables accordingly.

### 🐳 Build the Docker image

To build the image with Docker Compose:

```bash
docker-compose up --build -d
```

### ▶️ Run the container

After building, you can run the container with:

```bash
docker-compose up -d
```

### 🛑 Stop the container

To stop the running containers:

```bash
docker-compose down
```