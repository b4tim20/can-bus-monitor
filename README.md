# CAN Bus Monitor

## Overview
The CAN Bus Monitor is a Python application designed to interface with CAN Bus systems. It provides a graphical user interface (GUI) for monitoring, logging, and converting CAN Bus data. The application utilizes the Tkinter library for the GUI and the pySerial library for serial communication.

## Features
- Select and connect to a specified COM port.
- Monitor CAN Bus data in real-time.
- Save logged data to a text file.
- Send data to an Arduino for further processing.
- Convert raw CAN Bus data into a readable format.

## Installation

### Prerequisites
- Python 3.x installed on your system.
- pip (Python package installer) should be available.

### Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd can-bus-monitor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) If you want to make the application executable, you can configure the `setup.py` file accordingly.

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Dependencies
The application requires the following Python packages:
- tkinter
- pyserial

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.